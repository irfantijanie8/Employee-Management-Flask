import sqlite3


def dbConnect():
    conn = sqlite3.connect(r'Employee Management/employee_info_db.db')
    return conn


def printEmp():
    # conn = dbConnect()
    # cur = conn.cursor
    connection = dbConnect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM admin_auth")
    results = cursor.fetchall()
    print(results)
    connection.commit()
    cursor.close()
    connection.close()


def home():
    try:
        conn = dbConnect()
        print("success")
    except:
        print("fail")
    finally:
        conn.close


if __name__ == '__main__':
    printEmp()
