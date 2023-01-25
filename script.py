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

name1 = "Al-Ahmad"
gender1 = "Male"
email1 = "irfantijanie2@gmail.com"
address1 = "no.43 Taman"
academic1 = "bachelor"
username1 = "irfantijanie1"
password1 = "123"
id1 = 1

cursor.execute(
    f"Update employee_info SET employee_name = '{name1}', gender = '{gender1}', email = '{email1}', address = '{address1}', Academic_qualification = '{academic1}', Username = '{username1}', Password = '{password1}' WHERE employee_ID = '{id1}';")

cursor.execute(
    "SELECT * FROM employee_info;")

results = cursor.fetchall()
print(results)
connection.commit()
cursor.close()
connection.close()
