// Function to send parking data to the server
function sendData() {
  // Retrieving values from input fields
  const parking = document.getElementById('number1').value;
  const accPark = document.getElementById('number2').value;
  const imagePicker = document.getElementById('imagePicker').files[0];

  // Creating a FormData object to send data as multipart/form-data
  const formData = new FormData();
  formData.append('image', imagePicker);
  formData.append('parking', parking);
  formData.append('accPark', accPark);

  // Sending data to the server via fetch API
  fetch('/save_spots', {
    method: 'PUT',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Handling successful response
      console.log('Success:', data);
      // Storing parking data in sessionStorage for future use
      sessionStorage.setItem('parking', parking);
      sessionStorage.setItem('accPark', accPark);
      // Redirecting user to the draw.html page after successful submission
      window.location.href = './static/draw.html';
    })
    .catch((error) => {
      // Handling errors
      console.error('Error:', error);
    });
}

// Function to display previously saved parking amounts
function showAmounts() {
  document.addEventListener('DOMContentLoaded', function () {
    // Retrieving parking data from sessionStorage
    const parking = sessionStorage.getItem('parking');
    const accPark = sessionStorage.getItem('accPark');
    // Displaying the parking amounts in the HTML document
    document.getElementById('park').innerHTML =
      'New regular parkingspots: ' + parking;
    document.getElementById('acc').innerHTML =
      'New accessible parkingspots: ' + accPark;
  });
}

// Function to check the size of the selected image
function checkImageSize(input) {
  // Getting the selected file, Creating a new image object, Creating a new FileReader object
  var file = input.files[0];
  var img = new Image();
  var reader = new FileReader();

  // Event handler for when the FileReader has loaded the file
  reader.onload = function (e) {
    // Event handler for when the image has loaded
    img.onload = function () {
      // Checking if the image dimensions are not equal to 3840x2160
      if (img.width !== 3840 || img.height !== 2160) {
        // Alerting the user if the image size is incorrect
        alert('Please select an image of size 3840x2160.');
        input.value = '';
      }
    };
    img.src = e.target.result;
  };

  reader.readAsDataURL(file);
}
