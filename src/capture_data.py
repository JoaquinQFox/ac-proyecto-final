import cv2
import mediapipe as mp
import os
import csv
import time

mp_hands = mp.solutions
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1,
    min_detection_confidence = 0.6,
    min_tracking_confidence = 0.6
)


gesture_name = input("Nombre del gesto: ")
os.makedirs("data", exist_ok=True)
filename = f"data/{gesture_name}.csv"

if not os.path.isfile(filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["gesture"] + [f"{coord}{i}" for i in range(21) for coord in ("x", "y", "z")]
        writer.writerow(header)


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

print("Presiona 's' para capturar datos, 'q' para salir.")



