from flask import Flask, render_template, redirect, url_for, Request
import flask
import smsGateway
import json
from data_queue import data_queue

app = Flask(__name__) # Creates Flask object

totalData = [] # Stores a list of dictionaries containing each reminder the user creates


# Sends reminder information to smsGateway.py file to be sent out
def sendText():
    json_data = json.dumps(totalData)
    data_queue.put(json_data)
    
    


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if flask.request.method == 'POST':
        phone = flask.request.form['phoneNumber']
        message = flask.request.form['message']
        dateTime = flask.request.form['datetimeInput']
        interval = flask.request.form['interval']
        data = {"phone": phone, "message": message, "dateTime": dateTime, "interval": interval}
        totalData.append(data)
        sendText()
    return display_table()

@app.route('/table')
def display_table():
    return render_template("running.html", data=totalData)


    

if __name__ == '__main__':
    app.run(debug=True)

