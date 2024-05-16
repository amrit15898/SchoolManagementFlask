check = document.getElementById("check")
function checking(){
    window.alert('only for checking')
}
document.addEventListener("DOMContentLoaded", function() {
    // Get the link element
    var getTeachersLink = document.getElementById("get-teachers-link");

    // Attach click event listener to the link
    getTeachersLink.addEventListener("click", function(event) {
        // Prevent the default behavior of the link (i.e., navigating to a new page)
        event.preventDefault();

        // Create a new XMLHttpRequest object
        var xhr = new XMLHttpRequest();

        // Configure the request
        xhr.open("GET", "http://127.0.0.1:5000/get-teachers");

        // Set up a function to handle the response
        xhr.onload = function() {
            if (xhr.status === 200) {
                // Handle the response here
                console.log(xhr.responseText);
                // You can manipulate the DOM or display the response data as needed
            } else {
                // Handle errors here
                console.error("Request failed. Status:", xhr.status);
            }
        };

        // Set up a function to handle errors
        xhr.onerror = function() {
            // Handle errors here
            console.error("Request failed. Network error");
        };

        // Send the request
        xhr.send();
    });
});