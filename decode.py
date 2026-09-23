import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode as decode_dm

# Запуск видеопотока
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Не удалось открыть камеру")
    exit()

def deskew_image(image):
    """Исправление наклона изображения путем нахождения минимального прямоугольника вокруг кода."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return image  # Если контуров нет, возвращаем оригинальное изображение
    
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    angle = rect[-1]
    if angle < -45:
        angle += 90
    
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, rotation_matrix, (w, h), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def preprocess_image(image):
    """Предобработка изображения: коррекция наклона, бинаризация, шумоподавление."""
    image = deskew_image(image)  # Исправление наклона
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Усиление контраста
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # Бинаризация
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Морфологические преобразования для уменьшения шума
    kernel = np.ones((3, 3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return morph

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка при получении кадра")
        break
    
    processed_frame = preprocess_image(frame)
    decoded_dm = decode_dm(processed_frame)
    
    if decoded_dm:
        for obj in decoded_dm:
            print(f"✅ Data Matrix: {obj.data.decode('utf-8')}")
    
    combined_frame = np.hstack((cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), processed_frame))
    cv2.imshow("Исходное и обработанное изображение", combined_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
