import random
from tabulate import tabulate

def gen_acc(cursor):
    while True:
        new_acc = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100000,999999)}"
        cursor.execute("select count(*) from accounts where account_number = :1", [new_acc])
        if cursor.fetchone()[0] == 0:
            break
    bancode = "00" + input("은행선택 (1:하나은행, 2:우리은행, 3:국민은행, 4:신한은행, 5:기업은행): ")
    
    while True:
        bal = input("초기 입금액(1000원 이상) : ")
        if int(bal) >= 1000: break
    
    nick = input("계좌 별명 : ")
    return new_acc, bancode, bal, nick

def bank_menu(userid,conn,cursor):
    while True:
        n = input("""===은행 메뉴===
        1. 내 계좌 생성
        2. 내 계좌 조회
        3. 입금
        4. 출금
        5. 계좌이체
        6. 거래내역 조회
        7. 로그아웃
        선택 : """)
        match n:
            case '1': 
                try:
                    new_acc, bancode, bal, nick= gen_acc(cursor)
                    sql = "insert into accounts values(:1,:2,:3,:4,:5)"
                    cursor.execute(sql, [new_acc,userid,bancode,bal,nick])
                    conn.commit()
                except ValueError:
                    print("금액은 숫자만 입력 가능합니다.")
                except Exception as e:
                    conn.rollback()
                    print(f"계좌 생성 중 오류발생 : {e}")

            case '2':
                try:
                    sql = "select * from accounts where userid = :1"
                    cursor.execute(sql,[userid])
                    rows = cursor.fetchall()
                    if rows:
                        header = ["계좌번호", "사용자ID", "은행ID", "잔액", "별명"]
                        print(tabulate(rows, headers=header, tablefmt="fancy_grid", stralign="center", numalign="center"))
                    else:
                        print("계좌 없음")
                except Exception as e:
                    print(f"계좌 조회 중 오류 발생 : {e}")

            case '3':
                try:
                    acc_num = input("입금할 계좌번호: ")
                    money = int(input("입금할 금액: "))
                    if money <= 0:
                        print("입금액은 0보다 커야합니다.")
                        continue
                    sql = "update accounts set balance = balance + :1 where account_number = :2"
                    cursor.execute(sql, [money,acc_num])

                    if cursor.rowcount == 0:
                        print("존재하지 않는 계좌번호입니다.")
                    else:
                        conn.commit()
                        print(f"{acc_num}계좌에 {money}원 입금 완료되었습니다.")
                except ValueError:
                    print("금액은 숫자만 입력 가능합니다.")
                except Exception as e:
                    conn.rollback()
                    print(f"입금 중 오류 발생 : {e}")

            case '4':
                acc_num = input("출금할 계좌번호: ")
                sql = "select balance from accounts where userid = :1"
                cursor.execute(sql, [userid])
                bal = cursor.fetchone()
                while True:
                    money = input("출금할 금액: ")
                    if bal[0] < money:
                        print("잔액 부족")
                    else: break
                
                
                
            case '7': break


