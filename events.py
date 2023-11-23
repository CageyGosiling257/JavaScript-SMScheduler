# Event class file containing member variables and functions used to create and send out SMS reminders

from twilio.rest import Client
import datetime
from datetime import timedelta
from datetime import datetime
import pyinputplus as pyip
import time
import pytz

# Creates an object for each reminder the user creates
class Event():
    def __init__(self):  # Constructor that initializes member variables of object.  Also calls createReminder() function
        self.twilioNumber = "18776242715" 
        self.accountSID = "ACce6ad8a057611e8676133cbdb41c952b" 
        self.authToken = "db5853ca072c05c36797b6b45ed3cd7f" 
        self.userCellNumber = " " 
        self.date = " " 
        self.time = " " 
        self.reminder = " " 
        self.dateTime = " " 
        self.interval = " " 
        self.delta = " " 
        self.messagesSent = 0 
        self.createReminder() 
        self.setTimeDelta() 
    

 # Asks the user a series of questions to retreive information necessary to send an SMS message
    def createReminder(self):
        # 1st Question: User Phone Number
            status = False
            while status == False:
                try:
                    cellNum = input("\n\nWhat is your cell phone number? Please enter it without spaces like so: '4235769182'.\n\n")
                    if(len(cellNum) == 10 and cellNum.isdigit()):
                        self.userCellNumber = "1" + cellNum
                        status = True
                    else:
                        raise Exception("\n\nPhone Number Entered Incorrectly\n\n")
                except: 
                    print("\nSorry, you must have entered your phone number incorrectly.  Please try again following \nthis example: '4235769182'.")
                    time.sleep(2)
                    status = False    
                
        # 2nd question: Reminder Text
            self.reminder = pyip.inputStr(prompt="\nWhat would you like your reminder message to say?\n\n")
            
        # 3rd question: Date to Send 1st Text
            self.date = pyip.inputDate(prompt="\nWhat date should the first reminder be sent to you?  Please enter the date in MM/DD/YY format.\n\n" 
                            ,formats=('%m/%d/%y','%d/%m/%y'))
            
        # 4th question: Time to Send 1st Text
            self.time = pyip.inputTime(prompt="\nWhat time should the first reminder be sent to you?\n" 
                            "\nPlease enter it in HH:MM format using military time. Ex: '08:00' for 8:00 AM or '20:00' for 8:00 PM.\n\n")
        
        # 5th question: How often Reminder Repeats
            self.interval = pyip.inputMenu(prompt="\nHow often should this reminder occur? Please enter a number to select a choice.\n\n"
                                           ,choices=["Weekly", "Daily", "Twice a Day", "Hourly", "Every Minute", "No Repeats"],numbered=True)
            
            timeZone = pytz.timezone('US/Eastern') 
            self.dateTime = timeZone.localize(datetime.combine(self.date, self.time))


    # Determines if/when a reminder should repeat (weekly, daily, hourly etc.)
    def setTimeDelta(self):
        if self.interval == "Weekly": 
                self.delta = timedelta(days=7)
                
        elif self.interval == "Daily": 
                self.delta = timedelta(hours=24)
                
        elif self.interval == "Twice a Day":
                self.delta = timedelta(hours=12)
        
        elif self.interval == "Hourly":
                self.delta = timedelta(minutes=60)
        
        elif self.interval == "Every Minute":
                self.delta = timedelta(seconds=60)
        
        elif self.interval == "No Repeats":
                self.delta = None
        
        else: 
                self.delta = None
    
    

    # Calculates when the next reminder text should be sent out
    def setRepeatDateTime(self):
        timeZone = pytz.timezone('US/Eastern')
        currentTime = datetime.now(timeZone) 
        self.dateTime = self.delta + currentTime
        print("This reminder will fire again at {}".format(self.dateTime))

        
    # Sends the SMS reminder to the user's cellphone
    def sendSMS(self): 
        twilioClient = Client(self.accountSID, self.authToken)
        message = twilioClient.messages.create(body=self.reminder, from_=self.twilioNumber, to=self.userCellNumber)
        self.messagesSent += 1
        return