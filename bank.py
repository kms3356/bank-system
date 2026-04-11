from tabulate import tabulate
import def_modul
import bank_modul
import admin_modul

def bank_menu(userid,conn,cursor):
    sql = "select name from users where user_ID = :1"
    cursor.execute(sql, [userid])
    name = cursor.fetchone()[0]

    while True:
        n = bank_modul.in_put(name)
        match n:
            case '1': 
                bank_modul.acc_generate(userid,cursor,conn)

            case '2':
                def_modul.select_acc(userid, cursor, '2')

            case '3':
                bank_modul.deposit(userid,cursor,conn)

            case '4':
                bank_modul.withdraw(userid,cursor,conn)

            case '5':
                me_data = [["1", "내 계좌로 이체"], ["2", "로컬 계좌로 이체"], ["3", "통합 계좌로 이체"]]
                print(tabulate(me_data, headers=["번호", "계좌이체 메뉴"], tablefmt="rounded_grid"))
                n = input("선택 : ")
                if n == '1':
                    def_modul.my_acc(userid, cursor, conn)
                elif n == '2':
                    def_modul.local_acc(userid, cursor, conn)
                elif n == '3':
                    def_modul.unified_acc(userid, cursor, conn)
                else:
                    print("잘못된 입력입니다.")
                    continue
                    
            case '6':
                bank_modul.log(userid,cursor)

            case '7':
                bank_modul.ch_nick(userid,cursor,conn)

            case '8':
                bank_modul.acc_search(userid,cursor)

            case 'q': break

            case _:
                print("잘못된 입력입니다.")
                continue


def admin_menu(conn,cursor):
    while True:
        n = admin_modul.in_put()
        match n:
            case '1':
                admin_modul.user_inquiry(cursor)

            case '2':
                admin_modul.ch_user(cursor,conn)

            case '3':
                admin_modul.del_user(cursor,conn)

            case 'q' : break

            case _:
                print("잘못된 입력입니다.")
                continue
