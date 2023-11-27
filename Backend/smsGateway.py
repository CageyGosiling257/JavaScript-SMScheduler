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
from data_queue import data_queue

os.chdir(r'/home/dfreeman/Desktop/SMSScheduler/JavaScript-SMScheduler/Backend')

# Creates spreadsheet
ss = ezsheets.Spreadsheet('1YhI6SSaoHEAPsxS8Qnea_tZ9EpOeN-zbLJB6ho8I9lE')

SMSList = ss[0] # Creates specific sheet

unfilteredCarrierEmails = SMSList.getColumn(4) # Retreives column of carrier emails

filteredUSCarrierEmails = [] # Stores cells containing only U.S.A carriers

filteredSMSList = []

cell = 251 # Cell row number with 1st U.S. number

# Creates Eastern timezone for times
timezone = pytz.timezone('US/Eastern')

totalReminders = []

# Filters column 4 to only include U.S. Carriers
while (cell < 337):
    filteredUSCarrierEmails.append(unfilteredCarrierEmails[cell])
    cell += 1

# Processes data input
def processDataInput(jsonData):
    global totalReminders
    totalReminders = json.loads(jsonData) # Data recieved is the total_data variable


# Sorts the dynamic list of reminders by dateTime
def sortTotalReminders():
    global totalReminders
    sorted(totalReminders, key=lambda x: (x['dateTime']))

def addPhoneToEmail(phone):
    # Applies inputted phone number to SMSGateway email
    for carrier in filteredUSCarrierEmails:
        if(carrier.startswith("##########")):
            carrierEmail = phone + carrier[10:]
            filteredSMSList.append(carrierEmail)


# Adds user's phone number to SMS email and then sends the SMS email      
def sendText (head, body):
    counter = 0
    
    # Sends email to SMS carriers
    for email in filteredSMSList:
        print(email)
        ezgmail.send(email,head,body)
        print(f"Email Sent YAY! This is the {counter}\n\n")
        counter += 1
        
# Resets the DateTime variable of a message after it is sent out
def resetDateTime():
    global totalReminders
    temp = totalReminders
    for entry in temp:
        if(entry["interval"] == "No Repeats"):
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
        while(len(totalReminders) < 1):
            time.sleep(1)    
        print("\n\nSend messages function has been called!\n\n")
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
                    sendText(entry["message"], entry["message"])
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




sendOutThread = threading.Thread(target=sendMessages)
sendOutThread.start()



if __name__== '__main__':
# Check if the JSON data is provided as a command-line argument
    if len(sys.argv) > 1:
        json_data = sys.argv[1]  # Access the first command-line argument
        
        # Call the function to process the JSON data
        processDataInput(json_data)
    else:
        print("No data provided.")



