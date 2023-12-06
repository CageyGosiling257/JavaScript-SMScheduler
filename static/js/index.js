// Resets the input fields for user
function resetInputs() {
    document.getElementById('inputForm').reset();
}


// Validates the form to ensure inputs were entered correctly
function validateForm() {

  // Phone number validation
  const phoneNumber = document.getElementById('phoneNumber').value;
  const phoneNumberPattern = /^[0-9]{10}$/;
  if (!phoneNumberPattern.test(phoneNumber)) {
    alert('Please enter a valid phone number with 10 digits.');
    return false;
  }

  // Message validation
  const message = document.getElementById('message').value;
  if(message.trim() === '') {
    alert('Please fill in the message field with your message.');
    return false;
  }

  // DateTime validation
  const inputDateTimeValue = document.getElementById('datetimeInput').value;
  const inputDateTime = new Date(inputDateTimeValue);
  const now = new Date();
  if(now - inputDateTime >= 0) {
    alert('Please select a dateTime that is at least 1 minute in the future.');
    return false;
  }

  // Repeat Dropdown validation
  const repeatInterval = document.getElementById('interval').value;
  if(repeatInterval === '') {
    alert('Please select a repeat interval from the dropdown.');
    return false;
  }

  return true; // If all validations pass, the form will be submitted
}


// Function that compares the dates of datetime entries and returns the difference
function compareDates(list) {
    const now = new Date(); // Current date and time
    const sortedList = list.slice(); // Creates a copy of the original list
    
    sortedList.sort((a, b) => {
        const dateA = new Date(a.dateTime);
        const dateB = new Date(b.dateTime);
        
        const diffA = Math.abs(now - dateA); // Time difference from dateA to now
        const diffB = Math.abs(now - dateB); // Time difference from dateB to now
        
        return diffA - diffB; // Sort based on the differences
    });
    
    return sortedList;
}



/*
BEGINNING OF FUNCTION CALLS THAT MAKE PROGRAM WORK
*/


// Performs JS operations after the page has loaded
document.addEventListener('DOMContentLoaded', function() {
    titleAdded = false; // Check to see if the Table title has been added
  
    // Displays the user-created reminders to the screen in the form of a table
    // from the soonest reminder to the one farthest away.
    function displayReminders() {
      fetch('/get_table_data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            let sortedData = compareDates(data);
            data = sortedData;
            console.log(data);
            updateTable(data); // Update table with sorted reminders
        })
        .catch(error => {
            console.error('Error fetching table data:', error);
        });
    }
  
  
    // Event listener waits for the user to click the submit button to display the table
    document.getElementById('inputForm').addEventListener('submit', function(event) {
      event.preventDefault();

      // Checks to see if the inputs were validated. If so, function continues, if not
      // the function alerts the user and the inputs are reset.
      if(validateForm()) {

        // Uses AJAX to add a reminder to the reminders list when the user submits a form.
        fetch('/submit', {
          method: 'POST',
          body: new FormData(document.getElementById('inputForm'))
        })
          .then(response => {
            // Optionally handle response if needed
            console.log('Form submitted successfully');
            displayReminders(); // Call to update table and countdown for the function
          })
          .catch(error => {
            // Handles any errors
            console.error('Error submitting form:', error);
          });
      } else {
        alert('Please enter valid user inputs.');
        resetInputs();
      }
    });
  
    // Creates and displays a table on screen that contains the user-created reminders
    function updateTable() {
        fetch('/get_table_data')  // Fetch data from the Flask route
        .then(response => response.json())
        .then(data => {
            console.log(data)
            let sortedData = compareDates(data);
            data = sortedData;
            console.log(data);
            // Creates an h1 header for the reminder table
            if (!titleAdded) {
                const pageTitle = document.createElement('h1');
                pageTitle.textContent = 'Reminder Schedule';
                const countdownsDiv = document.getElementById('countdowns');
                countdownsDiv.parentNode.insertBefore(pageTitle, countdownsDiv.nextSibling);
                titleAdded = true;
          }
  
            // Creates table for the reminders the user creates
            const table = document.querySelector('table'); // Selects the 1st tbody element
            table.innerHTML = ''; // Clear previous data
  
            const tableHead = document.createElement('thead'); // Creates a table head
            const headRow = document.createElement('tr'); // Creates a table head row
            const headers = ['Phone', 'Message', 'DateTime', 'Interval', 'Times Sent']; // Table header labels
  
            // For each header, it creates a 'th' element to append as child to headRow element
            headers.forEach(headerText => {
                const th = document.createElement('th');
                th.textContent = headerText;
                headRow.appendChild(th);
            })
  
            tableHead.appendChild(headRow); // Creates the table head with the table row entries
            table.appendChild(tableHead);

            // Creates the table body
            const tableBody = document.createElement('tbody');
            data.forEach(row => {
              const bodyRow = document.createElement('tr');
              // Creates the table cells with their data for each row
              Object.values(row).forEach(cellData => {
                  const td = document.createElement('td');
                  td.textContent = cellData;
                  bodyRow.appendChild(td);
              });
            tableBody.appendChild(bodyRow); // Creates the table body made up of each row
          });
          table.appendChild(tableBody); // Adds the table body to the table
          resetInputs(); // Resets input fields
        })
  
        // Catches errors in loading the table
        .catch(error => {
          console.error('Error fetching table data:', error);
        });
    }
  });