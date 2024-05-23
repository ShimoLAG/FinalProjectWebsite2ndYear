from flask import Blueprint, render_template, redirect, url_for
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import MySQLdb.cursors
from . import mysql


#importing Blueprint just means this .py has a bunch or urls defined in here


views = Blueprint('views', __name__) #defining a blueprint


#ROUTES FOR POSTING DATA/INSERTING ITEMS AND UPDATING THE HTML

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
        accountID = current_user.accountID

        days = (datetime.strptime(endDate, '%Y-%m-%d') - datetime.strptime(startDate, '%Y-%m-%d')).days

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO travel (accountID, travelName, startDate, endDate, days, travelDescription) VALUES (%s, %s, %s, %s, %s, %s)", (accountID, travelName, startDate, endDate, days, travelDescription))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('views.travel'))

    accountID = current_user.accountID
    account_travel = get_travel(accountID)

    return render_template('travel.html', travel=account_travel)



@views.route('/itinerary/<int:travelID>', methods=['GET', 'POST'])
@login_required
def itinerary(travelID):
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
        itineraryDay = request.form.get('itineraryDay')
        itineraryDescription = request.form.get('itineraryDescription')
        itineraryName = request.form.get('itineraryName')
        
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO itineraries (itineraryDay, itineraryName, itineraryDescription, travelID) VALUES (%s, %s, %s, %s)", 
            (itineraryDay, itineraryName, itineraryDescription, travelID)
        )
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to the same page to avoid resubmission on page refresh
        return redirect(url_for('views.itinerary', travelID=travelID))

    # Fetch itinerary data for the given travelID and render the template
    itineraries_and_travel = get_itineraries_and_travel_name(travelID)
    
    return render_template('itinerary.html', itineraries=itineraries_and_travel, travelID=travelID)





@views.route('/destinations/<int:itineraryID>', methods=['GET', 'POST'])
@login_required
def destinations(itineraryID):
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
        return redirect(url_for('views.destinations', itineraryID=itineraryID))

    # Fetch destination data for the given itineraryID and render the template
    if current_user.is_authenticated:
        destinations = get_destinations(itineraryID)
        return render_template("destinations.html", destinations=destinations, itineraryID=itineraryID)
    else:
        flash("Not logged in", category='error')
        return redirect(url_for('auth.login'))  # Redirect to login page



@views.route('/activities/<int:destinationID>', methods=['GET', 'POST'])
@login_required
def activities(destinationID):
    
    def get_activities(destinationID):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT activityID, activityName, activityDescription, timeFrom, timeTo, address, destinationID FROM activities WHERE destinationID = %s', (destinationID,))
        activities = cursor.fetchall()
        cursor.close()
        return activities
    
    if request.method == 'POST':
        activityName = request.form['activityName']
        timeFrom = request.form['timeFrom']
        timeTo = request.form['timeTo']
        address = request.form['address']
        activityDescription= request.form['activityDescription']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO activities (activityName, timeFrom, timeTo, address, activityDescription, destinationID) VALUES (%s, %s, %s, %s, %s, %s)", (activityName, timeFrom, timeTo, address, activityDescription, destinationID))
        mysql.connection.commit()
        cursor.close()
        
        # Redirect to the same page to avoid resubmission on page refresh
        return redirect(url_for('views.activities', destinationID=destinationID))
    
    # Fetch activity data for the given destinationID and render the template
    if current_user.is_authenticated:
        activities = get_activities(destinationID)
        return render_template("activities.html", activities=activities, destinationID=destinationID)
    else:
        flash("Not logged in", category='error')
        return redirect(url_for('auth.login'))  # Redirect to login page




#ROUTES FOR UPDATING THE DATA

@views.route('/travelUpdate', methods=['POST'])
@login_required
def travelUpdate():
    if request.method == 'POST':
        travelID = request.form['travelID']
        travelName = request.form['travelName']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        travelDescription = request.form['travelDescription']

        # Calculate the number of days
        days = (datetime.strptime(endDate, '%Y-%m-%d') - datetime.strptime(startDate, '%Y-%m-%d')).days
        
        cur = mysql.connection.cursor()
        cur.execute('''
                    UPDATE travel
                    SET travelName = %s, startDate = %s, endDate = %s, days = %s, travelDescription = %s
                    WHERE travelID = %s
                    ''', (travelName, startDate, endDate, days, travelDescription, travelID))
        mysql.connection.commit()
        cur.close()

        flash("Data updated successfully", category="success")
        return redirect(url_for('views.travel'))
    

@views.route('/itineraryUpdate', methods=['POST'])
@login_required
def itineraryUpdate():
    print("Route accessed")  # Debug: Check if route is accessed

    if request.method == 'POST':
        itineraryID = request.form['itineraryID']
        travelID = request.form['travelID']  # Added travelID to use in redirection
        itineraryDay = request.form['itineraryDay']
        itineraryDescription = request.form['itineraryDescription']
        itineraryName = request.form['itineraryName']


        try:
            # Update itinerary in the database
            cur = mysql.connection.cursor()
            cur.execute('''
                        UPDATE itineraries
                        SET itineraryDay = %s, itineraryName = %s, itineraryDescription = %s
                        WHERE itineraryID = %s
                        ''', ( itineraryDay, itineraryName,  itineraryDescription, itineraryID))
            mysql.connection.commit()
            cur.close()

            flash("Data updated successfully", category="success")
        except Exception as e:
            mysql.connection.rollback()
            flash(f"An error occurred: {e}", category="error")
        finally:
            return redirect(url_for('views.itinerary', travelID=travelID))
    

@views.route('/destinationsUpdate', methods=['POST'])
@login_required
def destinationsUpdate():
    if request.method == 'POST':
        itineraryID = request.form.get('itineraryID')
        destinationID = request.form['destinationID']  # Added to fetch destinationID
        zipcode = request.form['zipcode']
        destinationName = request.form['destinationName']
        cityName = request.form['cityName']
        regionName = request.form['regionName']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                        UPDATE destinations
                        SET zipcode = %s, destinationName = %s, cityName = %s, regionName = %s
                        WHERE destinationID = %s
                        ''', (zipcode, destinationName, cityName, regionName, destinationID))
            mysql.connection.commit()
            cur.close()

            flash("Data updated successfully", category="success")
        except Exception as e:
            mysql.connection.rollback()
            flash(f"An error occurred: {e}", category="error")
        finally:
           return redirect(url_for('views.destinations', itineraryID=itineraryID))
        
@views.route('/activityUpdate', methods=['POST'])
@login_required
def activityUpdate():
    if request.method == 'POST':
        destinationID = request.form.get('destinationID')
        activityID = request.form.get('activityID')  # Added to fetch destinationID
        activityName = request.form['activityName']
        timeFrom = request.form['timeFrom']
        timeTo = request.form['timeTo']
        activityDescription = request.form['activityDescription']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                        UPDATE activities
                        SET activityName = %s, timeFrom = %s, timeTo = %s, activityDescription = %s
                        WHERE activityID = %s
                        ''', (activityName, timeFrom, timeTo, activityDescription, activityID))
            mysql.connection.commit()
            cur.close()

            flash("Data updated successfully", category="success")
        except Exception as e:
            mysql.connection.rollback()
            flash(f"An error occurred: {e}", category="error")
        finally:
           return redirect(url_for('views.activities', destinationID=destinationID))
        

#DELETE


@views.route('/travelDelete/<int:travelID>', methods = ['GET'])
def travelDelete(travelID):
    flash("deleted succesfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM travel WHERE travelID=%s", (travelID,))
    mysql.connection.commit()
    return redirect(url_for('views.travel'))

@views.route('/itineraryDelete/<int:itineraryID>', methods=['GET'])
@login_required
def itineraryDelete(itineraryID):
    flash("Deleted successfully")
    cur = mysql.connection.cursor()
    
    # Attempt to fetch the travelID associated with the given itineraryID
    cur.execute("SELECT travelID FROM itineraries WHERE itineraryID=%s", (itineraryID,))
    result = cur.fetchone()
    
    if result:
        travelID = result[0]  # Extract travelID from the query result
        cur.execute("DELETE FROM itineraries WHERE itineraryID=%s", (itineraryID,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('views.itinerary', travelID=travelID))
    else:
        # Handle the case where no travelID is found for the given itineraryID
        flash("Itinerary not found or already deleted.", category='error')
        cur.close()
        return redirect(url_for('views.itineraries'))  # Assuming you have a view for listing itineraries




@views.route('/destinationsDelete/<int:destinationID>', methods=['GET'])
@login_required
def destinationsDelete(destinationID):
    flash("Deleted successfully")
    cur = mysql.connection.cursor()
    
    # Attempt to fetch the itineraryID associated with the given destinationID
    cur.execute("SELECT itineraryID FROM destinations WHERE destinationID=%s", (destinationID,))
    result = cur.fetchone()
    
    if result:
        itineraryID = result[0]  # Extract itineraryID from the query result (using dictionary cursor)
        cur.execute("DELETE FROM destinations WHERE destinationID=%s", (destinationID,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('views.destinations', itineraryID=itineraryID))
    else:
        # Handle the case where no itineraryID is found for the given destinationID
        flash("Destination not found or already deleted.", category='error')
        cur.close()
        return redirect(url_for('views.destinations'))  # Assuming you have a view for listing destinations
    
@views.route('/activitiesDelete/<int:activityID>', methods=['GET'])
@login_required
def activitiesDelete(activityID):
    flash("Deleted successfully")
    cur = mysql.connection.cursor()
    
    # Attempt to fetch the destinationID associated with the given activityID
    cur.execute("SELECT destinationID FROM activities WHERE activityID=%s", (activityID,))
    result = cur.fetchone()
    
    if result:
        destinationID = result[0]  # Extract destinationID from the query result
        cur.execute("DELETE FROM activities WHERE activityID=%s", (activityID,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('views.activities', destinationID=destinationID))
    else:
        # Handle the case where no destinationID is found for the given activityID
        flash("Activity not found or already deleted.", category='error')
        cur.close()
        return redirect(url_for('views.destinations'))  # Assuming you have a view for listing destinations



#SEARCH

@views.route('/travelSearch', methods=['POST'])
@login_required
def travelSearch():
    travelName = request.form['travelName']
    accountID = current_user.accountID
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM travel WHERE travelName LIKE %s AND accountID = %s", ('%' + travelName + '%', accountID))
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('travel.html', travel=data)







