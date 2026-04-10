import random
from tabulate import tabulate
import oracledb

def gen_acc(cursor):
    while True:
        new_acc = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100000,999999)}"
        cursor.execute("select count(*) from accounts where account_number = :1", [new_acc])
        if cursor.fetchone()[0] == 0:
            break
    ban_menu = [['1', '하나은행'],['2', '우리은행'],['3', '국민은행'],['4', '신한은행'],['5', '기업은행']]
    print(tabulate(ban_menu, headers=["번호", "은행이름"]))
    n = int(input("번호 선택 : "))
    bancode = ban_menu[n-1][1]
    
    
    while True:
        bal = input("초기 입금액(1000원 이상) : ")
        if int(bal) >= 1000: break
    
    nick = input("계좌 별명 : ")
    return new_acc, bancode, bal, nick

def select_acc(userid, cursor, menu):
    try:
        sql = "select * from accounts where userid = :1"
        cursor.execute(sql,[userid])
        rows = cursor.fetchall()
        if rows:
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
                    print("잘못된 계좌 선택")
                    continue
        else:
            print("계좌 없음")
    except Exception as e:
        print(f"계좌 조회 중 오류 발생 : {e}")

if __name__ == '__main__':
    with oracledb.connect(user = 'c##bank', password = 'bank', dsn='localhost:1521/free') as conn:
        with conn.cursor() as cur:
            select_acc('qwe', cur, '3')

def my_acc(userid, cursor, conn):
    while True:
        sel_acc = select_acc(userid, cursor, '4')
        sel_acc2 = select_acc(userid, cursor, '3')
        if sel_acc == sel_acc2:
            print("중복. 계좌 다시 선택.")
            continue
        else: break
    account_transfer(userid,sel_acc,sel_acc2, cursor, conn)
    

def account_transfer(userid, my_acc, your_acc, cursor, conn):
    try:
        sql = "select balance from accounts where account_number = :1"
        cursor.execute(sql, [my_acc])
        bal = cursor.fetchone()
        while True:
            money = int(input("계좌이체할 금액 입력: "))
            if money < 0 or bal[0] < money:
                print("금액 오류. 금액 다시 입력.")
            else: break
        sql = "update accounts set balance = balance - :1 where account_number = :2"
        cursor.execute(sql, [money, my_acc])
        sql = "update accounts set balance = balance + :1 where account_number = :2"
        cursor.execute(sql, [money, your_acc])
        sql = "insert into log values(log_no.nextval, :1, :2, :3, :4, sysdate)"
        cursor.execute(sql, [userid, my_acc, '계좌이체 -> ' + your_acc, money])
        conn.commit()
        print("\n이체가 성공적으로 완료되었습니다.")
    except ValueError:
        print("숫자만 입력 가능합니다.")
    except Exception as e:
        conn.rollback()
        print(f"계좌이체 중 오류 발생 : {e} (모든 작업 취소)")

def local_acc(userid, cursor, conn):
    sel_acc = select_acc(userid, cursor, '4')
    while True:
        loc_acc = input("\n입금할 상대 계좌번호 입력. 예시)123-456-789012 : ")
        sql = "select userid from accounts where account_number = :1"
        cursor.execute(sql, [loc_acc])
        row = cursor.fetchone()
        if row:
            break
        else:
            print("잘못된 계좌번호 입력.")
            continue
    account_transfer(userid,sel_acc,loc_acc,cursor,conn)
    
    # se: 진짜 db cul: 한글이름
def search(se, cul, cursor):
    while True:
        try:
            n = input(f"검색할 {cul} 입력 : ")
            sql = f"select * from accounts where {se} = :1"
            cursor.execute(sql, [n])
            rows = cursor.fetchall()
            if not rows:
                print("검색 결과 없음.")
                continue
            else:
                print(tabulate(rows,headers=["계좌번호", "ID", "은행이름", "잔액", "별명"], tablefmt="fancy_grid"))
                break
        except Exception as e:
            print(f"계좌검색 중 오류 발생 : {e}")

        
            

        