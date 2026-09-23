# cmos — QR/Data Matrix Scanner

Сканер QR-кодов и Data Matrix с веб-камеры на OpenCV: распознаёт коды в
реальном времени, обводит их рамкой и выводит содержимое в консоль.

## Возможности

- `main.py` — видеопоток с камеры + распознавание QR-кодов (pyzbar);
- `decode.py` — то же с упором на Data Matrix (pylibdmtx) и выравниванием
  наклона изображения;
- тестовые изображения `cnpt.png`, `kent.png` — образцы кодов для проверки
  без камеры.

## Установка (Windows)

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```sh
python main.py      # QR-сканер с камеры; выход — клавиша q
python decode.py    # Data Matrix с камеры
```

Номер камеры задаётся в `camera_index` (по умолчанию 0).

## Лицензия

MIT — см. [LICENSE](LICENSE).
