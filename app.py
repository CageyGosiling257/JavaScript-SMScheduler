from flask import Flask, render_template
import flask
import smsGateway
import pytz
import json
import logging

timezone = pytz.timezone('US/Eastern')
# Sets logging of flask file to debug so it can see
logging.basicConfig(level=logging.DEBUG)

# Creates flask app to allow communication between website and Backend logic
app = Flask(__name__, static_url_path='/static')

totalData = [] # Stores a list of dictionaries user created reminders

# Sends reminder information to smsGateway.py file to send out text messages
def callSMSGateway(dictionary):
    json_data = json.dumps(dictionary)
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
    app.logger.info('Form has been submitted!')
    if flask.request.method == 'POST':
        phone = flask.request.form['phoneNumber']
        message = flask.request.form['message']
        dateTime = flask.request.form['datetimeInput']
        interval = flask.request.form['interval']
        data = {"phone": phone, "message": message, "dateTime": dateTime, "interval":
                interval, "timesSent": 0}
        totalData.append(data)
        if(smsGateway.validateInputs(data)):
            app.logger.info("Reminder added to list!")
            callSMSGateway(data)
            return render_template("index.html")
        else :
            return render_template("index.html")

# Output app route that displays information relating to the reminders that user has created
@app.route('/get_table_data')
def display_table():
    global totalData
    tempData = totalData
    app.logger.info('Reminder metadata sentout.')
    return tempData

# Runs the program when the file is ran.
if __name__ == '__main__':   
    app.run(debug=True)

