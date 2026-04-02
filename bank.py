import oracledb
import random
def gen_accnum():
    while True:
        new_acc = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100000,999999)}"
        cursor.execute("select count(*) from accounts where account_number = :1", [new_acc])
        if cursor.fetchone()[0] == 0:
            return new_acc

def bank(userid):
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
                new_acc = gen_accnum()
                bancode = "00" + input("은행선택 1:하나은행, 2:우리은행, 3:국민은행, 4:신한은행, 5:기업은행")
                while True:
                    bal = input("초기 입금액(1000원 이상) : ")
                    if int(bal) >= 1000: break
                nick = input("계좌 별명 : ")
                sql = "insert into accounts values(:1,:2,:3,:4,:5)"
                cursor.execute(sql, [new_acc,userid,bancode,bal,nick])
                conn.commit()
            case '2':
                sql = "select * from accounts where user_ID = :1"
                cursor.execute(sql,{userid})
                if cursor:
                    for row in cursor:
                        print(row)
                else:
                    print("계좌 없음")
            case '7': break


conn = oracledb.connect(user = 'c##bank', password = 'bank', dsn='localhost:1521/free')
cursor = conn.cursor()
while True:
    n = input("""===메인메뉴===
1. 회원가입
2. 로그인
3. 종료
선택 : """)
    
    if n =='1':
        while True:
            print("====회원가입 서비스====")
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
                sql = "insert into users (user_ID, password, name, phone, address) values (:id, :ps, :name, :phone, :address)"
                cursor.execute(sql,{'id':id, 'ps':ps, 'name':name, 'phone':phone, 'address':address})
                conn.commit()
                break
        print("회원가입 완료")
    elif n=='2':
        id = input("ID 입력: ")
        ps = input("비밀번호 입력: ")
        sql = "select password from users where user_ID = :id"
        cursor.execute(sql, {'id':id})
        row = cursor.fetchone()
        if row is None:
            print("존재하지 않는 아이디")
        elif row[0] == ps:
            print("로그인 성공")
            bank(id)
        else:
            print("비밀번호 틀림")    
    else:
        print("종료합니다.")
        break
cursor.close()
conn.close()
