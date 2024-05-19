from flask import Blueprint, render_template, redirect, url_for
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import MySQLdb.cursors
from . import mysql


#importing Blueprint just means this .py has a bunch or urls defined in here


views = Blueprint('views', __name__) #defining a blueprint

@views.route('/', methods=['GET', 'POST'])
def landingpage():
    return render_template("landingpage.html", user = current_user)


@views.route('/home')
@login_required
def home():
    return render_template("home.html")

@views.route('/travel', methods=['GET', 'POST'])
@login_required
def travel():
    def get_account_id():
        if current_user.is_authenticated:
            return current_user.accountID
        else:
            return None
        
    def get_travel(accountID):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT travelID, travelName, startDate, endDate, DATEDIFF(endDate, startDate) AS days, travelDescription FROM travel WHERE accountID = %s', (accountID,))
        travel = cursor.fetchall()
        cursor.close()
        return travel
    
    if request.method == 'POST':
        travelName = request.form['travelName']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        travelDescription = request.form['travelDescription']
        accountID = get_account_id()
        if accountID is None:
            flash("Not logged in", category='error')
            return redirect(url_for('auth.login'))  # Redirect to login page
        

        days = (datetime.strptime(endDate, '%Y-%m-%d') - datetime.strptime(startDate, '%Y-%m-%d')).days
            
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO travel (accountID, travelName, startDate, endDate, days, travelDescription) VALUES (%s, %s, %s, %s, %s, %s)", (accountID, travelName, startDate, endDate, days, travelDescription))
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to the same page to avoid resubmission on page refresh
        return redirect(url_for('views.travel'))

    # Fetch travel data for the current user and render the template
    accountID = get_account_id()
    if accountID is None:
        flash("Not logged in", category='error')
        return redirect(url_for('auth.login'))  # Redirect to login page
    
    account_travel = get_travel(accountID)
    
    return render_template('travel.html', travel=account_travel)



@views.route('/itinerary/<int:travelID>', methods=['GET', 'POST'])
@login_required
def itinerary(travelID):
    def get_account_id():
        if current_user.is_authenticated:
            return current_user.accountID
        else:
            return None
    
    def get_itineraries(travelID):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT itineraryID, itineraryDay, itineraryName, itineraryDescription, travelID FROM itineraries WHERE travelID = %s', (travelID,))
        itineraries = cursor.fetchall()
        cursor.close()
        return itineraries

    if request.method == 'POST':
        itineraryDay = request.form['itineraryDay']
        itineraryDescription = request.form['itineraryDescription']
        itineraryName = request.form['itineraryName']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO itineraries (itineraryDay, itineraryName, itineraryDescription, travelID) VALUES (%s, %s, %s, %s)", (itineraryDay, itineraryName, itineraryDescription, travelID))
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to the same page to avoid resubmission on page refresh
        return redirect(url_for('views.itinerary', travelID=travelID))

    # Fetch itinerary data for the given travelID and render the template
    accountID = get_account_id()
    if accountID is None:
        flash("Not logged in", category='error')
        return redirect(url_for('auth.login'))  # Redirect to login page
    
    itineraries = get_itineraries(travelID)
    
    return render_template('itinerary.html', itineraries=itineraries, travelID=travelID)


@views.route('/destinations')
@login_required
def destinations():
    return render_template("destinations.html")

@views.route('/activities')
@login_required
def activities():
    return render_template("activities.html")