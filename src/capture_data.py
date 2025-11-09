import cv2
import mediapipe as mp
import os
import csv
import time

def normalizar_landmarks(landmarks):
    base_x, base_y, base_z = landmarks[0][0], landmarks[0][1], landmarks[0][2]
    norm = []
    for (x, y, z) in landmarks:
        norm.append((x - base_x, y - base_y, z - base_z))
    return norm


mp_hands = mp.solutions.hands
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

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error leyendo el frame.")
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )

            coords_raw  = [(lm.x, lm.y, lm.z) for lm in hand.landmark]
            coords_norm = normalizar_landmarks(coords_raw)
            coords      = [v for point in coords_norm for v in point]

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                with open(filename, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([gesture_name] + coords)
                print("Muestra capturada")
                time.sleep(0.3)

    cv2.imshow("Captura de gesto", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

