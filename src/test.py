import cv2
import mediapipe as mp
import joblib
import numpy as np
import pandas as pd

def normalizar_landmarks(landmarks):
    base_x, base_y, base_z = landmarks[0][0], landmarks[0][1], landmarks[0][2]
    norm = []
    for (x, y, z) in landmarks:
        norm.append((x - base_x, y - base_y, z - base_z))
    return norm

model = joblib.load("model/hand_gesture_model.pkl")
encoder = joblib.load("model/gesture_encoder.pkl")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

UMBRAL_PROB = 0.7
FRAMES_ESTABLES = 4

# Estabilidad por mano
estabilidad = {
    'Left':  {'gesto': None, 'contador': 0},
    'Right': {'gesto': None, 'contador': 0}
}

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=2) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        texto_manos = []

        if results.multi_hand_landmarks:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                coords_raw = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                coords_norm = normalizar_landmarks(coords_raw)
                landmarks = [v for point in coords_norm for v in point]

                feature_names = [f"{coord}{i}" for i in range(21) for coord in ("x", "y", "z")]
                x = pd.DataFrame([landmarks], columns=feature_names)
                
                mano_label = hand_handedness.classification[0].label
                mano_label = "Left" if mano_label == "Right" else "Right"
                x["handedness"] = 1 if mano_label == "Right" else 0

                probs = model.predict_proba(x)[0]
                max_prob = np.max(probs)
                gesture_index = np.argmax(probs)

                if max_prob < UMBRAL_PROB:
                    gesture = "Sin gesto"
                else:
                    gesture = encoder.inverse_transform([gesture_index])[0]

                # Estabilidad por mano
                if gesture == estabilidad[mano_label]['gesto']:
                    estabilidad[mano_label]['contador'] += 1
                else:
                    estabilidad[mano_label]['contador'] = 0
                    estabilidad[mano_label]['gesto'] = gesture

                if estabilidad[mano_label]['contador'] >= FRAMES_ESTABLES:
                    texto_manos.append(f"{mano_label}: {gesture}")
                else:
                    texto_manos.append(f"{mano_label}: Detectando...")
        else:
            texto_manos.append("No hay manos detectadas")

        flipped = cv2.flip(image, 1)
        y0 = 50
        for i, texto in enumerate(texto_manos):
            cv2.putText(flipped, texto, (30, y0 + i*40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('MediaPipe Hands', flipped)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
