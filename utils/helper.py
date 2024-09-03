import pyautogui as pg
import pytesseract as pt
from PIL import Image, ImageEnhance
import json
import os
import keyboard

def preprocess_image(image, save_debug=False):
    # Hanya lakukan langkah yang diperlukan
    image = image.convert("L")
    image = image.point(lambda p: p > 128 and 255)
    
    # Optional: Sesuaikan nilai enhance hanya jika diperlukan
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    if save_debug:
        image.save("img/debugs/processed_image.png")  # Save for debugging

    return image

def get_text_from_region(region, config="", save_debug=False):
    screenshot = pg.screenshot(region=region)
    if save_debug:
        screenshot.save("img/debugs/get_text_debug_region.png")  # Save screenshot for debugging
    
    image = preprocess_image(screenshot, save_debug=save_debug)
    text = pt.image_to_string(image, config=config)
    return text

def save_to_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_from_json(path):
    # Cek apakah file ada
    if not os.path.exists(path):
        print(f"File '{path}' tidak ditemukan. Pastikan untuk menjalankan 'Add required location and region' terlebih dahulu.")
        return None
    
    # Cek apakah file kosong
    if os.path.getsize(path) == 0:
        print(f"File '{path}' kosong. Pastikan untuk menjalankan 'Add required location and region' terlebih dahulu.")
        return None

    try:
        with open(path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"File '{path}' tidak berisi data JSON yang valid.")
        return None
    
def get_region():
    print('Taruh kursor ke sudut kiri atas area, jika sudah tekan "s"')
    keyboard.wait('s')
    left_top = pg.position()

    print('Taruh kursor ke sudut kanan bawah area, jika sudah tekan "s"')
    keyboard.wait('s')
    right_bottom = pg.position()

    width = right_bottom[0] - left_top[0]
    height = right_bottom[1] - left_top[1]

    region = (left_top[0], left_top[1], width, height)
    print(f"region: {region}")
    return region