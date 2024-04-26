function sendData() {
  var parking = document.getElementById("number1").value;
  var accPark = document.getElementById("number2").value;

  sessionStorage.setItem("parking", parking);
  sessionStorage.setItem("accPark", accPark);

  window.location.href='./static/draw.html';
}

function showDraw() {
  document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the values from session storage
    var parking = sessionStorage.getItem("parking");
    var accPark = sessionStorage.getItem("accPark");

    // Display the values in the respective divs
    document.getElementById("park").innerHTML = parking;
    document.getElementById("acc").innerHTML = accPark;

    fetch('/run-opencv').then(response => {
      console.log('opencv.py executed successfully');
    }).catch(error => {
      console.error('Error executing opencv.py:', error);
    });
});
}
