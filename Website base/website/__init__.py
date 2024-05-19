from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
import MySQLdb.cursors
from .models import users

mysql = MySQL()
User = users
def create_app():
    app = Flask(__name__) #initializes the application
    app.config['SECRET_KEY'] = 'secret key' #encrypts the cookies and session data related to website (dont worry bout it)
    
   
    app.config['MYSQL_HOST'] = "localhost"
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = "root"
    app.config['MYSQL_DB'] = "Itinerary"

    mysql.init_app(app)

    from .views import views 
    from .auth import auth


    #basically registers the url of the website
    app.register_blueprint(views, url_prefix = '/') #i will explain more in person what this does
    app.register_blueprint(auth, url_prefix = '/')



    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE accountID = %s", (user_id,))
        users = cursor.fetchone()
        if users:
            return User(users[0], users[1], users[2], users[3], users[4], users[5], users[6], users[7], users[8])
        return None


    return app
   