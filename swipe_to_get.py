import pyautogui as pg
import keyboard
import time
import sys
import re  # Import regex module
import pandas as pd  # Import pandas for handling data
import utils.helper as hp
import prototypes.get_weekly as gw

awalan = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

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
    print(f"Region: {region}")
    return region

# Nama komoditas
nama_komoditas = input("Masukkan nama komoditas: ")

# Rate
rate = input("Masukkan rate: ")

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

# Mendapatkan region tanggal (statis)
region_date = get_region()

# Memulai pada posisi awal
pg.click(pos)
print('Inisialisasi selesai, mulai gerakan kursor...')
time.sleep(1)

# Menghitung jarak yang harus ditempuh dalam piksel
distance = pos2[0] - pos[0]

# Variabel untuk menyimpan deteksi tanggal sebelumnya
previous_date_detected = ""

# Variabel untuk menyimpan data hasil deteksi
data = {
    "TANGGAL": [],
    "KOMODITAS": [],
    "HARGA": [],
    "RATE": []
}

# Fungsi untuk memfilter tanggal dari teks berdasarkan awalan
def filter_date(text, awalan):
    words = text.split()
    for i in range(len(words) - 2):  # Pastikan ada cukup kata untuk membentuk tanggal
        if words[i] in awalan:
            date_candidate = " ".join(words[i:i+3])
            if re.match(r'^[A-Za-z]{3} \d{2} \d{4}$', date_candidate):
                return date_candidate
    return None

# Loop untuk menggerakkan kursor dari posisi awal ke posisi akhir
for x_offset in range(0, distance, 2):  # Mengubah posisi x setiap 1 piksel
    # Menggerakkan kursor
    pg.dragTo(pos[0] + x_offset, pos[1], duration=0.2)

    # Memeriksa jika tombol 'q' ditekan untuk keluar
    if keyboard.is_pressed('q'):
        print('Program dihentikan oleh pengguna.')
        sys.exit(1)

    # Mengambil teks dari region harga
    detected_text = hp.get_text_from_region(region_price, config="--psm 7 --oem 1 -l eng", save_debug=False)

    # Mengambil teks dari region tanggal
    detected_date = hp.get_text_from_region(region_date, config="--psm 7 --oem 1", save_debug=False)
    print(detected_date)
    
    # Filter tanggal yang valid dari teks yang terdeteksi
    valid_date = filter_date(detected_date, awalan)

    # Hanya mencetak jika deteksi tanggal berbeda dari iterasi sebelumnya dan valid
    if valid_date and valid_date != previous_date_detected:
        # Menggunakan regex untuk mengambil angka dari kata ketiga dalam teks harga
        price_match = re.search(r'\b\d+(\.\d+)?\b', detected_text.split()[3])
        # price_value = price_match.group(0).replace('.', '') if price_match else 'N/A'
        price_value = price_match.group(0).replace('.', '.') if price_match else 'N/A'

        print(f'Deteksi tanggal baru: {valid_date}')
        print(f'Deteksi harga: {price_value}')

        # Memperbarui deteksi tanggal sebelumnya
        previous_date_detected = valid_date

        # Menyimpan hasil deteksi ke dalam variabel data
        data["TANGGAL"].append(valid_date)
        data["KOMODITAS"].append(nama_komoditas)  # Sesuaikan dengan jenis komoditas yang Anda deteksi
        data["HARGA"].append(price_value)
        data["RATE"].append(rate) # Sesuaikan dengan rate yang Anda deteksi

    time.sleep(0.3)  # Jeda untuk menjaga kursor tetap aktif dan memicu hover

# Setelah loop selesai, menyimpan hasil ke file Excel
df = pd.DataFrame(data)
df.to_excel(f'hasil_deteksi_{nama_komoditas}.xlsx', index=False)

print("Program selesai dan data telah disimpan ke file hasil_deteksi.xlsx.")
