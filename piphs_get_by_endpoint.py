import requests
from datetime import datetime, timedelta
import time
import pyperclip

# URL dasar
base_url = "https://www.bi.go.id/hargapangan/WebSite/Home/GetGridData1"

# Daftar komoditas
commodity_list = [
    "1_1",  # Beras Kualitas Bawah I
    "1_2",  # Beras Kualitas Bawah II
    "1_3",  # Beras Kualitas Medium I
    "1_4",  # Beras Kualitas Medium II
    "1_5",  # Beras Kualitas Super I
    "1_6",  # Beras Kualitas Super II
    "2_7",  # Daging Ayam Ras Segar
    "3_8",  # Daging Sapi Kualitas I
    "3_9",  # Daging Sapi Kualitas II
    "4_10", # Telur Ayam Ras Segar
    "5_11", # Bawang Merah Ukuran Sedang
    "6_12", # Bawang Putih Ukuran Sedang
    "7_13", # Cabai Merah Besar
    "7_14", # Cabai Merah Keriting
    "8_15", # Cabai Rawit Hijau
    "8_16", # Cabai Rawit Merah
    "9_17", # Minyak Goreng Curah
    "9_18", # Minyak Goreng Kemasan Bermerk 1
    "9_19", # Minyak Goreng Kemasan Bermerk 2
    "10_20", # Gula Pasir Kualitas Premium
    "10_21"  # Gula Pasir Lokal
]

# Daftar jenis harga
priceType_list = [
    "1",  # Jenis Pasar: Pasar Tradisional
    "2",  # Jenis Pasar: Pasar Modern
    "3",  # Jenis Pasar: Pedagang Besar
    "4"   # Jenis Pasar: Produsen
]

# Parameter tetap
isPasokan = "1"
jenis = "1"
periode = "1"
provId = "22"

# Tanggal mulai dan akhir
start = 1
end = 28

month = 2

start_date = datetime(2023, month, start)
end_date = datetime(2023, month, end)

# Fungsi untuk format tanggal sesuai kebutuhan URL
def format_date(date):
    return date.strftime("%b %%20%d%%2C %%20%Y")

# List untuk menyimpan hasil
data_hasil = []

# Iterasi setiap tanggal
current_date = start_date
iteration = 0

start_time = time.time() # Waktu mulai

while current_date <= end_date:
    formatted_date = format_date(current_date)
    
    # Iterasi setiap priceType
    for priceType in priceType_list:
        # Iterasi setiap commodity
        for commodity in commodity_list:
            # Buat URL dengan parameter yang sesuai
            url = f"{base_url}?tanggal={formatted_date}&commodity={commodity}&priceType={priceType}&isPasokan={isPasokan}&jenis={jenis}&periode={periode}&provId={provId}"
            
            # Lakukan permintaan HTTP
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data['data']:
                    nilai = data['data'][0]['Nilai']  # Mengambil "Nilai" dari hasil
                    # Format nilai menjadi string tanpa desimal
                    formatted_nilai = f"{nilai:.0f}" if isinstance(nilai, float) else str(nilai)
                    # print(f"{formatted_nilai}")
                    # Simpan hasil dengan format yang bisa di-paste ke Excel
                    data_hasil.append(formatted_nilai)
                else:
                    # Tambahkan baris kosong jika tidak ada data
                    data_hasil.append(f"")
            else:
                print(f"Error fetching data for {current_date.strftime('%d-%m-%Y')} for commodity {commodity} and priceType {priceType}")
        
        iteration += 1
        print(f"Iteration: {iteration} completed for date {current_date.strftime('%d-%m-%Y')} and priceType {priceType}")
    
    # Lanjut ke tanggal berikutnya
    current_date += timedelta(days=1)

# Gabungkan semua nilai ke dalam satu string dengan newline sebagai pemisah
nilai_string = "\n".join(data_hasil)

# Salin ke clipboard
pyperclip.copy(nilai_string)
print("Data telah disalin ke clipboard. Silakan paste di Excel.")
print(f"Elapsed time: {time.time() - start_time} seconds")
