# Park-Spotter
This repository contains code for parking area car detection application. This contains both server backend and expo application code used to see available spots and get notifications on your phone while driving to work. To use the project you will need a server to run the code on and an IP camera. We used Azure for a VM and ran the backend code there. 

The project uses a pre-trained machine learning model to search for cars in the image provided by the camera. The current model in use is <a href="https://docs.ultralytics.com/">YOLOv8 by Ultralytics</a>. In our project code the video feed doesn't get saved or uploaded to anywhere and is only processed from the live feed. Ultralytics might collect some usage data and you can read more about it <a href="https://docs.ultralytics.com/help/privacy/">here</a>.

## How to get started with the project 

### Download python 
https://www.python.org/downloads/
Version need to be >= 3.9.x

### Clone repository
```
git clone https://github.com/JerbsH/Park-Spotter.git
```
### Starting the application
Use the correct starting script based on your server operating system.
#### Unix based system
```
bash startapp.sh
```
#### Windows system
```
.\startapp.bat
```


