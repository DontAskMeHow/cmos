import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Используем нужный индекс камеры (замени на правильный, если нужно)
camera_index = 0  # Убедись, что этот индекс соответствует нужной камере

print(f"Используется камера с индексом: {camera_index}")
cap = cv2.VideoCapture(camera_index, cv2.CAP_MSMF)
if not cap.isOpened():
    print("❌ Не удалось открыть камеру")
    exit()

def draw_detected_code(frame, decoded_objects):
    """ Рисует зеленые прямоугольники вокруг обнаруженных кодов и выводит их значения. """
    for obj in decoded_objects:
        points = obj.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=3)
        
        text = obj.data.decode("utf-8")
        x, y = obj.rect.left, obj.rect.top
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        print(f"Обнаружен код: {text}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка при получении кадра")
        break

    decoded_objects = decode(frame)
    draw_detected_code(frame, decoded_objects)

    cv2.imshow("QR и Data Matrix Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
