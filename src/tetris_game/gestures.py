import cv2
import mediapipe as mp
import joblib
import numpy as np
import pandas as pd

model = joblib.load("model/hand_gesture_model.pkl")
encoder = joblib.load("model/gesture_encoder.pkl")
scaler = joblib.load("model/hand_scaler.pkl")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2
)

UMBRAL_PROB = 0.8

def normalizar_landmarks(landmarks):
    base_x, base_y, base_z = landmarks[0][0], landmarks[0][1], landmarks[0][2]
    norm = []
    for (x, y, z) in landmarks:
        norm.append((x - base_x, y - base_y, z - base_z))
    return norm

def read_gesture(frame):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    gestures_dict = {"Left": "Sin gesto", "Right": "Sin gesto"}

    if not results.multi_hand_landmarks:
        return gestures_dict

    for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
        coords_raw = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
        coords_norm = normalizar_landmarks(coords_raw)
        landmarks = [v for p in coords_norm for v in p]

        feature_names = [f"{coord}{i}" for i in range(21) for coord in ("x", "y", "z")]
        x = pd.DataFrame([landmarks], columns=feature_names)

        hand_label = hand_handedness.classification[0].label
        mano_real = "Left" if hand_label == "Right" else "Right"

        x["handedness"] = 1 if mano_real == "Right" else 0


        x_scaled = scaler.transform(x)
        probs = model.predict_proba(x_scaled)[0]

        max_prob = np.max(probs)
        if max_prob < UMBRAL_PROB:
            gesture = "Sin gesto"
        else:
            gesture_idx = np.argmax(probs)
            gesture = encoder.inverse_transform([gesture_idx])[0]
        
        gestures_dict[mano_real] = gesture
    
    return gestures_dict