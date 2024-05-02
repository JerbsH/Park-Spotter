function sendData() {
  const parking = document.getElementById('number1').value;
  const accPark = document.getElementById('number2').value;

  sessionStorage.setItem('parking', parking);
  sessionStorage.setItem('accPark', accPark);

  fetch('/save_spots', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      parking: parking,
      accPark: accPark,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
      window.location.href = './static/draw.html';
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function showDraw() {
  document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the values from session storage
    const parking = sessionStorage.getItem('parking');
    const accPark = sessionStorage.getItem('accPark');

    // Display the values in the respective divs
    document.getElementById('park').innerHTML = parking;
    document.getElementById('acc').innerHTML = accPark;

    fetch('/run-opencv')
      .then((response) => {
        console.log('opencv.py executed successfully');
      })
      .catch((error) => {
        console.error('Error executing opencv.py:', error);
      });
  });
}
