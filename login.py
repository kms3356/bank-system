import oracledb
import bank
conn = oracledb.connect(user = 'c##bank', password = 'bank', dsn='localhost:1521/free')
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

while True:
    n = input("""===메인메뉴===
1. 회원가입
2. 로그인
3. 종료
선택 : """)
    
    if n =='1':
        try:
            print("====회원가입 서비스====")
            id, ps, name, phone, address = ID_gen()
            sql = "insert into users (user_ID, password, name, phone, address) values (:id, :ps, :name, :phone, :address)"
            cursor.execute(sql,{'id':id, 'ps':ps, 'name':name, 'phone':phone, 'address':address})
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"회원가입 중 오류 발생 : {e})")
            continue
        print("회원가입 완료")

    elif n=='2':
        try:
            id = input("ID 입력: ")
            ps = input("비밀번호 입력: ")
            sql = "select password from users where user_ID = :id"
            cursor.execute(sql, {'id':id})
            row = cursor.fetchone()
            if row is None:
                print("존재하지 않는 아이디")
            elif row[0] == ps:
                print("로그인 성공")
                bank.bank_menu(id,conn,cursor)
            else:
                print("비밀번호 틀림")    
        except Exception as e:
            conn.rollback()
            print(f"로그인 중 오류발생 : {e}")

    else:
        print("종료합니다.")
        break
cursor.close()
conn.close()
