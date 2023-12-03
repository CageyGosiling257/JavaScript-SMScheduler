let phoneNumber = ""; 
let message = "";
let datetime = "";
let deltaInterval = ""
let countDownIsRunning = false
let reminders = []; // Stores list of dictionaries containing the information of each reminder
let timer = setInterval(updateCountdown, 1000) // Updates the countdown every second

// Sorts reminders from closest dateTime to the current time to the furthest away
function sortReminders() {
    reminders.sort((a,b) => {
        dateA = new Date(a.datetime);
        dateB = new Date(b.datetime);
        return dateA - dateB;
    });
}

function updateRemindersCountdown() {
    if(countDownIsRunning == true){
        for (entry in reminders) {
            updateCountdown(entry)
            sortReminders()
        }
    }
}

// Updates the countdown with the countdown until the next reminder fires
function updateCountdown(reminder) {
    targetDate = reminder.datetime; // Sets the target date to the inputted date
    now = new Date().getTime();
    distance = targetDate - now;

    // Calculates the different components of the countdown timer
    days = Math.floor(distance / (1000 * 60 * 60 * 24));
    hours = Math.floor(distance % (1000 * 60 * 60 * 24) / (1000 * 60 * 60));
    minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Displays timer on website screen.
    document.getElementById('Output').innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    
    if(distance < 0) {
        clearInterval(timer)
        document.getElementById('Output').innerHTML = "EXPIRED";
    }
    
}

// Event listeners for when user interacts with the app
document.addEventListener("DOMContentLoaded", function() {
    let form = document.getElementById("inputContainer");

    form.addEventListener("submit", function(event) {
        event.preventDefault();// Prevent default form submission behavior

        // Retrieve the user input values for each part needed for 
        phoneNumber = document.getElementById("phoneNumber").value;
        message = document.getElementById("message").value;
        datetime = document.getElementById("datetimeInput").value;
        deltaInterval = document.getElementById("interval").value;
        let dictOfInputs = {"phoneNumber": phoneNumber, "message": message, "datetime":datetime, "deltaInterval": deltaInterval};
        reminders.push(dictOfInputs);

        console.log("This is the reminders list:" + reminders)
        // Condition to start reminders countdown only when reminders list is not empty
        if(countDownIsRunning == false){
            countDownIsRunning == true;
        }
    
        // Calls function to start the reminders countdown
        updateRemindersCountdown();
        sortReminders();
        console.log(reminders);
    }); 
});
