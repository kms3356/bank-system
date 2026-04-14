from tabulate import tabulate
import def_modul
class Bank_session:
    def __init__(self, userid, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.userid = userid

        sql = "select name from users where user_ID = :1"
        self.cursor.execute(sql, [self.userid])
        self.name = self.cursor.fetchone()[0]

    def in_put(self):
        print("\n" + "="*30)
        print(f"{self.name} BANKING SYSTEM".center(28))
        print("="*30)

        print(tabulate([["1", "내 계좌 생성"], ["2", "내 계좌 조회"], ["3", "입금"], ["4", "출금"], 
                        ["5", "계좌이체"], ["6", "거래내역 조회"], ["7", "내 계좌 별명 수정"], ["8", "내 계좌 검색"], ["9", "내 계좌 삭제"],
                        ["q", "로그아웃"]], headers=["번호", "메뉴"], tablefmt="rounded_grid"))
        return(input("선택 : "))

    def acc_generate(self):
        try:
            new_acc, bancode, bal, nick= def_modul.gen_acc(self.cursor)
            sql = "insert into accounts values(:1,:2,:3,:4,:5)"
            self.cursor.execute(sql, [new_acc,self.userid,bancode,bal,nick])
            self.conn.commit()
            print("\n" + "새로운 계좌 생성이 완료되었습니다.")

        except ValueError:
            print("금액은 숫자만 입력 가능합니다.")
        except Exception as e:
            self.conn.rollback()
            print(f"계좌 생성 중 오류발생 : {e}")

    def deposit(self):
        try:
            sel_acc = def_modul.select_acc(self.userid, self.cursor, '3')
            if not sel_acc: return

            while True:
                money = int(input("입금할 금액: "))
                if money <= 0:
                    print("입금액은 0보다 커야합니다.")
                    continue
                else:  break

            sql = "update accounts set balance = balance + :1 where account_number = :2"
            self.cursor.execute(sql, [money,sel_acc])

            sql = "insert into log values(log_no.nextval, :1, :2, '입금', :3, sysdate)"
            self.cursor.execute(sql, [self.userid, sel_acc, money])
            self.conn.commit()
            print(f"\n{sel_acc}계좌에 {money}원 입금 완료되었습니다.")

        except ValueError:
            print("금액은 숫자만 입력 가능합니다.")
        except Exception as e:
            self.conn.rollback()
            print(f"입금 중 오류 발생 : {e}")

    def withdraw(self):
        try:
            sel_acc = def_modul.select_acc(self.userid, self.cursor, '4')
            if not sel_acc: return

            sql = "select balance from accounts where account_number = :1"
            self.cursor.execute(sql, [sel_acc])
            bal = self.cursor.fetchone()
            if bal[0] == 0:
                print("잔액이 없습니다.")
                return
            
            while True:
                money = int(input("출금할 금액: "))
                if bal[0] < money:
                    print("잔액이 부족합니다.")
                    continue
                if money <= 0:
                    print("출금액은 0보다 커야합니다.")
                    continue
                else: break

            sql = "update accounts set balance = balance - :1 where account_number = :2"
            self.cursor.execute(sql, [money,sel_acc])

            sql = "insert into log values(log_no.nextval, :1, :2, '출금', :3, sysdate)"
            self.cursor.execute(sql, [self.userid, sel_acc, money])
            self.conn.commit()
            print(f"\n{sel_acc}계좌에서 {money}원 출금 완료되었습니다.")

        except ValueError:
            print("금액은 숫자만 입력 가능합니다.")
        except Exception as e:
            self.conn.rollback()
            print(f"출금 중 오류 발생 : {e}")

    def log(self):
        try:
            sql = "select * from log where userid = :1 order by log_id"
            self.cursor.execute(sql, [self.userid])
            rows = self.cursor.fetchall()

            if rows:
                header = ["logID", "userID", "계좌번호", "거래내용", "금액", "날짜"]
                print(tabulate(rows, headers=header, tablefmt="fancy_grid", stralign="center", numalign="center"))

            else:
                print("거래내역이 없습니다.")
                return
            
        except Exception as e:
            print(f"거래내역 조회 중 오류 발생 : {e}")

    def ch_nick(self):
        try:
            sel_acc = def_modul.select_acc(self.userid, self.cursor, '5')
            if not sel_acc: return
            n = input("새로운 별명: ")

            sql = "update accounts set nickname = :1 where account_number = :2"
            self.cursor.execute(sql, [n, sel_acc])
            self.conn.commit()
            print("계좌 별명 수정에 성공했습니다.")

        except Exception as e:
            print(f"계좌 별명 수정 중 오류 발생 : {e}")
            self.conn.rollback()

    def acc_search(self):
        try:
            sql = "select * from accounts where userid = :1"
            self.cursor.execute(sql,[self.userid])
            rows = self.cursor.fetchall()

        except Exception as e:
            print(f"계좌 검색 중 오류 발생 : {e}")   
            return

        if rows:
            search_menu = [["1", "계좌번호"], ["2", "별명"], ["3", "은행"]]
            header = ["번호", "검색 대상"]

            while True:
                print(tabulate(search_menu, headers=header, tablefmt="rounded_grid"))
                n = input("선택 : ")
                if n in ('1','2','3'): break
                else:
                    print("다시 입력")
                    continue 

            if n == '1':
                def_modul.search('account_number', '계좌번호', self.cursor, self.userid)
            if n == '2':
                def_modul.search('nickname', '별명', self.cursor, self.userid)
            if n == '3':
                def_modul.search('bankid', '은행', self.cursor, self.userid)
        else:
            print("계좌가 없습니다.")
            return
        
    def acc_del(self):
        sel_acc = def_modul.select_acc(self.userid, self.cursor, '5')
        if not sel_acc: return
        try:
            sql = "delete from log where account_number = :1"
            self.cursor.execute(sql, [sel_acc])
            sql = "delete from accounts where account_number = :1"
            self.cursor.execute(sql, [sel_acc])
            self.conn.commit()
            print("계좌 삭제에 성공했습니다.")

        except Exception as e:
            print(f"계좌 삭제 중 오류 발생 : {e}")
            self.conn.rollback()