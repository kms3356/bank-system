import random
from tabulate import tabulate
import oracledb
import os
from dotenv import load_dotenv


def gen_acc(cursor):
    while True:
        new_acc = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100000,999999)}"
        cursor.execute("select count(*) from accounts where account_number = :1", [new_acc])
        if cursor.fetchone()[0] == 0:
            break

    while True:
        ban_menu = [['1', '하나은행'],['2', '우리은행'],['3', '국민은행'],['4', '신한은행'],['5', '기업은행']]
        print(tabulate(ban_menu, headers=["번호", "은행이름"], tablefmt="rounded_grid"))
        n = int(input("번호 선택 : "))
        if 0 < n < 6:
            bancode = ban_menu[n-1][1]
            break
        else: 
            print("잘못된 입력입니다.")
            continue
    
    while True:
        bal = input("초기 입금액(1000원 이상) : ")
        if int(bal) >= 1000: break
    
    nick = input("계좌 별명 : ")
    return new_acc, bancode, bal, nick



def select_acc(userid, cursor, menu, my_to_my=False):
    try:
        sql = "select * from accounts where userid = :1"
        cursor.execute(sql,[userid])
        rows = cursor.fetchall()

        if rows:
            if my_to_my == True and len(rows) == 1: 
                print("계좌 수가 부족합니다.")
                return False
            header = ["번호", "계좌번호", "사용자ID", "은행이름", "잔액", "별명"]
            display = [[i] + list(row) for i, row in enumerate(rows,1)]
            print(tabulate(display, headers=header, tablefmt="fancy_grid", stralign="center", numalign="center"))

            if menu == '2': return
            while True:
                if menu == '3':
                    n = int(input("입금할 계좌 선택: "))
                elif menu == '4':
                    n = int(input("출금할 계좌 선택: "))
                elif menu == '5':
                    n = int(input("계좌 선택: "))
                if 0 < n <= len(rows):
                    return rows[n-1][0]
                else: 
                    print("잘못된 계좌 선택입니다.")
                    continue
        else:
            print("계좌가 없습니다.")
            return False
    except Exception as e:
        print(f"계좌 조회 중 오류 발생 : {e}")
def search(se, cul, cursor, userid):
    while True:
        try:
            n = input(f"검색할 {cul} 입력 : ")
            sql = f"select * from accounts where {se} = :1 and userid = :2"
            cursor.execute(sql, [n, userid])
            rows = cursor.fetchall()

            if not rows:
                print("검색 결과 없음.")
                continue

            else:
                print(tabulate(rows,headers=["계좌번호", "ID", "은행이름", "잔액", "별명"], tablefmt="fancy_grid"))
                break

        except Exception as e:
            print(f"계좌검색 중 오류 발생 : {e}")

class acc_transfer:
    def __init__(self, userid, cursor, conn):
        self.userid = userid
        self.cursor = cursor
        self.conn = conn

    def in_put(self):
        me_data = [["1", "내 계좌로 이체"], ["2", "로컬 계좌로 이체"], ["3", "통합 계좌로 이체"]]
        print(tabulate(me_data, headers=["번호", "계좌이체 메뉴"], tablefmt="rounded_grid"))
        return(input("선택 : "))
    
    def my_acc(self):
        while True:
            sel_acc = select_acc(self.userid, self.cursor, '4', True)
            if not sel_acc:
                return
            
            sel_acc2 = select_acc(self.userid, self.cursor, '3')
            if sel_acc == sel_acc2:
                print("중복된 계좌를 선택하셨습니다.")
                continue
            else: break
        self.account_transfer(sel_acc, sel_acc2)
        

    def account_transfer(self,my_acc, your_acc):
        try:
            sql = "select balance from accounts where account_number = :1"
            self.cursor.execute(sql, [my_acc])
            bal = self.cursor.fetchone()
            if bal[0] == 0:
                print("잔액이 없습니다.")
                return
            while True:
                money = int(input("계좌이체할 금액 입력: "))
                if money < 0:
                    print("금액은 0이상만 입력 가능합니다.")
                    continue
                if bal[0] < money:
                    print("잔액이 부족합니다.")
                    continue
                else: break

            sql = "update accounts set balance = balance - :1 where account_number = :2"
            self.cursor.execute(sql, [money, my_acc])

            sql = "update accounts set balance = balance + :1 where account_number = :2"
            self.cursor.execute(sql, [money, your_acc])

            sql = "insert into log values(log_no.nextval, :1, :2, :3, :4, sysdate)"
            self.cursor.execute(sql, [self.userid, my_acc, '계좌이체 -> ' + your_acc, money])
            self.conn.commit()
            print("\n이체가 성공적으로 완료되었습니다.")

        except ValueError:
            print("숫자만 입력 가능합니다.")
        except Exception as e:
            self.conn.rollback()
            print(f"계좌이체 중 오류 발생 : {e} (모든 작업 취소)")

    def local_acc(self):
        sel_acc = select_acc(self.userid, self.cursor, '4')
        if not sel_acc: return

        while True:
            loc_acc = input("\n입금할 상대 계좌번호 입력. 예시)123-456-789012 : ")
            sql = "select userid from accounts where account_number = :1"
            self.cursor.execute(sql, [loc_acc])
            row = self.cursor.fetchone()

            if row and sel_acc != loc_acc:
                break
            else:
                print("잘못된 계좌번호 입력.")
                continue
        self.account_transfer(sel_acc, loc_acc)
    

    def unified_acc(self):
        sel_acc = select_acc(self.userid, self.cursor, '4')
        if not sel_acc: return

        load_dotenv()
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        dsn = os.getenv("UNIFIED_DB_DSN")

        with oracledb.connect(user = user, password = password, dsn=dsn) as conn2:
            with conn2.cursor() as cursor2:
                try:
                    while True:

                        unify_acc = input("계좌이체 할 상대 계좌 입력 : ")
                        sql = "select user_id from accounts where account_num = :1"
                        cursor2.execute(sql, [unify_acc])
                        rows = cursor2.fetchone()
                        if rows:
                            break
                        else:
                            print("계좌정보 없음")
                            continue

                    sql = "select balance from accounts where account_number = :1"
                    self.cursor.execute(sql, [sel_acc])
                    bal = self.cursor.fetchone()
                    while True:
                        money = int(input("계좌이체할 금액 입력: "))
                        if money < 0 or bal[0] < money:
                            print("금액 오류. 금액 다시 입력.")
                        else: break

                    sql = "update accounts set balance = balance - :1 where account_number = :2"
                    self.cursor.execute(sql, [money, sel_acc])

                    sql = "update accounts set balance = balance + :1 where account_num = :2"
                    cursor2.execute(sql, [money, unify_acc])

                    sql = "insert into log values(log_no.nextval, :1, :2, :3, :4, sysdate)"
                    self.cursor.execute(sql, [self.userid, sel_acc, '통합계좌이체', money])
                    self.conn.commit()
                    conn2.commit()
                    print("\n이체가 성공적으로 완료되었습니다.")

                except ValueError:
                    print("숫자만 입력 가능합니다.")
                except Exception as e:
                    self.conn.rollback()
                    conn2.rollback()
                    print(f"계좌이체 중 오류 발생 : {e} (모든 작업 취소)")
                
