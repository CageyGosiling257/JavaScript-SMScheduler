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

os.chdir(r'C:\Users\davea\OneDrive\Desktop\SMS JavaScript Project')

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
        # INSERT FUNCTION CALL TO RESET DATETIME OF REPEATED INTERVALS
        sortTotalReminders()

# Constantly is sending out text messages whenever their dateTimes come due
sendOutThread = threading.Thread(target=sendMessages())






###### ADD WAY TO HAVE REMINDER'S DATETIME INCREASE DEPENDING ON THEIR INTERVALS TO REPEAT



