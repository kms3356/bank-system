from tabulate import tabulate
import hashlib
def in_put():
    print("\n" + "="*21)
    print("MAIN MENU".center(21))
    print("="*21)
    print(tabulate([["1", "회원가입"], ["2", "로그인"], ["q", "종료"]], headers=["번호", "메뉴"], tablefmt="rounded_grid"))
    return(input("선택 : "))

class Login_session:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        
    def ID_gen(self):
        while True:
            id = input("ID 생성: ")
            sql = "select count(*) from users where user_ID = :id"
            self.cursor.execute(sql, {'id' : id})
            row = self.cursor.fetchone()
            if row[0] > 0:
                print("ID중복. 다시 입력하세요.")
                continue

            else: 
                ps = input("비밀번호 입력: ")
                name = input("이름 입력: ")
                phone = input("전화번호 입력: ")
                address = input("주소 입력: ")
                return id, ps, name, phone, address


    def admin(self,id):
        sql = "select role from users where user_id = :1"
        self.cursor.execute(sql,[id])
        role = self.cursor.fetchone()[0]
        return role

    def join_mem(self):
        try:
            hash_obj = hashlib.sha256()
            print("====회원가입 서비스====")
            id, ps, name, phone, address = self.ID_gen()
            hash_obj.update(ps.encode())
            hashed_ps = hash_obj.hexdigest()

            sql = "insert into users (user_ID, password, name, phone, address) values (:id, :ps, :name, :phone, :address)"
            self.cursor.execute(sql,{'id':id, 'ps':hashed_ps, 'name':name, 'phone':phone, 'address':address})
            print("회원가입이 완료되었습니다.")
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"회원가입 중 오류 발생 : {e})")
            return

    def log_in(self):
        try:
            hash_obj = hashlib.sha256()
            id = input("\n" + "ID 입력: ")
            pswd = input("비밀번호 입력: ")
            hash_obj.update(pswd.encode())
            ps = hash_obj.hexdigest()
            sql = "select password from users where user_ID = :id"
            self.cursor.execute(sql, {'id':id})
            row = self.cursor.fetchone()
            if row is None:
                print("\n" + "존재하지 않는 아이디입니다.")
                return
            elif row[0] == ps:
                role = self.admin(id)
                print("\n" + role + " 로그인 성공!")
                return id, role
                
            else:
                print("\n" + "비밀번호가 틀렸습니다.")
                return
            
        except Exception as e:
            print(f"로그인 중 오류발생 : {e}")