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
    
    def get_itineraries_and_travel_name(travelID):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT i.itineraryID, i.itineraryDay, i.itineraryName, i.itineraryDescription, i.travelID, t.travelName 
            FROM itineraries i
            JOIN travel t ON i.travelID = t.travelID
            WHERE i.travelID = %s
        ''', (travelID,))
        data = cursor.fetchall()
        cursor.close()
        return data

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
    
    itineraries_and_travel = get_itineraries_and_travel_name(travelID)
    
    return render_template('itinerary.html', itineraries=itineraries_and_travel, travelID=travelID)



@views.route('/destinations/<int:itineraryID>', methods=['GET', 'POST'])
@login_required
def destinations(itineraryID):  # Ensure itineraryID is passed as a parameter
    def get_account_id():
        if current_user.is_authenticated:
            return current_user.accountID
        else:
            return None
    
    def get_destinations(itineraryID):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT destinationID, zipcode, destinationName, cityName, regionName, itineraryID FROM destinations WHERE itineraryID = %s', (itineraryID,))
        destinations = cursor.fetchall()
        cursor.close()
        return destinations
    
    if request.method == 'POST':
        zipcode = request.form['zipcode']
        destinationName = request.form['destinationName']
        cityName = request.form['cityName']
        regionName = request.form['regionName']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO destinations (zipcode, destinationName, cityName, regionName, itineraryID) VALUES (%s, %s, %s, %s, %s)", (zipcode, destinationName, cityName, regionName, itineraryID))
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to the same page to avoid resubmission on page refresh
        return redirect(url_for('views.destinations', itineraryID=itineraryID))  # Corrected url_for destination

    # Fetch destination data for the given itineraryID and render the template
    accountID = get_account_id()
    if accountID is None:
        flash("Not logged in", category='error')
        return redirect(url_for('auth.login'))  # Redirect to login page
    
    destinations = get_destinations(itineraryID)
    
    return render_template("destinations.html", destinations=destinations, itineraryID=itineraryID)


@views.route('/activities/<int:destinationID>', methods=['GET', 'POST'])
@login_required
def activities(destinationID):
    """
    Define a Flask view to handle GET and POST requests for activities associated with a specific destination identified by destinationID.
    """
    def get_account_id():
        """
        Helper function to retrieve the account ID of the current logged-in user.
        """
        if current_user.is_authenticated:
            return current_user.accountID
        else:
            return None
    
    def get_activities(destinationID):
        """
        Function to fetch activities associated with the given destinationID from the database.
        """
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT activityID, activityName, activityDescription, timeFrom, timeTo, address, activitySequence, destinationID FROM activities WHERE destinationID = %s', (destinationID,))
        activities = cursor.fetchall()
        cursor.close()
        return activities
    
    if request.method == 'POST':
        """
        Handling POST requests to add new activities associated with the destination.
        """
        activityName = request.form['activityName']
        timeFrom = request.form['timeFrom']
        timeTo = request.form['timeTo']
        address = request.form['address']
        activityDescription= request.form['activityDescription']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT IFNULL(MAX(activitySequence), 0) + 1 FROM activities WHERE destinationID = %s", (destinationID,))
        activitySequence = cursor.fetchone()[0]

        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO activities (activityName, timeFrom, timeTo, address, activityDescription, destinationID, activitySequence) VALUES (%s, %s, %s, %s, %s, %s, %s)", (activityName, timeFrom, timeTo, address, activityDescription, destinationID, activitySequence))
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to the same page to avoid resubmission on page refresh
        return redirect(url_for('views.activities', destinationID=destinationID))
    
    # Fetch activity data for the given destinationID and render the template
    accountID = get_account_id()
    if accountID is None:
        flash("Not logged in", category='error')
        return redirect(url_for('auth.login'))  # Redirect to login page
    
    activities = get_activities(destinationID)
    
    return render_template("activities.html", activities=activities, destinationID=destinationID)
