from flask import Flask

def create_app():
    app = Flask(__name__) #initializes the application
    app.config['SECRET_KEY'] = 'secret key' #encrypts the cookies and session data related to website (dont worry bout it)

    from .views import views
    from .auth import auth


    #basically registers the url of the website
    app.register_blueprint(views, url_prefix = '/') #i will explain more in person what this does
    app.register_blueprint(auth, url_prefix = '/')


    return app
   