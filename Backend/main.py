# This file will be constantly running in order to send out the SMS reminders at their designated times
import events
import time, datetime
from datetime import datetime
import threading
import pytz

exitFlag = threading.Event()


# Main function of the program that outputs text and accepts input from the user.
def main():

    print("\n\nWelcome to the SMScheduler!  Please follow the directions below:\n\n")
    time.sleep(1)
    reminder1 = events.Event() 
    sortedReminders = [reminder1]
   
    # Creates a new thread to send out reminders
    threadObj = threading.Thread(target=checkReminders,args=(sortedReminders,))
    threadObj.start() 
    
    time.sleep(2) 
    
    # Creates new reminders or exits the program.  If all reminders are set to NOT repeat,and have been sent out
    # then the program will terminate.
    while len(sortedReminders) > 0:
        global choice # Declares choice a global variable
        choice = input("""
\n\n
Please enter '1' if you would like to create another reminder or '2' to exit the application. \n
Otherwise, please wait until your reminders are texted to you.

Your next reminder will be at {}.\n\n""".format(sortedReminders[0].dateTime))
        
        # Adds a reminder if user selected '1' to create another reminder
        if choice == '1':  
            reminder = events.Event() 
            sortedReminders.append(reminder) 
            sortedReminders = sorted(sortedReminders, key=lambda reminder: reminder.dateTime)
            print("\n\nNumber of reminders: {}.\n".format(len(sortedReminders)))
            time.sleep(1)


        # Choice to end the program completely                
        elif choice == '2':
            print("\nThe program will stop as soon as the next reminder is sent. Thank you for using the SMScheduler!\n")
            exitFlag.set()
            break
            
        else:
            print("\n\nSorry, you have entered unrecognized response, please enter '1' if you would like " 
                "to create another reminder or '2' to wait for your next reminder.\n\n")
            
    # Terminates the program if there are no more reminders left
    if(len(sortedReminders) == 0):
        print("\n\nAll reminders have been sent out.  Thank you for using the SMScheduler!\n"
            "The SMScheduler will now terminate.  Have a blessed day!\n")
        time.sleep(3)
        exit()



# Sends each reminder text to user at designated times
def checkReminders(reminders):
    currentDate = datetime.now(pytz.timezone('US/Eastern'))
    
    
    while not exitFlag.is_set():
        
            # Breaks out of loop if there are no more reminders left or if user chooses to terminate the program
            if(len(reminders) == 0):
                break
            
            else:  # Runs code to send out text messages when it comes time for a message to send  
                for remind in reminders:
                    print("\n\nTotal Reminders: {}\n\n".format(len(reminders)))  
                    print("\nProcessing...   Your next reminder will be at {}.\n".format(remind.dateTime))
                    while currentDate < remind.dateTime:
                        time.sleep(1)
                        currentDate = datetime.now(pytz.timezone('US/Eastern'))
                    
                    print("\nA reminder has been texted to you.  You will receive a text message momemtarily.\n")
                    remind.sendSMS()
                    
                    if(remind.delta is not None):                     
                        remind.setRepeatDateTime()
                    else: 
                        reminders.remove(remind)

    print("\n\nAll reminders have been sent out.  Thank you for using the SMScheduler!\n"
        "The SMScheduler will now terminate.  Have a blessed day!\n")
    time.sleep(3)
    exit()
        
                    

# Calls main function to run program
if __name__ == '__main__':
    main()


