"""
Module for detecting parking spots using YOLOv5
"""
import pickle
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
TOTAL_SPOTS = 30  # Total number of parking spots
FREE_SPOTS = TOTAL_SPOTS - TOTAL_CARS
print(f"Total parking spots: {TOTAL_SPOTS}")
print(f"Total detected cars: {TOTAL_CARS}")
print(f"Free parking spots: {FREE_SPOTS}")
