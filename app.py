import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form, FlaskForm
from wtforms import StringField, RadioField, EmailField, SelectField, PasswordField, IntegerField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import ValidationError, DataRequired
from flask_restful import Resource, Api
import json
import requests

app = Flask(__name__)
api = Api(app)
app.secret_key = "__privatekey__"


class GetRegistrationForm(FlaskForm):
    name = StringField(label="employee name", validators=[
        DataRequired()], render_kw={"placeholder": "Name"})
    gender = RadioField(label='Gender', choices=[
        'Male', 'Female'], validators=[DataRequired()])
    email = EmailField(label="Email", validators=[
        DataRequired()], render_kw={"placeholder": "Email"})
    address = TextAreaField(label="Address", validators=[
        DataRequired()], render_kw={"placeholder": "Address"})
    academic = SelectField(label="Academic", choices=[(
        'bachelor', 'Bachelor'), ('master', 'Master'), ('phd', 'PHD')], validators=[DataRequired()])
    username = StringField(label="Username", validators=[
        DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(label="Password", validators=[
        DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Submit")


class UpdateForm(FlaskForm):
    empInfo = ("", "", "", "", "", "", "", "")

    name = StringField(label="employee name", validators=[
        DataRequired()], render_kw={"placeholder": f"{empInfo[1]}"})
    gender = RadioField(label='Gender', choices=[
        'Male', 'Female'], default=f"{empInfo[2]}", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[
        DataRequired()], render_kw={"placeholder": f"{empInfo[3]}"})
    address = TextAreaField(label="Address", validators=[
        DataRequired()], render_kw={"placeholder": f"{empInfo[4]}"})
    academic = SelectField(label="Academic", choices=[(
        'bachelor', 'Bachelor'), ('master', 'Master'), ('phd', 'PHD')], default=f"{empInfo[5]}", validators=[DataRequired()])
    username = StringField(label="Username", validators=[
        DataRequired()], render_kw={"placeholder": f"{empInfo[6]}"})
    password = PasswordField(label="Password", validators=[
        DataRequired()], render_kw={"placeholder": f"{empInfo[7]}"})
    empID = HiddenField()
    submit = SubmitField("Submit")


class GetLogin(FlaskForm):
    username = StringField(label="Username", validators=[
        DataRequired()], render_kw={"placeholder": "username"})
    password = PasswordField(label="Password", validators=[
        DataRequired()], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")


class search(FlaskForm):
    employeeId = IntegerField(label="Employee ID", validators=[
        DataRequired()], render_kw={"placeholder": "Enter Employee ID"})
    submit = SubmitField("Search")


def dbConnect():
    conn = sqlite3.connect(r'Employee Management/employee_info_db.db')
    return conn


def getIdInfo(empID):
    conn = sqlite3.connect(
        r'Employee Management/employee_info_db.db')
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cur.execute(f"SELECT * FROM employee_info where employee_id='{empID}'")
    result = cur.fetchone()
    return result


def getId(username):
    conn = sqlite3.connect(
        r'Employee Management/employee_info_db.db')
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cur.execute(f"SELECT * FROM employee_info where Username='{username}'")
    result = cur.fetchone()
    return result[0]


@ app.route('/')
def home():
    try:
        conn = dbConnect()
        return render_template('home.html')
    except:
        return "Connection Failed"
    finally:
        try:
            conn.close
        except:
            return "Connection Failed"


@ app.route('/login', methods=['POST', 'GET'])
def login():
    getLoginForm = GetLogin()
    if request.method == 'POST':
        if getLoginForm.validate() == "False":
            flash("please fill out this field")
            return render_template('login.html', form=getLoginForm)
        else:
            usernameLogin = getLoginForm.username.data
            passwordLogin = getLoginForm.password.data
            connection = sqlite3.connect(
                r'Employee Management/employee_info_db.db')
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT * FROM admin_auth where Username='{usernameLogin}' AND Password='{passwordLogin}';")
            if cursor.fetchone() == None:
                cursor.execute(
                    f"SELECT * FROM employee_info where Username='{usernameLogin}' AND Password='{passwordLogin}';")

                # invalid login
                if cursor.fetchone() == None:
                    cursor.close()
                    connection.close()
                    flash("Invalid Username or Password")
                    return render_template('login.html', form=getLoginForm)
                # employee login
                else:
                    cursor.close()
                    connection.close()
                    return redirect(url_for('dashboard', userUsername=usernameLogin))

            # admin login
            else:
                cursor.close()
                connection.close()
                return redirect(url_for('dashboard', userUsername=usernameLogin))

            cursor.close()
            connection.close()
            # return redirect(url_for('successSubmission', form=getRegistrationForm))

            return passwordLogin
    elif request.method == 'GET':
        return render_template('login.html', form=getLoginForm)


@ app.route('/signup', methods=['POST', 'GET'])
def signup():
    getRegistrationForm = GetRegistrationForm()
    if request.method == 'POST':
        if getRegistrationForm.validate() == "False":
            flash("please fill out this field")
            return render_template('signup.html', form=getRegistrationForm)
        else:
            connection = sqlite3.connect(
                r'Employee Management/employee_info_db.db')
            cursor = connection.cursor()

            name1 = getRegistrationForm.name.data
            gender1 = getRegistrationForm.gender.data
            email1 = getRegistrationForm.email.data
            address1 = getRegistrationForm.address.data
            academic1 = getRegistrationForm.academic.data
            username1 = getRegistrationForm.username.data
            password1 = getRegistrationForm.password.data

            cursor.execute(
                f"SELECT * FROM employee_info where Username='{username1}';")
            # if username don't exist

            if cursor.fetchone() == None:
                cursor.execute(
                    f"INSERT INTO employee_info VALUES (Null, '{name1}', '{gender1}', '{email1}', '{address1}', '{academic1}', '{username1}', '{password1}')")
            else:
                cursor.close()
                connection.close()
                flash("Username has been taken")
                return render_template('signup.html', form=getRegistrationForm)

            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('dashboard', userUsername=username1))
            # return getRegistrationForm.username.data
    elif request.method == 'GET':
        return render_template('signup.html', form=getRegistrationForm)


@ app.route('/adminDashboard')
def dashboard():
    try:
        userUsername = request.args['userUsername']
    except:
        return "please login"
    connection = sqlite3.connect(
        r'Employee Management/employee_info_db.db')
    cursor = connection.cursor()

    cursor.execute(
        f"SELECT * FROM admin_auth where Username='{userUsername}';")
    # admin dash
    if cursor.fetchone() != None:
        return render_template('adminDash.html', userUsername=userUsername, admin=True)
    else:
        cursor.execute(
            f"SELECT * FROM employee_info where Username='{userUsername}';")
        # if employee
        empID = getId(userUsername)
        if cursor.fetchone() != None:
            return render_template('adminDash.html', userUsername=userUsername, admin=False, empID=empID)
        else:
            return "please login"


class EmployeeInfo(Resource):
    def get(self):
        users = []
        try:
            conn = sqlite3.connect(
                r'Employee Management/employee_info_db.db')
            cur = conn.cursor()
            conn.row_factory = sqlite3.Row
            cur.execute("SELECT * FROM employee_info")
            rows = cur.fetchall()

            for i in rows:
                employee = {}
                employee["employee_id"] = i[0]
                employee["employee_name"] = i[1]
                employee["gender"] = i[2]
                employee["email"] = i[3]
                employee["address"] = i[4]
                employee["Academic_qualification"] = i[5]
                employee["Username"] = i[6]
                employee["Password"] = i[7]
                users.append(employee)
        except:
            users = []
        return json.dumps(users)


@ app.route('/search', methods=['POST', 'GET'])
def adminSearch():
    getEmpID = search()
    # response = requests.get("http://127.0.0.1:5000/api")

    if request.method == 'POST':
        if getEmpID.validate() == "False":
            flash("please fill out this field")
            return render_template('search.html', form=getEmpID)
        else:
            connection = sqlite3.connect(
                r'Employee Management/employee_info_db.db')
            cursor = connection.cursor()
            EMPID = getEmpID.employeeId.data
            cursor.execute(
                f"SELECT * FROM employee_info where employee_id='{EMPID}';")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result == None:
                flash("Employee ID doesn't exist")
                return render_template('search.html', form=getEmpID)
            else:
                return render_template('search.html', form=getEmpID, result=result)

    elif request.method == 'GET':
        response = requests.get("http://127.0.0.1:5000/api")
        response = response.json()
        response = json.loads(response)

        print(type(response))
        return render_template('search.html', form=getEmpID, response=response)


@ app.route('/add', methods=['POST', 'GET'])
def addEmployee():
    addEmployee = GetRegistrationForm()
    if request.method == 'POST':
        if addEmployee.validate() == "False":
            flash("please fill out this field")
            return render_template('addEmployee.html', form=addEmployee)
        else:
            connection = sqlite3.connect(
                r'Employee Management/employee_info_db.db')
            cursor = connection.cursor()

            name1 = addEmployee.name.data
            gender1 = addEmployee.gender.data
            email1 = addEmployee.email.data
            address1 = addEmployee.address.data
            academic1 = addEmployee.academic.data
            username1 = addEmployee.username.data
            password1 = addEmployee.password.data

            cursor.execute(
                f"SELECT * FROM employee_info where Username='{username1}';")
            # if username don't exist
            if cursor.fetchone() == None:
                cursor.execute(
                    f"INSERT INTO employee_info VALUES (Null, '{name1}', '{gender1}', '{email1}', '{address1}', '{academic1}', '{username1}', '{password1}')")
                connection.commit()
                cursor.close()
                connection.close()
            else:
                flash("Username has been taken")
                cursor.close()
                connection.close()
                return render_template('addEmployee.html', form=addEmployee)

            return redirect(url_for('dashboard'))
            # return getRegistrationForm.username.data
    elif request.method == 'GET':
        return render_template('addEmployee.html', form=addEmployee)


@ app.route('/view', methods=['GET', 'POST', 'DELETE'])
def view():
    updateEmployee = UpdateForm()

    if request.method == 'POST':
        if updateEmployee.validate() == "False":
            flash("please fill out this field")
            return render_template('view.html', form=updateEmployee)
        else:
            connection = sqlite3.connect(
                r'Employee Management/employee_info_db.db')
            cursor = connection.cursor()

            id1 = updateEmployee.empID.data
            name1 = updateEmployee.name.data
            gender1 = updateEmployee.gender.data
            email1 = updateEmployee.email.data
            address1 = updateEmployee.address.data
            academic1 = updateEmployee.academic.data
            username1 = updateEmployee.username.data
            password1 = updateEmployee.password.data

            cursor.execute(
                f"Update employee_info SET employee_name = '{name1}', gender = '{gender1}', email = '{email1}', address = '{address1}', Academic_qualification = '{academic1}', Username = '{username1}', Password = '{password1}' WHERE employee_ID = '{id1}';")
            connection.commit()
            return redirect(url_for('dashboard', userUsername=username1))

    elif request.method == 'GET':
        empID = request.args['empID']
        info = getIdInfo(empID)
        updateEmployee.empInfo = info
        updateEmployee.empID.data = info[0]
        updateEmployee.name.data = info[1]
        updateEmployee.gender.data = info[2]
        updateEmployee.email.data = info[3]
        updateEmployee.address.data = info[4]
        updateEmployee.academic.data = info[5]
        updateEmployee.username.data = info[6]
        updateEmployee.password.data = info[7]
        return render_template('view.html', form=updateEmployee)

        # @ app.route('/success')
        # def successSubmission(form):
        #     # getRegistrationForm = GetRegistrationForm()
        #     # return getRegistrationForm.username.data
        #     return form.userna.data

        # def __init__(self):
        #     con = sqlite3.connect('employee_info_db.db')
        #     c = con.cursor
api.add_resource(EmployeeInfo, '/api')
app.run

if __name__ == '__main__':
    app.run(debug=True)
