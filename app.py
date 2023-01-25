from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import Form, FlaskForm
from wtforms import StringField, RadioField, EmailField, SelectField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import ValidationError, DataRequired

import sqlite3
app = Flask(__name__)
app.secret_key = "__privatekey__"


class GetRegistrationForm(FlaskForm):
    name = StringField(label="employee name", validators=[DataRequired()])
    gender = RadioField(label='Gender', choices=[
                        'Male', 'Female'], validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired()])
    address = TextAreaField(label="Address", validators=[DataRequired()])
    academic = SelectField(label="Academic", choices=[(
        'bachelor', 'Bachelor'), ('master', 'Master'), ('phd', 'PHD')], validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class GetLogin(FlaskForm):
    username = StringField(label="Username", validators=[
                           DataRequired()], render_kw={"placeholder": "username"})
    password = PasswordField(label="Password", validators=[
                             DataRequired()], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")


def dbConnect():
    conn = sqlite3.connect(r'Employee Management/employee_info_db.db')
    return conn


@app.route('/')
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


@app.route('/login', methods=['POST', 'GET'])
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
                    f"SELECT * FROM employee_info where Username='{usernameLogin}' AND Password={passwordLogin};")
                if cursor.fetchone() == None:
                    return "not success"
                # employee login
                else:
                    return "Employee success"

            # admin login
            else:
                return "admin success"
            connection.commit()
            cursor.close()
            connection.close()
            # return redirect(url_for('successSubmission', form=getRegistrationForm))

            return passwordLogin
    elif request.method == 'GET':
        return render_template('login.html', form=getLoginForm)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    getRegistrationForm = GetRegistrationForm()
    if request.method == 'POST':
        if getRegistrationForm.validate() == "False":
            flash("please fill out this field")
            return render_template('signup.html', form=getRegistrationForm)
        else:
            return redirect(url_for('empDash'))
            # return getRegistrationForm.username.data
    elif request.method == 'GET':
        return render_template('signup.html', form=getRegistrationForm)


@app.route('/adminDashboard')
def adminDash():
    return "admin Dashboard"


@app.route('/employeeDashboard')
def empDash():
    return "Employee Dashboard"

# @ app.route('/success')
# def successSubmission(form):
#     # getRegistrationForm = GetRegistrationForm()
#     # return getRegistrationForm.username.data
#     return form.username.data


# def __init__(self):
#     con = sqlite3.connect('employee_info_db.db')
#     c = con.cursor


if __name__ == '__main__':
    app.run(debug=True)
