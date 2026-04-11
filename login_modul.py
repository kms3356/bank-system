from tabulate import tabulate

def in_put():
    print("\n" + "="*21)
    print("MAIN MENU".center(21))
    print("="*21)
    print(tabulate([["1", "회원가입"], ["2", "로그인"], ["q", "종료"]], headers=["번호", "메뉴"], tablefmt="rounded_grid"))
    return(input("선택 : "))

def ID_gen(cursor):
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

def join_mem(cursor, conn):
    try:
        print("====회원가입 서비스====")
        id, ps, name, phone, address = ID_gen(cursor)
        sql = "insert into users (user_ID, password, name, phone, address) values (:id, :ps, :name, :phone, :address)"
        cursor.execute(sql,{'id':id, 'ps':ps, 'name':name, 'phone':phone, 'address':address})
    except Exception as e:
        conn.rollback()
        print(f"회원가입 중 오류 발생 : {e})")
        return
    print("회원가입이 완료되었습니다.")
    conn.commit()

def log_in(cursor, conn):
    try:
        id = input("\n" + "ID 입력: ")
        ps = input("비밀번호 입력: ")
        sql = "select password from users where user_ID = :id"
        cursor.execute(sql, {'id':id})
        row = cursor.fetchone()
        if row is None:
            print("\n" + "존재하지 않는 아이디입니다.")
        elif row[0] == ps:
            role = admin(id,cursor)
            print("\n" + role + " 로그인 성공!")
            return id, role
            
        else:
            print("\n" + "비밀번호가 틀렸습니다.")
    except Exception as e:
        conn.rollback()
        print(f"로그인 중 오류발생 : {e}")