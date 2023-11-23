from flask import Flask, render_template, redirect, url_for, Request
import flask
import smsGateway
import subprocess
import json
from data_queue import data_queue
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__, template_folder='/home/dfreeman/Desktop/SMSScheduler/JavaScript-SMScheduler/templates', 
            static_folder='/home/dfreeman/Desktop/SMSScheduler/JavaScript-SMScheduler/static') # Creates Flask object

totalData = [] # Stores a list of dictionaries containing each reminder the user creates


# Sends reminder information to smsGateway.py file to be sent out
def sendText():
    global totalData
    json_data = json.dumps(totalData)
    data_queue.put(json_data)
    
    
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    global totalData
    app.logger.info('Form has been submitted!')
    if flask.request.method == 'POST':
        phone = flask.request.form['phoneNumber']
        message = flask.request.form['message']
        dateTime = flask.request.form['datetimeInput']
        interval = flask.request.form['interval']
        data = {"phone": phone, "message": message, "dateTime": dateTime, "interval": interval}
        totalData.append(data)
        sendText()
        subprocess.Popen(['python', 'smsGateway.py'])
        app.logger.info('The other python program has begun!')
    return display_table()

@app.route('/table')
def display_table():
    global totalData
    app.logger.info('The table with the information has been loaded...')
    return render_template("running.html", data=totalData)


if __name__ == '__main__':
    app.run(debug=True)

