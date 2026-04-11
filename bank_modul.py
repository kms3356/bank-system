from tabulate import tabulate
import def_modul

def in_put(name):
    print("\n" + "="*30)
    print(f"{name} BANKING SYSTEM".center(28))
    print("="*30)

    print(tabulate([["1", "내 계좌 생성"], ["2", "내 계좌 조회"], ["3", "입금"], ["4", "출금"], 
                    ["5", "계좌이체"], ["6", "거래내역 조회"], ["7", "내 계좌 별명 수정"], ["8", "내 계좌 검색"], 
                    ["q", "로그아웃"]], headers=["번호", "메뉴"], tablefmt="rounded_grid"))
    return(input("선택 : "))

def acc_generate(userid,cursor, conn):
    try:
        new_acc, bancode, bal, nick= def_modul.gen_acc(cursor)
        sql = "insert into accounts values(:1,:2,:3,:4,:5)"
        cursor.execute(sql, [new_acc,userid,bancode,bal,nick])
        conn.commit()
        print("\n" + "새로운 계좌 생성이 완료되었습니다.")

    except ValueError:
        print("금액은 숫자만 입력 가능합니다.")
    except Exception as e:
        conn.rollback()
        print(f"계좌 생성 중 오류발생 : {e}")

def deposit(userid,cursor,conn):
    try:
        sel_acc = def_modul.select_acc(userid, cursor, '3')
        if not sel_acc: return

        money = int(input("입금할 금액: "))
        while True:
            if money <= 0:
                print("입금액은 0보다 커야합니다.")
                continue
            else:  break

        sql = "update accounts set balance = balance + :1 where account_number = :2"
        cursor.execute(sql, [money,sel_acc])

        sql = "insert into log values(log_no.nextval, :1, :2, '입금', :3, sysdate)"
        cursor.execute(sql, [userid, sel_acc, money])
        conn.commit()
        print(f"\n{sel_acc}계좌에 {money}원 입금 완료되었습니다.")

    except ValueError:
        print("금액은 숫자만 입력 가능합니다.")
    except Exception as e:
        conn.rollback()
        print(f"입금 중 오류 발생 : {e}")

def withdraw(userid,cursor,conn):
    try:
        sel_acc = def_modul.select_acc(userid, cursor, '4')
        if not sel_acc: return

        sql = "select balance from accounts where account_number = :1"
        cursor.execute(sql, [sel_acc])
        bal = cursor.fetchone()

        while True:
            money = int(input("출금할 금액: "))
            if bal[0] < money or money < 0:
                print("출금액 입력 오류. 다시 입력하세요.")
            else: break

        sql = "update accounts set balance = balance - :1 where account_number = :2"
        cursor.execute(sql, [money,sel_acc])

        sql = "insert into log values(log_no.nextval, :1, :2, '출금', :3, sysdate)"
        cursor.execute(sql, [userid, sel_acc, money])
        conn.commit()
        print(f"\n{sel_acc}계좌에서 {money}원 출금 완료되었습니다.")

    except ValueError:
        print("금액은 숫자만 입력 가능합니다.")
    except Exception as e:
        conn.rollback()
        print(f"출금 중 오류 발생 : {e}")

def log(userid,cursor):
    try:
        sql = "select * from log where userid = :1 order by log_id"
        cursor.execute(sql, [userid])
        rows = cursor.fetchall()

        if rows:
            header = ["logID", "userID", "계좌번호", "거래내용", "금액", "날짜"]
            print(tabulate(rows, headers=header, tablefmt="fancy_grid", stralign="center", numalign="center"))

        else:
            print("거래내역이 없습니다.")
            return
        
    except Exception as e:
        print(f"거래내역 조회 중 오류 발생 : {e}")

def ch_nick(userid,cursor,conn):
    try:
        sel_acc = def_modul.select_acc(userid, cursor, '5')
        if not sel_acc: return
        n = input("새로운 별명: ")

        sql = "update accounts set nickname = :1 where account_number = :2"
        cursor.execute(sql, [n, sel_acc])
        conn.commit()
        print("계좌 별명 수정에 성공했습니다.")

    except Exception as e:
        print(f"계좌 별명 수정 중 오류 발생 : {e}")
        conn.rollback()

def acc_search(userid,cursor):
    try:
        sql = "select * from accounts where userid = :1"
        cursor.execute(sql,[userid])
        rows = cursor.fetchall()

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
            def_modul.search('account_number', '계좌번호', cursor, userid)
        if n == '2':
            def_modul.search('nickname', '별명', cursor, userid)
        if n == '3':
            def_modul.search('bankid', '은행', cursor, userid)
    else:
        print("계좌가 없습니다.")
        return