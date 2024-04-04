import sys
import time
import os
import cv2
import torch
from dotenv import load_dotenv

load_dotenv()

try:
    MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)
except Exception as e:
    print(f"Error loading model: {e}", file=sys.stderr)
    sys.exit(1)

VEHICLE_CLASSES = {2, 3, 7}  # Car, motorcycle, truck

try:
    VIDEO_PATH = os.getenv('SECURE_URL')
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        raise ValueError("Could not open video file.")
except Exception as e:
    print(f"Error opening video file: {e}", file=sys.stderr)
    sys.exit(1)

# Print video size, image size, and frame rate
print(f"Video size: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
print(f"Frame rate: {cap.get(cv2.CAP_PROP_FPS)}")
FRAME_INTERVAL = 5
last_frame_time = time.time()


# Create a resizable window
#cv2.namedWindow('Video Feed', cv2.WINDOW_NORMAL)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    #cv2.imshow('Video Feed', frame)
    if time.time() - last_frame_time >= FRAME_INTERVAL:
        last_frame_time = time.time()

        results = MODEL(frame)
        results.print()

        TOTAL_CARS = 0
        for *box, conf, cls in results.xyxy[0]:
            class_id = int(cls)
            class_name = MODEL.names[class_id]
            print(f"Detected a {class_name} with confidence {conf}")
            if int(cls) in VEHICLE_CLASSES and conf >= 0.4:
                TOTAL_CARS += 1

        # Calculate the number of free parking spots
        TOTAL_SPOTS = 8  # Total number of parking spots
        FREE_SPOTS = TOTAL_SPOTS - TOTAL_CARS
        print(f"Total parking spots: {TOTAL_SPOTS}")
        print(f"Total detected cars: {TOTAL_CARS}")
        print(f"Free parking spots: {FREE_SPOTS}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#results.show()
cap.release()
#cv2.destroyAllWindows()
