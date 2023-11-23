let form = document.getElementById("inputForm");
let button = document.getElementById("alertButton");

function setLocalTime() {
    let time = document.createElement("INPUT");
    time.setAttribute("type", "datetime-local");
    document.body.appendChild(time);

}

function sayHello() {
    alert("Hello Wolrd")
}

button.addEventListener("click", function (event) {
    // Alerts user what the datetime input of a function is
    event.preventDefault()

    let dateTime = document.getElementById("datetimeInput").value;
    alert(dateTime)

});

// form.addEventListener("load")

form.addEventListener("submit", function(event) {
    // Prevent default form submission behavior

    // Retrieve the user input values for each part needed for 
    let phoneNumber = document.getElementById("phoneNumber").value;
    let message = document.getElementById("message").value;
    let datetime = document.getElementById("datetimeInput").value;
    let deltaInterval = document.getElementById("interval").value;

    // console.log("Phone number: " + phoneNumber);
    // console.log("Text message " + message);
    // console.log("Datetime " + datetime);
    // console.log("Interval " + deltaInterval);


}); 
