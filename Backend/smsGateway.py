# This file will test sending sms messages through Email Gateways
import os
import ezgmail
import ezsheets
import threading
import json
import datetime
import pytz
import time
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

totalReminders = [] # List of dictionaries containing information for reminders


# Filters column 4 to only include U.S. Carriers
while (cell < 337):
    filteredUSCarrierEmails.append(unfilteredCarrierEmails[cell])
    cell += 1

# Creates a list of all created reminders
if not data_queue.empty():
    json_data = data_queue.get()
    totalReminders = json.loads(json_data)  # Data recieved is the total_data variable


# Sorts the dynamic list of reminders by dateTime
def sortTotalReminders():
    global totalReminders
    totalReminders = sorted(totalReminders, key=lambda x: (x['dateTime']))

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
    for entry in totalReminders:
        if(entry["interval"] == "No Repeats"):
            totalReminders.remove(entry)
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
    
    
    

# Sends out text message for each reminder that the user creates
def sendMessages():
    global totalReminders
    while(len(totalReminders) < 1):
        time.sleep(1)    
    print("\n\nSend messages function has been called!\n\n")
    while(len(totalReminders) >= 1):
        for entry in totalReminders:
            
            print(entry)
            print(entry["dateTime"])
            currentTime = datetime.datetime.now(timezone)
            print(currentTime)
            
            # Has thread wait to send out texts until it is time
            while(currentTime < entry["dateTime"]):
                time.sleep(1)
                currentTime = datetime.datetime.now(timezone)
            
            addPhoneToEmail(entry["phone"])
            sendText(entry["message"], entry["message"])
            print(f"\n\nSent text {entry['message']} to {entry['phone']} phone number!\n\n")
            resetDateTime()
            sortTotalReminders()


sendOutThread = threading.Thread(target=sendMessages)
sendOutThread.start()



# if __name__== '__main__':
#     sendOutThread = threading.Thread(target=sendMessages())
#     sendOutThread.start()



