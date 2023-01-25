import sqlite3

# define connection and cursor
connection = sqlite3.connect(r'Employee Management/employee_info_db.db')

cursor = connection.cursor()

# # create stores table

# command1 = """CREATE TABLE IF NOT EXISTS admin_auth
# (Username VARCHAR, Password VARCHAR)"""
# cursor.execute(command1)


# command2 = """CREATE TABLE IF NOT EXISTS employee_info
# (employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
#  employee_name VARCHAR,
#  gender VARCHAR,
#  email VARCHAR,
#  address VARCHAR,
#  academic_qualification VARCHAR,
#  Username VARCHAR,
#  Password VARCHAR)"""
# cursor.execute(command2)

# cursor.execute(
#     "INSERT INTO employee_info VALUES (Null, 'Muhammad Irfan', 'Male', 'irfantijanie1@gmail.com', 'no.43 Taman', 'bachelor', 'irfantijanie1', '123')")


cursor.execute(
    "SELECT * FROM employee_info;")

results = cursor.fetchall()
print(results)
connection.commit()
cursor.close()
connection.close()
