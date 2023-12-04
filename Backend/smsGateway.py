# This file will test sending sms messages through Email Gateways
import ezgmail
import ezsheets
import threading
import json
import datetime
from datetime import timedelta, datetime
import pytz
import time
import os

os.chdir(r'/home/dfreeman/Desktop/SMSScheduler/JavaScript-SMScheduler/Backend')


# Creates spreadsheet that contains data for SMS Gateway Emails
ss = ezsheets.Spreadsheet('1YhI6SSaoHEAPsxS8Qnea_tZ9EpOeN-zbLJB6ho8I9lE')
SMSList = ss[0] # Creates specific sheet
unfilteredCarrierEmails = SMSList.getColumn(4) # Retreives column of carrier emails
filteredUSCarrierEmails = [] # Stores cells containing only U.S.A carriers
filteredSMSList = [] # Holds list of U.S. carrier emails containing user's phone number
cell = 251 # Cell row number with 1st U.S. number
timezone = pytz.timezone('US/Eastern')

# List that holds input data containing information about the reminder from the website
totalReminders = []
sortedTotalReminders = []
isThreadRunning = False
sendOutThread = None

# Filters column 4 to only include U.S. Carriers
while (cell < 337):
    filteredUSCarrierEmails.append(unfilteredCarrierEmails[cell])
    cell += 1

# Retrieves json data from user, converts the dateTime str to dateTime object, sorts list of reminders
# based on their dateTime objects.
def processDataInput(jsonData):
    global totalReminders
    global sortedTotalReminders
    tempData = json.loads(jsonData) # Input json data is turned into a list of dictionaries
    dateTimeFormat ='%Y-%m-%dT%H:%M'
    naiveReminderDateTime = datetime.strptime(tempData["dateTime"], dateTimeFormat)
    tempData["dateTime"] = timezone.localize(naiveReminderDateTime)
    totalReminders.append(tempData)
    sortedTotalReminders = sortTotalReminders(totalReminders)
    print(sortedTotalReminders, "\n\nThis is processDataInput\n\n")


# Sorts the dynamic list of reminders by dateTime by converting dateTime strings in dateTime objects
def sortTotalReminders(reminders):
    sortedTotalReminders = sorted(reminders, key=lambda x: abs((x["dateTime"] - datetime.now(timezone))))
    return sortedTotalReminders

# Applies inputted phone number to SMSGateway email
def addPhoneToEmail(phone):
    global filteredSMSList
    filteredSMSList = [] # Clears SMSList to prevent duplicate carrier emails
    for carrier in filteredUSCarrierEmails:
        if(carrier.startswith("##########")):
            carrierEmail = phone + carrier[10:]
            filteredSMSList.append(carrierEmail)


# Adds user's phone number to SMS email and then sends the SMS email      
def sendText (body):
    counter = 0
    global filteredSMSList
    # Sends email to SMS carriers
    for email in filteredSMSList:
        print(email)
        ezgmail.send(email,"",body)
        print(f"Email Sent YAY! This is the {counter} email!!\n\n")
        counter += 1
        
# Resets the DateTime variable of a message after it is sent out
def resetDateTime():
    global sortedTotalReminders
    temp = sortedTotalReminders
    for entry in temp:
        if(entry["interval"] == "No Repeats" and entry["timesSent"] != 0):
            temp.remove(entry)
        elif (entry["interval"] == "Every Minute"):
            entry["dateTime"] = entry["dateTime"] + timedelta(seconds=60)
        elif (entry["interval"] == "Every Hour"):
            entry["dateTime"] = entry["dateTime"] + timedelta(minutes=60)
        elif (entry["interval"] == "Every 12 Hours"):
            entry["dateTime"] = entry["dateTime"] + timedelta(hours=12)
        elif (entry["interval"] == "Daily (24 Hours)"):
            entry["dateTime"] = entry["dateTime"] + timedelta(hours=24)
        elif (entry["interval"] == "Every 2 days (48 hours)"):
            entry["dateTime"] = entry["dateTime"] + timedelta(hours=48)
        elif (entry["interval"] == "Weekly (7 Days)"):
            entry["dateTime"] = entry["dateTime"] + timedelta(days=7)
            
    # Resets value of totalReminders to edited vals
    sortedTotalReminders = temp    
    
    

# Sends out text message for each reminder that the user creates
def sendMessages():
    global sortedTotalReminders
    while True:
        try:
            if not sortedTotalReminders:
                break  # Break the loop if there are no more reminders

            currentTime = datetime.now(timezone)
            for entry in sortedTotalReminders[:]:  # Loop over a copy of the list
                reminderDateTime = entry["dateTime"]

                if currentTime >= reminderDateTime:
                    addPhoneToEmail(entry["phone"])
                    sendText(entry["message"])
                    entry["timesSent"] += 1
                    print(f"\n\nSent text {entry['message']} to {entry['phone']} phone number!\n\n")
                    resetDateTime()
                    sortedTotalReminders = sortTotalReminders(sortedTotalReminders)

            time.sleep(1)
        except Exception as e:
            print(f"Error in sendMessages: {e}")

# Takes input json and creates thread to process it and send messages
def startProgram(json):
    global isThreadRunning
    global sendOutThread
    processDataInput(json)
    if(not isThreadRunning):
        sendOutThread = threading.Thread(target=sendMessages)
        sendOutThread.start()
        isThreadRunning = True