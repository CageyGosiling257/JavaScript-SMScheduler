from flask import Flask, render_template, redirect, url_for, request, Request
import flask
import smsGateway
import pytz
import json
import logging
import os


currentFilePath = os.path.abspath(__file__) # Creates filepath for current file
currentDirectory = os.path.dirname(currentFilePath) # Finds directory of the current file 
staticFolder = os.path.join(currentDirectory,'..', 'static') # Finds path to static folder
templateFolder = os.path.join(currentDirectory,'..', 'templates') # Finds path to the templates folder
threadIsRunning = False # Sets flag to not create new thread to false at start of program
timezone = pytz.timezone('US/Eastern')
# Sets logging of flask file to debug so it can see
logging.basicConfig(level=logging.DEBUG)

# Creates flask app to allow communication between website and Backend logic
app = Flask(__name__, template_folder=templateFolder, 
            static_folder=staticFolder, static_url_path='/static')

totalData = [] # Stores a list of dictionaries user created reminders

# Sends reminder information to smsGateway.py file to send out text messages
def callSMSGateway(dict):
    json_data = json.dumps(dict)
    smsGateway.startProgram(json=json_data)
    

# Beginning app route that shows the original index.html file
@app.route('/')
def index():
    return render_template('index.html')

# App route that occurs when the user clicks the submit button.  This starts processing
# the reminder data that the user has inputted through the submit button.
@app.route('/submit', methods=['POST'])
def submit():
    global totalData
    global threadIsRunning
    app.logger.info('Form has been submitted!')
    if flask.request.method == 'POST':
        phone = flask.request.form['phoneNumber']
        message = flask.request.form['message']
        dateTime = flask.request.form['datetimeInput']
        interval = flask.request.form['interval']
        data = {"phone": phone, "message": message, "dateTime": dateTime, "interval":
                interval, "timesSent": 0}
        totalData.append(data)
        app.logger.info('The other python program has begun!')
        callSMSGateway(data)
        return render_template("index.html")

# Output app route that displays information relating to the reminders that user has created
@app.route('/get_table_data')
def display_table():
    global totalData
    tempData = totalData
    app.logger.info('The table with the information has been loaded...')
    return tempData

# Runs the program when the file is ran.
if __name__ == '__main__':   
    app.run(debug=False)

