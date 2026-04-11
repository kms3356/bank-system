import os
import oracledb
import bank
from tabulate import tabulate
from dotenv import load_dotenv
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dsn = os.getenv("DB_DSN")

conn = oracledb.connect(user = user, password = password, dsn=dsn)
cursor = conn.cursor()

def ID_gen():
    while True:
        id = input("ID 생성: ")
        sql = "select count(*) from users where user_ID = :id"
        cursor.execute(sql, {'id' : id})
        row = cursor.fetchone()
        if row[0] > 0:
            print("ID중복. 다시 입력하세요.")
            continue
        else: 
            ps = input("비밀번호 입력: ")
            name = input("이름 입력: ")
            phone = input("전화번호 입력: ")
            address = input("주소 입력: ")
            return id, ps, name, phone, address

def admin(id, cursor):
    sql = "select role from users where user_id = :1"
    cursor.execute(sql,[id])
    role = cursor.fetchone()[0]
    return role

menu_data = [["1", "회원가입"], ["2", "로그인"], ["q", "종료"]]
while True:
    print("\n" + "="*21)
    print("MAIN MENU".center(21))
    print("="*21)
    print(tabulate(menu_data, headers=["번호", "메뉴"], tablefmt="rounded_grid"))
    n = input("선택 : ")
    
    if n =='1':
        try:
            print("====회원가입 서비스====")
            id, ps, name, phone, address = ID_gen()
            sql = "insert into users (user_ID, password, name, phone, address) values (:id, :ps, :name, :phone, :address)"
            cursor.execute(sql,{'id':id, 'ps':ps, 'name':name, 'phone':phone, 'address':address})
        except Exception as e:
            conn.rollback()
            print(f"회원가입 중 오류 발생 : {e})")
            continue
        print("회원가입 완료")
        conn.commit()

    elif n=='2':
        try:
            id = input("\n" + "ID 입력: ")
            ps = input("비밀번호 입력: ")
            sql = "select password from users where user_ID = :id"
            cursor.execute(sql, {'id':id})
            row = cursor.fetchone()
            if row is None:
                print("\n" + "존재하지 않는 아이디")
            elif row[0] == ps:
                print("\n" + "로그인 성공")
                role = admin(id,cursor)
                if role == 'user':
                    bank.bank_menu(id,conn,cursor)
                elif role == 'admin':
                    bank.admin_menu(conn,cursor)
            else:
                print("\n" + "비밀번호 틀림")    
        except Exception as e:
            conn.rollback()
            print(f"로그인 중 오류발생 : {e}")

    elif n=='q':
        print("종료합니다.")
        break
    else:
        print("잘못된 입력")
        continue
cursor.close()
conn.close()