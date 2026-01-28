from PIL import Image
import os

# Целевой размер изображений (в пикселях)
TARGET_WIDTH = 100
TARGET_HEIGHT = 100

# Путь к папке с исходными изображениями
ASSETS_DIR = "assets"

for filename in os.listdir(ASSETS_DIR):
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
        filepath = os.path.join(ASSETS_DIR, filename)
        
        try:
            # Открываем изображение
            img = Image.open(filepath)
            
            # Приводим к целевому размеру (с сохранением пропорций и центрированием)
            img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)
            
            # Создаём новое изображение с прозрачным фоном и размещаем в центре
            new_img = Image.new('RGBA', (TARGET_WIDTH, TARGET_HEIGHT), (0, 0, 0, 0))
            new_img.paste(
                img,
                ((TARGET_WIDTH - img.width) // 2,
                 (TARGET_HEIGHT - img.height) // 2)
            )
            
            # Формируем имя выходного файла
            new_filename = filename.rsplit('.', 1)[0] + ".png"
            new_filepath = os.path.join(ASSETS_DIR, new_filename)
            
            # Сохраняем в PNG
            new_img.save(new_filepath, "PNG")
            print(f"Конвертировано и масштабировано: {filename} → {new_filename}")

        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")
