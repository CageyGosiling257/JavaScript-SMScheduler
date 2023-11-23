# Unit Tests file for SMScheduler
import events
import datetime
from datetime import datetime
from datetime import timedelta
import main



# Stores whether or not a function passed a test. 1 means it passed and 2 means it failed.
benchmarks = {}

print("\n\n Welcome to the beginning of the SMScheduler Unit Tests!!\n\n")

# Creates initial test object to test its member functions
testObj = events.Event()
testObjList = [testObj]


# Tests the constructor of Event class in events.py
def testConstructor():
    if testObj.userCellNumber == " ":  # Test fails if constructor fails to call createReminder() to get user input
        print("\n\nCONSTRUCTOR FAILED.  createReminder FUNCTION FAILED TO EXECUTE PROPERLY\n\n")
        benchmarks.update({"constructor": "fail"})
    else:
        benchmarks.update({"constructor": "pass"})
    
    if testObj.delta == " ": # If delta variable has not be assigned anything, it fails
        print("\n\nCONSTRUCTOR FAILED.  setTimeDelta FUNCTION FAILED TO EXECUTE PROPERLY\n\n")
        benchmarks.update({"constructor": "fail"})
        
    else:
        print("\n\nCONSTRUCTOR PASSED.\n\n")
        benchmarks.update({"constructor": "pass"})


# Tests the CreateReminder function in events.py to see if it prompts user for input and stores what the user inputted
def testCreateReminder():
    if testObj.reminder == " ": # If reminder variable has not been changed the function fails
        print("\n\ncreateReminder FUNCTION FAILED\n\n")
        benchmarks.update({"createReminder": "fail"})
    else:
        print("\n\ncreateReminder FUNCTION PASSED\n\n")
        benchmarks.update({"createReminder": "pass"})
        


# Tests the setTimeDelta function in events.py to see if stored the user's choice for the timedelta variable (how often a reminder should repeat)
def testSetTimeDelta():
    if testObj.reminder == " ": # If delta variable has not been changed the function fails
        print("\n\nsetTimeDelta FUNCTION FAILED\n\n")
        benchmarks.update({"setTimeDelta": "fail"})
    else:
        print("\n\nsetTimeDelta FUNCTION PASSED\n\n")
        benchmarks.update({"setTimeDelta": "pass"})
        


# Tests the setRepeatTime function in events.py.  Creates a new object just to avoid messing with other testing functions
def testSetRepeatDateTime():
    testObj.delta = timedelta(seconds=5)# Forces the delta to be non-none so that an error will not be raised
    testDate1 = testObj.dateTime # Sets 1st testDate to original inputted dateTime
    testDate2 = testObj.setRepeatDateTime() # Sets 2nd testDate to changed dateTime
    if testDate2 == testDate1: # If the 2nd date still equals the original date the function failed
        print("\n\nsetRepeatDateTime FUNCTION FAILED\n\n")
        benchmarks.update({"setRepeatedDateTime": "fail"})
    else:
        print("\n\nsetRepeatDateTime FUNCTION PASSED\n\n")
        benchmarks.update({"setRepeatedDateTime": "pass"})
        
    
# Tests the sendSMS function in events.py.  If the testObj does not send a message, the function failed
def testSendSMS():
    testObj.sendSMS() # Calls the sendSMS function to send a message
    if testObj.messagesSent < 1:
        print("\n\nsendSMS FUNCTION FAILED\n\n")
        benchmarks.update({"sendSMS": "fail"})
    else:
        print("\n\nsendSMS FUNCTION PASSED\n\n")
        benchmarks.update({"sendSMS": "pass"})
        
# Tests the CheckReminders Function in the main.py file. 
def testCheckReminders(objList):
    objList[0].delta = None # Forces function to delete its only reminder after 1 text
    main.checkReminders(objList)
    if len(objList) != 0: # Already sent a message in the last unit test, so now 2 will have been sent
        print("\n\ncheckReminders FUNCTION FAILED\n\n")
        benchmarks.update({"checkReminders": "fail"})
    else:
        print("\n\ncheckReminders FUNCTION PASSED\n\n")
        benchmarks.update({"checkReminders": "pass"})
        

        

        
    

# Calls all functions in the file to test them.  If any of them failed, their definition in the 
# benchmarks dictionary will be "fail".  The function will then print which functions failed.
testConstructor()
testCreateReminder()
testSetTimeDelta()
testSetRepeatDateTime()
testSendSMS()
testCheckReminders(testObjList)

for key in benchmarks:
    if benchmarks[key] == "fail":
        print("The function {} failed.  Please fix this function before deploying.".format(key))
    else: 
        print("\n\nThe function {} passed!  Great work!\n\n".format(key))
        
        
    
