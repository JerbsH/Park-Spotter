function sendData() {
  const parking = document.getElementById('number1').value;
  const accPark = document.getElementById('number2').value;
  const imagePicker = document.getElementById('imagePicker').files[0];

  const formData = new FormData();
  formData.append('image', imagePicker);
  formData.append('parking', parking);
  formData.append('accPark', accPark);

  fetch('/save_spots', {
    method: 'PUT',
    body: formData,
  })
  .then((response) => response.json())
  .then((data) => {
    console.log('Success:', data);
    sessionStorage.setItem('parking', parking);
    sessionStorage.setItem('accPark', accPark);
    window.location.href = './static/draw.html';
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

function showAmounts() {
  document.addEventListener('DOMContentLoaded', function () {

    const parking = sessionStorage.getItem('parking');
    const accPark = sessionStorage.getItem('accPark');
    document.getElementById('park').innerHTML = "New regular parkingspots: " + parking;
    document.getElementById('acc').innerHTML = "New accessible parkingspots: " + accPark;
  });
}

function checkImageSize(input) {
  var file = input.files[0];
  var img = new Image();
  var reader = new FileReader();

  reader.onload = function(e) {
    img.onload = function() {
      if (img.width !== 3840 || img.height !== 2160) {
        alert('Please select an image of size 3840x2160.');
        input.value = '';
      }
    };
    img.src = e.target.result;
  };

  reader.readAsDataURL(file);
}


