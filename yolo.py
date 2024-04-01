"""
Module for detecting parking spots using YOLOv5
"""
"""import pickle
import torch
from PIL import Image
import cv2
import numpy as np
 
# Load the YOLOv5 model
MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

# Load the saved image with the drawn regions
IMAGE = Image.open("./source/parkingfront.jpg")
 
# Convert the image to a numpy array
IMAGE_NP = np.array(IMAGE)
 
# Inference
RESULTS = MODEL(IMAGE_NP)
 
# Load the saved points
with open("carSpots.pkl", "rb") as file:
    POINTS = pickle.load(file)
 
# Convert the points to a numpy array and calculate centroids
POINTS_NP = [np.array(point_group) for point_group in POINTS]
ANNOTATED_CENTROIDS = [
    (int(np.mean(point_group[:, 0])), int(np.mean(point_group[:, 1])))
    for point_group in POINTS_NP
]
 
# Map centroids to their corresponding points for faster lookup
CENTROID_TO_POINTS = dict(zip(ANNOTATED_CENTROIDS, POINTS_NP))
 
# Set of vehicle classes for faster lookup
VEHICLE_CLASSES = {2, 3, 7}

 
# Count the number of detected cars in each region
TOTAL_CARS = 0  # Total number of detected cars
COUNTED_BOXES = []  # List to keep track of counted boxes
for *box, conf, cls in RESULTS.xyxy[0]:
    if int(cls) in VEHICLE_CLASSES:  # Check if the detected object is a car, motorcycle, truck
        # Get the centroid of the detected car bounding box
        centroid_x = int((box[0] + box[2]) / 2)
        centroid_y = int((box[1] + box[3]) / 2)
        # Check if the centroid falls within any of the annotated regions
        for annotated_centroid in ANNOTATED_CENTROIDS:
            if cv2.pointPolygonTest(
                CENTROID_TO_POINTS[annotated_centroid], (centroid_x, centroid_y), False
            ) >= 0:
                # Check if the box overlaps with any previously counted box
                for counted_box in COUNTED_BOXES:
                    xA = max(box[0], counted_box[0])
                    yA = max(box[1], counted_box[1])
                    xB = min(box[2], counted_box[2])
                    yB = min(box[3], counted_box[3])
                    # Compute the area of intersection
                    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
                    # Compute the area of both the prediction and ground-truth rectangles
                    boxAArea = (box[2] - box[0] + 1) * (box[3] - box[1] + 1)
                    boxBArea = (counted_box[2] - counted_box[0] + 1) * (counted_box[3] - counted_box[1] + 1)
                    # Compute the intersection over union
                    iou = interArea / float(boxAArea + boxBArea - interArea)
                    # If overlap is more than 50%, it's probably the same vehicle
                    if iou > 0.5:
                        break
                else:
                    TOTAL_CARS += 1
                    COUNTED_BOXES.append(box)
                break  # Break once a match is found to avoid double counting
 
# Print and display the results
RESULTS.print()  # print results to console
RESULTS.show()  # display results
 
# Calculate the number of free parking spots
TOTAL_SPOTS = 24  # Total number of parking spots
FREE_SPOTS = TOTAL_SPOTS - TOTAL_CARS
print(f"Total parking spots: {TOTAL_SPOTS}")
print(f"Total detected cars: {TOTAL_CARS}")
print(f"Free parking spots: {FREE_SPOTS}")"""

import cv2
import numpy as np
import pickle
import torch
import time

# Load the YOLOv5 model
MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

# Load the saved points
with open("carSpots.pkl", "rb") as file:
    POINTS = pickle.load(file)

# Convert the points to a numpy array and calculate centroids
POINTS_NP = [np.array(point_group) for point_group in POINTS]
ANNOTATED_CENTROIDS = [
    (int(np.mean(point_group[:, 0])), int(np.mean(point_group[:, 1])))
    for point_group in POINTS_NP
]

# Map centroids to their corresponding points for faster lookup
CENTROID_TO_POINTS = dict(zip(ANNOTATED_CENTROIDS, POINTS_NP))

# Set of vehicle classes for faster lookup
VEHICLE_CLASSES = {2, 3, 7}

# Open the video file
VIDEO_PATH = './source/jerenAutot.mp4'
cap = cv2.VideoCapture(VIDEO_PATH)

# Calculate the delay based on the video's frame rate
frame_rate = cap.get(cv2.CAP_PROP_FPS)
delay = 0.7 / frame_rate

# Variables to capture frames every 30 seconds
FRAME_INTERVAL = 5  # Capture frame every 30 seconds in real-time
last_frame_time = time.time()

# Load the image and get its size
image = cv2.imread("./source/jerenAutot.jpg")
image_height, image_width = image.shape[:2]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to match the size of the image
    frame = cv2.resize(frame, (image_width, image_height))

    # Display the video feed
    cv2.imshow('Video Feed', frame)

    # Resize the window
    WINDOW_WIDTH = 1917
    WINDOW_HEIGHT = 1045
    cv2.resizeWindow('Video Feed', WINDOW_WIDTH, WINDOW_HEIGHT)
    # Process frame every 30 seconds in real-time
    if time.time() - last_frame_time >= FRAME_INTERVAL:
        last_frame_time = time.time()

        # Perform object detection using YOLOv5
        results = MODEL(frame)
        #results.print()
        #results.show()

        # Count the number of detected cars in each region
        TOTAL_CARS = 0  # Total number of detected cars
        COUNTED_BOXES = []  # List to keep track of counted boxes
        for *box, conf, cls in results.xyxy[0]:
            class_id = int(cls)
            class_name = MODEL.names[class_id]
            print(f"Detected a {class_name} with confidence {conf}")
            if int(cls) in VEHICLE_CLASSES:  # Check if the detected object is a car, motorcycle, truck
                # Get the centroid of the detected car bounding box
                centroid_x = int((box[0] + box[2]) / 2)
                centroid_y = int((box[1] + box[3]) / 2)
                # Check if the centroid falls within any of the annotated regions
                for annotated_centroid in ANNOTATED_CENTROIDS:
                    if cv2.pointPolygonTest(
                        CENTROID_TO_POINTS[annotated_centroid], (centroid_x, centroid_y), False
                    ) >= 0:
                        # Check if the box overlaps with any previously counted box
                        for counted_box in COUNTED_BOXES:
                            xA = max(box[0], counted_box[0])
                            yA = max(box[1], counted_box[1])
                            xB = min(box[2], counted_box[2])
                            yB = min(box[3], counted_box[3])
                            # Compute the area of intersection
                            interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
                            # Compute the area of both the prediction and ground-truth rectangles
                            boxAArea = (box[2] - box[0] + 1) * (box[3] - box[1] + 1)
                            boxBArea = (counted_box[2] - counted_box[0] + 1) * (counted_box[3] - counted_box[1] + 1)
                            # Compute the intersection over union
                            iou = interArea / float(boxAArea + boxBArea - interArea)
                            # If overlap is more than 50%, it's probably the same vehicle
                            if iou > 0.5:
                                break
                        else:
                            TOTAL_CARS += 1
                            COUNTED_BOXES.append(box)
                        break  # Break once a match is found to avoid double counting
        # Calculate the number of free parking spots
        TOTAL_SPOTS = 5  # Total number of parking spots
        FREE_SPOTS = TOTAL_SPOTS - TOTAL_CARS
        print(f"Total parking spots: {TOTAL_SPOTS}")
        print(f"Total detected cars: {TOTAL_CARS}")
        print(f"Free parking spots: {FREE_SPOTS}")                
    time.sleep(delay)
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()