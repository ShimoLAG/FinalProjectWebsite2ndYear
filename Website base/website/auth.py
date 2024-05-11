from flask import Blueprint, render_template

#importing Blueprint just means this .py has a bunch or urls defined in here


auth = Blueprint('auth', __name__)

@auth.route('/login') #this is how we make a route to and when we go to this url it runs the function below it
def login():
    return render_template('login.html')

@auth.route('/logout')
def logout():
    pass

@auth.route('/signup')
def signup():
    return render_template('signup.html')