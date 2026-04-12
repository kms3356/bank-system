import def_modul
import bank_modul
import admin_modul

def bank_menu(userid,conn,cursor):
    
    bank_session = bank_modul.Bank_session(userid, conn, cursor)
    acc_trans = def_modul.Acc_transfer(userid, cursor, conn)
    while True:

        n = bank_session.in_put()
        match n:
            case '1': 
                bank_session.acc_generate()

            case '2':
                def_modul.select_acc(userid, cursor, '2')

            case '3':
                bank_session.deposit()

            case '4':
                bank_session.withdraw()

            case '5':
                n = acc_trans.in_put()
                if n == '1':
                    acc_trans.my_acc()
                elif n == '2':
                    acc_trans.local_acc()
                elif n == '3':
                    acc_trans.unified_acc()
                else:
                    print("잘못된 입력입니다.")
                    continue
                    
            case '6':
                bank_session.log()

            case '7':
                bank_session.ch_nick()

            case '8':
                bank_session.acc_search()

            case 'q': break

            case _:
                print("잘못된 입력입니다.")
                continue


def admin_menu(conn,cursor):
    ad_session = admin_modul.Admin_session(conn, cursor)
    while True:
        n = admin_modul.in_put()
        match n:
            case '1':
                ad_session.user_inquiry()

            case '2':
                ad_session.ch_user()

            case '3':
                ad_session.del_user()

            case 'q' : break

            case _:
                print("잘못된 입력입니다.")
                continue
