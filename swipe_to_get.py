import pyautogui as pg
import keyboard
import time
import sys
import utils.helper as hp
import get_weekly as gw

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

# Mendapatkan posisi awal
print('Klik "s" untuk mendapatkan posisi awal.')
keyboard.wait('s')
pos = pg.position()
print(f'Posisi awal: {pos}')

# Mendapatkan posisi akhir
print('Klik "e" untuk mendapatkan posisi akhir.')
keyboard.wait('e')
pos2 = pg.position()
print(f'Posisi akhir: {pos2}')

# Mendapatkan region price
region_price = get_region()

# Mendapatkan region tanggal
region_date = get_region()

# Memulai pada posisi awal
pg.click(pos)
print('Inisialisasi selesai, mulai gerakan kursor...')
time.sleep(1)

# Menghitung jarak yang harus ditempuh dalam piksel
distance = pos2[0] - pos[0]

# Loop untuk menggerakkan kursor dari posisi awal ke posisi akhir
for x_offset in range(0, distance, 1):  # Mengubah posisi x setiap 1 piksel
    # Menggerakkan kursor dan memperbarui region_date
    pg.dragTo(pos[0] + x_offset, pos[1], duration=0.2)

    # Memperbarui posisi region_date secara relatif terhadap pergerakan kursor
    region_date = (region_date[0] + 1, region_date[1], region_date[2], region_date[3])

    # Memeriksa jika tombol 'q' ditekan untuk keluar
    if keyboard.is_pressed('q'):
        print('Program dihentikan oleh pengguna.')
        sys.exit(1)

    # Mengambil teks dari region harga
    detected_text = hp.get_text_from_region(region_price, config="--psm 7 --oem 1 -l eng", save_debug=True)
    print(f'Deteksi harga: {detected_text}')
    
    # Mengambil teks dari region tanggal
    detected_date = hp.get_text_from_region(region_date, config="--psm 7 --oem 1 -l eng", save_debug=True)
    print(f'Deteksi tanggal: {detected_date}')

    time.sleep(0.3)  # Jeda untuk menjaga kursor tetap aktif dan memicu hover

print("Program selesai.")
