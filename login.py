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
    if n =='1':
        login_modul.join_mem(cursor,conn)

    elif n=='2':
        id, role = login_modul.log_in(cursor,conn)
        if role == 'user':
            bank.bank_menu(id,conn,cursor)
        elif role == 'admin':
            bank.admin_menu(conn,cursor)

    elif n=='q':
        print("종료합니다.")
        break
    
    else:
        print("잘못된 입력")
        continue
cursor.close()
conn.close()