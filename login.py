import os
import oracledb
from dotenv import load_dotenv
import login_modul
import bank

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

conn = oracledb.connect(user=user, password=password, dsn=dsn)
cursor = conn.cursor()

while True:
    n = login_modul.in_put()
    user_session = login_modul.login_session(conn, cursor)
    if n =='1':
        user_session.join_mem()

    elif n=='2':
        try:
            id, role = user_session.log_in()
            if role == 'user':
                bank.bank_menu(id,conn,cursor)
            elif role == 'admin':
                bank.admin_menu(conn,cursor)
        except TypeError:
            continue

    elif n=='q':
        print("종료합니다.")
        break
    
    else:
        print("잘못된 입력")
        continue
cursor.close()
conn.close()