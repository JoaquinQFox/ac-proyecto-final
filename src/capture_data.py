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




