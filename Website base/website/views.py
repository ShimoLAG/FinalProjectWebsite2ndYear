from flask import Blueprint, render_template
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user


#importing Blueprint just means this .py has a bunch or urls defined in here


views = Blueprint('views', __name__) #defining a blueprint

@views.route('/', methods=['GET', 'POST'])
def landingpage():
    return render_template("landingpage.html", user = current_user)


@views.route('/home')
@login_required
def home():
    return render_template("home.html")

@views.route('/travel')
@login_required
def travel():
    return render_template("travel.html")

@views.route('/itinerary')
@login_required
def itinerary():
    return render_template("itinerary.html")

@views.route('/destinations')
@login_required
def destinations():
    return render_template("destinations.html")

@views.route('/activities')
@login_required
def activities():
    return render_template("activities.html")