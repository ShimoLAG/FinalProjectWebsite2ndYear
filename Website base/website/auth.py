from flask import Blueprint, render_template,request,flash,redirect,url_for,session
from flask_mysqldb import MySQL
from flask_login import login_user, login_required, logout_user, current_user
import mysql.connector
from . import mysql
from .models import users

#importing Blueprint just means this .py has a bunch or urls defined in here

User = users

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST']) #this is how we make a route to and when we go to this url it runs the function below it
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']


        cursor =mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email,password))
        users = cursor.fetchone()

        if users and password == users[8]:
            user = User(users[0], users[1], users[2], users[3],
                        users[4], users[5], users[6], users[7],
                        users[8])
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('incorrect username/password', category='error')

    return render_template('login.html', users=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        Dyear = request.form['Dyear']
        month = request.form['month']
        day = request.form['day']
        sex = request.form['sex']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        cursor = mysql.connection.cursor()
        cursor.execute(" SELECT * FROM users WHERE email=%s ", (email,)) 
        users = cursor.fetchone()

        if users:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            cursor.execute("INSERT INTO users (firstName,lastName,Dyear,month,day,sex,email,password) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (firstName,lastName,Dyear,month,day,sex,email,password))
            cursor.connection.commit()

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            
            new_users = cursor.fetchone()
            new_user = User(new_users[0], new_users[1], new_users[2], new_users[3],
                            new_users[4], new_users[5], new_users[6], new_users[7],
                            new_users[8])
            flash('Account Created', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
            
    
    return render_template('signup.html', users = current_user)