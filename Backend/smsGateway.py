# This file will test sending sms messages through Email Gateways
import os
import ezgmail
import ezsheets
import threading
import json
import datetime
import pytz
import time
import sys
from dataqueue import data_queue

# Child directory to create API tokens
os.chdir(r'/home/dfreeman/Desktop/SMSScheduler/JavaScript-SMScheduler/Backend')

# Creates spreadsheet that contains data for SMS Gateway Emails
ss = ezsheets.Spreadsheet('1YhI6SSaoHEAPsxS8Qnea_tZ9EpOeN-zbLJB6ho8I9lE')

SMSList = ss[0] # Creates specific sheet

unfilteredCarrierEmails = SMSList.getColumn(4) # Retreives column of carrier emails

filteredUSCarrierEmails = [] # Stores cells containing only U.S.A carriers

filteredSMSList = [] # Holds list of U.S. carrier emails containing user's phone number

cell = 251 # Cell row number with 1st U.S. number

# Creates Eastern timezone for times
timezone = pytz.timezone('US/Eastern')

# List that holds input data containing information about the reminder from the website
totalReminders = []

# Filters column 4 to only include U.S. Carriers
while (cell < 337):
    filteredUSCarrierEmails.append(unfilteredCarrierEmails[cell])
    cell += 1

# Retrieves data input and stores it in totalReminders so it can be used across the file
def processDataInput(jsonData):
    global totalReminders
    totalReminders = json.loads(jsonData) # Input json data is turned into a list of dictionaries


# Sorts the dynamic list of reminders by dateTime
def sortTotalReminders():
    global totalReminders
    sorted(totalReminders, key=lambda x: (x['dateTime']))

# Applies inputted phone number to SMSGateway email
def addPhoneToEmail(phone):
    for carrier in filteredUSCarrierEmails:
        if(carrier.startswith("##########")):
            carrierEmail = phone + carrier[10:]
            filteredSMSList.append(carrierEmail)


# Adds user's phone number to SMS email and then sends the SMS email      
def sendText (body):
    counter = 0
    
    # Sends email to SMS carriers
    for email in filteredSMSList:
        print(email)
        ezgmail.send(email,"",body)
        print(f"Email Sent YAY! This is the {counter} email!!\n\n")
        counter += 1
        
# Resets the DateTime variable of a message after it is sent out
def resetDateTime():
    global totalReminders
    temp = totalReminders
    for entry in temp:
        if(entry["interval"] == "No Repeats" and entry["timesSent"] != 0):
            temp.remove(entry)
        elif (entry["interval"] == "Every Minute"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(seconds=60)
        elif (entry["interval"] == "Every Hour"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(minutes=60)
        elif (entry["interval"] == "Every 12 Hours"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(hours=12)
        elif (entry["interval"] == "Daily (24 Hours)"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(hours=24)
        elif (entry["interval"] == "Every 2 days (48 hours)"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(hours=48)
        elif (entry["interval"] == "Weekly (7 Days)"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(days=7)
            
    # Resets value of totalReminders to edited vals
    totalReminders = temp    
    
    

# Sends out text message for each reminder that the user creates
def sendMessages():
    global totalReminders
    print(totalReminders)
    while True:
        # Has program wait until a reminder has been created to send it out
        while(len(totalReminders) < 1):
            time.sleep(1)
        while(len(totalReminders) >= 1):
            try:
                for entry in totalReminders:
                    print(entry)
                    print(entry["dateTime"])
                    currentTime = datetime.datetime.now(timezone)
                    print(currentTime)
                    dateTimeFormat ='%Y-%m-%dT%H:%M'
                    naiveReminderDateTime = datetime.datetime.strptime(entry["dateTime"], dateTimeFormat)
                    reminderDateTime = timezone.localize(naiveReminderDateTime)
                    print(reminderDateTime)
                    print(totalReminders)
                    # Has thread wait to send out texts until it is time
                    while(currentTime < reminderDateTime):
                        time.sleep(1)
                        currentTime = datetime.datetime.now(timezone)
                    
                    addPhoneToEmail(entry["phone"])
                    sendText(entry["message"])
                    entry["timesSent"] += 1
                    print(f"\n\nSent text {entry['message']} to {entry['phone']} phone number!\n\n")
                    print("\n\n This is right before resetDateTime()\n\n")
                    print(totalReminders)
                    resetDateTime()
                    print("\n\nThis is right before sortTotalReminders()\n\n")
                    print(totalReminders)
                    sortTotalReminders()
                    print(totalReminders)
            except:
                continue



# Thread that will constantly be running the sendMessages function to send out messages
# at their designated times
sendOutThread = threading.Thread(target=sendMessages)
sendOutThread.start()


# When this file is called in the flaskApp.py file
if __name__== '__main__':
# Check if the JSON input data is provided as a command-line argument
    if len(sys.argv) > 1:
        json_data = sys.argv[1]  # Access the first command-line argument with input data
        
        # Call the function to process the JSON data and put it into totalReminders
        processDataInput(json_data)
    else:
        print("No data provided.")



