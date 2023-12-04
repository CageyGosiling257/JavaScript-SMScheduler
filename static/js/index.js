// Resets the input fields for user
function resetInputs() {
    document.getElementById('inputForm').reset();
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


// Performs JS operations after the page has loaded
document.addEventListener('DOMContentLoaded', function() {
    titleAdded = false; // Check to see if the Table title has been added
  
    function updateTableAndCountdown() {
      fetch('/get_table_data')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            let sortedData = compareDates(data);
            data = sortedData;
            console.log(data);
            updateTable(data); // Update table with sorted reminders
            startCountdown(data); // Start the countdown with the sorted reminders
        })
        .catch(error => {
            console.error('Error fetching table data:', error);
        });
    }
  
  
    // Event listener waits for User Input to display table
    document.getElementById('inputForm').addEventListener('submit', function(event) {
      event.preventDefault();
  
      // Perform the form submission via AJAX/fetch to trigger Flask route
      fetch('/submit', {
        method: 'POST',
        body: new FormData(document.getElementById('inputForm'))
      })
        .then(response => {
          // Optionally handle response if needed
          console.log('Form submitted successfully');
          updateTableAndCountdown(); // Call to update table and countdown for the function
        })
        .catch(error => {
          // Handle errors if any
          console.error('Error submitting form:', error);
        });
    });
  
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
            // Create table cells for each data entry
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
  