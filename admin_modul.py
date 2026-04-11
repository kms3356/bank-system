from tabulate import tabulate

def in_put():
    print('\n' + tabulate([["1", "전체 사용자 조회"], ["2", "사용자 정보 수정"], ["3", "사용자 정보 삭제"], ["q", "로그아웃"]], headers=["번호", "관리자 메뉴"], tablefmt="rounded_grid"))
    return(input("선택 : "))

def user_inquiry(cursor):
    try:
        sql = "select * from users"
        cursor.execute(sql)
        rows = cursor.fetchall()
        header = ["user_id", "password", "name", "phone", "address", "role"]
        print(tabulate(rows, headers=header, tablefmt="fancy_grid"))
    except Exception as e:
        print(f"사용자 조회 중 오류 발생 : {e}")

def ch_user(cursor,conn):
    try:
        id = input("\n수정할 유저 ID : ")
        ch_menu = ['name','phone', 'address', 'role']
        while True:
            cul = input("수정할 항목 : ")
            if cul in ch_menu: break
            else:
                print("수정할 수 없는 항목입니다.")
                continue
    
        value = input("수정할 내용 : ")
        sql = f"update users set {cul} = :1 where user_id = :2"
        cursor.execute(sql, [value, id])
        if cursor.rowcount == 0:
            print("ID확인이 필요합니다.")
            return
        else:
            conn.commit()
            print("사용자 정보 수정에 성공했습니다.")
    except Exception as e:
        print(f"사용자정보 수정 중 오류 발생 : {e}")
        conn.rollback()

def del_user(cursor,conn):
    id = input("\n삭제할 유저 ID : ")
    try:
        sql = "delete from log where userid = :1"
        cursor.execute(sql, [id])
        if cursor.rowcount == 0:
            print("ID확인이 필요합니다.")
            return

    except Exception as e:
        print(f"로그 삭제 중 오류 발생 : {e}")
        conn.rollback()
        return

    try:
        sql = "delete from accounts where userid = :1"
        cursor.execute(sql, [id])

    except Exception as e:
        print(f"계좌 삭제 중 오류 발생 : {e}")
        conn.rollback()
        return
    
    try:
        sql = "delete from users where user_id = :1"
        cursor.execute(sql, [id])

    except Exception as e:
        print(f"유저 삭제 중 오류 발생 : {e}")
        conn.rollback()
        return
    
    conn.commit()
    print(f"{id}유저 삭제에 성공했습니다.")