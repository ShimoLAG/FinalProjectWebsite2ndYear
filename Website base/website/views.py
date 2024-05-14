from flask import Blueprint, render_template

#importing Blueprint just means this .py has a bunch or urls defined in here


views = Blueprint('views', __name__) #defining a blueprint

@views.route('/')  #this is how we make a route to and when we go to this url it runs the function below it
def landingpage():
    return render_template("landingpage.html")


@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/travel')
def travel():
    return render_template("travel.html")

@views.route('/itinerary')
def itinerary():
    return render_template("itinerary.html")

@views.route('/destinations')
def destinations():
    return render_template("destinations.html")

@views.route('/activities')
def activities():
    return render_template("activities.html")