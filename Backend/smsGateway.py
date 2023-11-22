# This file will test sending sms messages through Email Gateways
import os
import ezgmail
import ezsheets
import threading
import json
import datetime
import pytz
import time
import datetime
from data_queue import data_queue

os.chdir(r'/home/dfreeman/Desktop/SMSScheduler/JavaScript-SMScheduler/Backend')

# Creates spreadsheet
ss = ezsheets.Spreadsheet('1YhI6SSaoHEAPsxS8Qnea_tZ9EpOeN-zbLJB6ho8I9lE')
SMSList = ss[0]# Creates specific sheet
unfilteredCarrierEmails = SMSList.getColumn(4) # Retreives column of carrier emails
filteredUSCarrierEmails = []
cell = 251 # Cell row number with 1st U.S. number
totalReminders = []


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
    totalReminders = sorted(totalReminders, key=lambda x: datetime.fromisoformat(x['date']))

# Adds user's phone number to SMS email and then sends the SMS email      
def sendText (phone, head, body):
    filteredSMSList = []
    counter = 0
    
    # Applies inputted phone number to SMSGateway emails
    for carrier in filteredUSCarrierEmails:
        if(carrier.startswith("##########")):
            carrierEmail = phone + carrier[10:]
            filteredSMSList.append(carrierEmail)
        else:
            pass
    
    # Sends email to SMS carriers
    for email in filteredSMSList:
        print(email)
        ezgmail.send("7706174970@txt.att.net",head,body)
        print(f"Email Sent YAY! This is the {counter}\n\n")
        counter += 1
        
# Resets the DateTime variable of a message after it is sent out
def resetDateTime():
    for entry in totalReminders:
        if(entry["interval"] == "No Repeats"):
            totalReminders.remove(entry)
        elif (entry["inteval"] == "Every Minute"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(seconds=60)
        elif (entry["inteval"] == "Every Hour"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(minutes=60)
        elif (entry["inteval"] == "Every 12 Hours"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(hours=12)
        elif (entry["inteval"] == "Daily (24 Hours)"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(hours=24)
        elif (entry["inteval"] == "Every 2 days (48 hours)"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(hours=48)
        elif (entry["inteval"] == "Weekly (7 Days)"):
            entry["dateTime"] = entry["dateTime"] + datetime.timedelta(days=7)
    
    
    

# Sends out text message for each reminder that the user creates
def sendMessages():    
    for entry in totalReminders:
        timezone = pytz.timezone('US/Eastern')
        currentTime = datetime.now(timezone)
        
        # Has thread wait to send out texts until it is time
        while(currentTime < entry["dateTime"]):
            time.sleep(1)
            currentTime = datetime.now(timezone)
        
        sendText(entry["phone"], entry["message"], entry["message"])
        resetDateTime()
        sortTotalReminders()

# Constantly is sending out text messages whenever their dateTimes come due
sendOutThread = threading.Thread(target=sendMessages())
sendOutThread.start()






###### ADD WAY TO HAVE REMINDER'S DATETIME INCREASE DEPENDING ON THEIR INTERVALS TO REPEAT



