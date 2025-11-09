import cv2
import mediapipe as mp
import joblib
import numpy as np

# Cargar modelo y encoder
model = joblib.load("model/hand_gesture_model.pkl")
encoder = joblib.load("model/gesture_encoder.pkl")

# Inicializar variables de detección
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

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

                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])

                x = np.array(landmarks).reshape(1, -1)
                y_pred = model.predict(x)
                gesture = encoder.inverse_transform(y_pred)[0]

                mano = hand_handedness.classification[0].label
                texto_manos.append(f"{mano}: {gesture}")
                

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