"""
Script untuk mengambil harga di PIHPS oleh rfsyhb
"""

import utils.helper as hp
import re
import pyautogui
import keyboard
import time
import pyperclip
import time

json_path = './required_data.json'

excel_cell_pos = (1855, 939)

def add_required_locations_and_regions():
    # Mendapatkan posisi untuk price_region
    print("Gerakkan kursor ke sudut kiri atas area price_region dan tekan 's'")
    keyboard.wait('s')
    left_top = pyautogui.position()
    print(f"{left_top}")
    time.sleep(0.5)

    print("Gerakkan kursor ke sudut kanan bawah area price_region dan tekan 's'")
    keyboard.wait('s')
    right_bottom = pyautogui.position()
    print(f"{right_bottom}")
    time.sleep(0.5)

    # Menghitung lebar dan tinggi area price_region
    width = right_bottom[0] - left_top[0]
    height = right_bottom[1] - left_top[1]

    # Menyusun tuple region
    price_region = (left_top[0], left_top[1], width, height)
    print(f"Price region saved: {price_region}\n")
    
    # Mendapatkan posisi untuk list_item_pos
    print("Gerakkan kursor ke posisi List Komoditas dan tekan 's'")
    keyboard.wait('s')
    list_item_pos = pyautogui.position()
    print(f"List item position saved: {list_item_pos}\n")

    # Mendapatkan posisi untuk submit_button_pos
    print("Gerakkan kursor ke posisi Submit Button dan tekan 's'")
    keyboard.wait('s')
    submit_button_pos = pyautogui.position()
    print(f"Submit button position saved: {submit_button_pos}\n")

    # Mendapatkan posisi untuk type_market_pos
    print("Gerakkan kursor ke posisi List Jenis Pasar dan tekan 's'")
    keyboard.wait('s')
    type_market_pos = pyautogui.position()
    print(f"Type market position saved: {type_market_pos}\n")

    # Mengumpulkan semua data dalam dictionary
    all_positions = {
        "price_region": price_region,
        "list_item_pos": list_item_pos,
        "submit_button_pos": submit_button_pos,
        "type_market_pos": type_market_pos
    }

    # Simpan data ke JSON
    hp.save_to_json(all_positions, json_path)
    print("All positions saved to JSON file.")

"""
Prototype awal untuk scan harga satu per satu
Ribet karena harus menyiapkan window excel juga
"""
def one_by_one(data):
    price_region = tuple(data['price_region'])
    list_item_pos = tuple(data['list_item_pos'])
    submit_button_pos = tuple(data['submit_button_pos'])

    while True:
        print('Press s to submit')
        keyboard.wait('s')
        pyautogui.click(submit_button_pos)
        pyautogui.click(excel_cell_pos)
        
        # wait for keyboard click ctrl using keyboard library
        print('Press ctrl to scan price and write')
        keyboard.wait('ctrl')
        pyautogui.press('backspace')
        
        raw_price = hp.get_text_from_region(price_region, config="--psm 7 --oem 1 -l eng", save_debug=True)
        print(raw_price)

        # get the numbers from the string
        numbers = re.findall(r'\d+', raw_price)
        price = ''.join(numbers)

        # type each digit of the price
        for digit in price:
            pyautogui.press(digit)

        pyautogui.press('enter')
        pyautogui.click(list_item_pos)
        time.sleep(0.1)

"""
Versi kedua, total item tidak bernama
Hasil akan tersimpan di clipboard dan bisa langsung ditempelkan ke Excel
"""
def scan_one_day_one_type(data):
    price_region = tuple(data['price_region'])
    list_item_pos = tuple(data['list_item_pos'])
    submit_button_pos = tuple(data['submit_button_pos'])
    
    total_item = 21
    list_price = []

    for i in range(total_item):
        print('Press r to submit')
        keyboard.wait('r')
        pyautogui.click(submit_button_pos)
        
        print('Press s to get price')
        keyboard.wait('s')
        raw_price = hp.get_text_from_region(price_region, config="--psm 7 --oem 1 -l eng", save_debug=True)
        print(raw_price)

        # get the numbers from the string
        numbers = re.findall(r'\d+', raw_price)
        price = ''.join(numbers)
        list_price.append(price)  # Tambahkan harga ke dalam list

        pyautogui.click(list_item_pos)

    # Gabungkan semua harga dengan newline ('\n') untuk format vertikal di Excel
    prices_string = '\n'.join(list_price)
    
    # Simpan ke clipboard
    pyperclip.copy(prices_string)
    print("All prices have been copied to clipboard. You can paste them into Excel now.")

"""
Versi ketiga, scan satu hari penuh untuk semua jenis pasar
"""
def scan_one_day_full(data):
    price_region = tuple(data['price_region'])
    list_item_pos = tuple(data['list_item_pos'])
    submit_button_pos = tuple(data['submit_button_pos'])
    type_market_pos = tuple(data['type_market_pos'])
    
    list_item = [
                    'Beras Bawah I', 'Beras Bawah II', 'Beras Medium I', 'Beras Medium II', 'Beras Super I', 'Beras Super II',
                    'Daging Ayam Segar', 'Sapi Kualitas I', 'Sapi Kualitas II', 'Telur Ayam Ras Segar', 'Bawang Merah Sedang', 'Bawang Putih Sedang',
                    'Cabai Merah Besar', 'Cabai Merah Keriting', 'Cabai Rawit Hijau', 'Cabai Rawit Merah', 'Minyak Goreng Curah', 'Minyak Goreng Bermerk 1', 'Minyak Goreng Bermerk 2',
                    'Gula Pasir Premium', 'Gula Pasir Lokal'
                ]
    total_item = len(list_item)
    list_type = ['Pasar Tradisional', 'Pasar Modern', 'Pedagang Besar', 'Produsen']
    list_price = []

    for i in range(len(list_type)):
        j = 0
        while j < total_item:
            print(f'Current type: {list_type[i]}\ncurrent item: {list_item[j]}')
            
            print('Press "r" to submit, "b" to go back, or any other key to repeat')
            key = keyboard.read_event()
            
            if key.event_type == keyboard.KEY_DOWN and key.name == 'r':
                pyautogui.click(submit_button_pos)
            elif key.event_type == keyboard.KEY_DOWN and key.name == 'b':
                print('Going back to previous item...\n')
                time.sleep(1)
                j = max(0, j - 1)  # Go back to previous iteration, but not below 0
                continue
            elif key.event_type == keyboard.KEY_DOWN:
                print('Repeating current item...\n')
                time.sleep(1)
                continue  # Repeat current iteration
            
            print('Press s to get price')
            keyboard.wait('s')
            raw_price = hp.get_text_from_region(price_region, config="--psm 7 --oem 1 -l eng", save_debug=True)
            print(raw_price)

            # get the numbers from the string
            numbers = re.findall(r'\d+', raw_price)
            price = ''.join(numbers)
            list_price.append(price)  # Tambahkan harga ke dalam list

            pyautogui.click(list_item_pos)

            # Increment item index after processing
            j += 1

        print('Finished, changing type')
        pyautogui.click(type_market_pos)

    # Gabungkan semua harga dengan newline ('\n') untuk format vertikal di Excel
    prices_string = '\n'.join(list_price)
    
    # Simpan ke clipboard
    pyperclip.copy(prices_string)
    print("All prices have been copied to clipboard. You can paste them into Excel now.")

if __name__ == '__main__':
    data = hp.load_from_json(json_path) # Load data from JSON

    select = input("Select:\n0. Add required location and region\n1. One by one\n2. Scan one day one type\n3. Scan one day full\n>>> ")
    
    if select == '0':
        add_required_locations_and_regions()
        print("Please run the script again after adding required locations and regions.")
    elif select == '1':
        one_by_one(data)
    elif select == '2':
        scan_one_day_one_type(data)
    elif select == '3':
        scan_one_day_full(data)
    else:
        print("Invalid selection")