import requests
from datetime import datetime, timedelta
import time
import pyperclip
from plyer import notification
import json

# Parameter URL
prov_id = 22
reg_id = 0
is_pasokan = 1

# Dictionary komoditas dengan kode sebagai key dan deskripsi sebagai value
commodity_dict = {
    "1_1": "Beras Kualitas Bawah I",
    "1_2": "Beras Kualitas Bawah II",
    "1_3": "Beras Kualitas Medium I",
    "1_4": "Beras Kualitas Medium II",
    "1_5": "Beras Kualitas Super I",
    "1_6": "Beras Kualitas Super II",
    "2_7": "Daging Ayam Ras Segar",
    "3_8": "Daging Sapi Kualitas I",
    "3_9": "Daging Sapi Kualitas II",
    "4_10": "Telur Ayam Ras Segar",
    "5_11": "Bawang Merah Ukuran Sedang",
    "6_12": "Bawang Putih Ukuran Sedang",
    "7_13": "Cabai Merah Besar",
    "7_14": "Cabai Merah Keriting",
    "8_15": "Cabai Rawit Hijau",
    "8_16": "Cabai Rawit Merah",
    "9_17": "Minyak Goreng Curah",
    "9_18": "Minyak Goreng Kemasan Bermerk 1",
    "9_19": "Minyak Goreng Kemasan Bermerk 2",
    "10_20": "Gula Pasir Kualitas Premium",
    "10_21": "Gula Pasir Lokal"
}

# Dictionary priceType dengan kode sebagai key dan deskripsi sebagai value
priceType_dict = {
    "1": "Pasar Tradisional",
    "2": "Pasar Modern",
    "3": "Pedagang Besar",
    "4": "Produsen"
}

# Definisi rentang tanggal
year = int(input("Masukkan tahun (ex: 2023): "))
month_list = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5,
    "Juni": 6, "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10,
    "November": 11, "Desember": 12
}
print(", ".join(list(month_list.keys())))
selected_month = input("Masukkan nama bulan (huruf pertama kapital): ")
month = month_list[selected_month]

start = 1
end = int(input("Masukkan tanggal akhir: "))

start_date = datetime(year, month, start)
end_date = datetime(year, month, end)

# Fungsi untuk format tanggal sesuai kebutuhan URL
def format_date(date):
    return date.strftime("%b %%20%d%%2C %%20%Y")

# List untuk menyimpan hasil data
output_data = []

# Iterasi setiap tanggal
current_date = start_date
iteration = 0

start_time = time.time()  # Waktu mulai

while current_date <= end_date:
    formatted_date = format_date(current_date)

    # Iterasi setiap priceType dan commodity
    for priceType, priceTypeDesc in priceType_dict.items():
        for commodity, description in commodity_dict.items():
            # Buat URL dengan parameter yang sesuai
            url = f"https://www.bi.go.id/hargapangan/Website/Home/GetDetailGridData?ProvId={prov_id}&RegId={reg_id}&PriceTypeId={priceType}&CatId={commodity}&date={formatted_date}&isPasokan={is_pasokan}&_=1724939729406"
            
            # Log informasi URL dan parameter
            print(f"Fetching data for URL: {url}")

            # Mengambil data dari endpoint
            response = requests.get(url)

            # Periksa apakah respons sukses
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Penanda untuk memeriksa apakah data untuk masing-masing kota ditemukan
                    palangkaraya_found = False
                    sampit_found = False

                    # Proses data untuk 'Kota Palangkaraya' dan 'Kota Sampit'
                    for entry in data["data"]:
                        if entry["name"] == "Kota Palangkaraya":
                            harga = entry.get(current_date.strftime("%d/%m/%Y"), "")
                            print(f"Data ditemukan untuk Kota Palangkaraya pada tanggal {current_date.strftime('%d/%m/%Y')}, commodity {description}, priceType {priceTypeDesc}: Harga {harga}")
                            output_data.append({
                                "TANGGAL": current_date.strftime("%d/%m/%Y"),
                                "KOTA_KAB": entry["name"],
                                "CAT_ID": description,  # Menggunakan deskripsi komoditas
                                "PRICE_TYPE": priceTypeDesc,  # Menambahkan deskripsi priceType
                                "HARGA_SAT": harga  # Biarkan kosong jika tidak ada data
                            })
                            palangkaraya_found = True
                        elif entry["name"] == "Kota Sampit":
                            harga = entry.get(current_date.strftime("%d/%m/%Y"), "")
                            print(f"Data ditemukan untuk Kota Sampit pada tanggal {current_date.strftime('%d/%m/%Y')}, commodity {description}, priceType {priceTypeDesc}: Harga {harga}")
                            output_data.append({
                                "TANGGAL": current_date.strftime("%d/%m/%Y"),
                                "KOTA_KAB": entry["name"],
                                "CAT_ID": description,  # Menggunakan deskripsi komoditas
                                "PRICE_TYPE": priceTypeDesc,  # Menambahkan deskripsi priceType
                                "HARGA_SAT": harga  # Biarkan kosong jika tidak ada data
                            })
                            sampit_found = True
                    
                    # Jika tidak ada data untuk kota tersebut, tambahkan baris kosong
                    if not palangkaraya_found:
                        print(f"Tidak ada data ditemukan untuk Kota Palangkaraya pada tanggal {current_date.strftime('%d/%m/%Y')}, commodity {description}, priceType {priceTypeDesc}")
                        output_data.append({
                            "TANGGAL": current_date.strftime("%d/%m/%Y"),
                            "KOTA_KAB": "Kota Palangkaraya",
                            "CAT_ID": description,
                            "PRICE_TYPE": priceTypeDesc,
                            "HARGA_SAT": ""
                        })
                    if not sampit_found:
                        print(f"Tidak ada data ditemukan untuk Kota Sampit pada tanggal {current_date.strftime('%d/%m/%Y')}, commodity {description}, priceType {priceTypeDesc}")
                        output_data.append({
                            "TANGGAL": current_date.strftime("%d/%m/%Y"),
                            "KOTA_KAB": "Kota Sampit",
                            "CAT_ID": description,
                            "PRICE_TYPE": priceTypeDesc,
                            "HARGA_SAT": ""
                        })

                    print("")  # Tambahkan baris kosong untuk memisahkan setiap iterasi

                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                    print("Response text:", response.text)  # Output respons untuk membantu debugging
            else:
                print(f"Error fetching data for {current_date.strftime('%d-%m-%Y')} with commodity {commodity} and priceType {priceType}")
        
        iteration += 1
        print(f"Completed iteration {iteration}: date {current_date.strftime('%d-%m-%Y')}, commodity {commodity}, priceType {priceType}")

    # Lanjut ke tanggal berikutnya
    current_date += timedelta(days=1)

# Mengurutkan data berdasarkan 'KOTA_KAB' sehingga 'Kota Palangkaraya' muncul terlebih dahulu
output_data.sort(key=lambda x: (x['KOTA_KAB'], x['TANGGAL']))

# Format output untuk clipboard
header = "TANGGAL\tKOTA_KAB\tCAT_ID\tPRICE_TYPE\tHARGA_SAT"
output_string = header + "\n" + "\n".join([f"{item['TANGGAL']}\t{item['KOTA_KAB']}\t{item['CAT_ID']}\t{item['PRICE_TYPE']}\t{item['HARGA_SAT']}" for item in output_data])

# Salin ke clipboard
pyperclip.copy(output_string)
print("Data telah disalin ke clipboard dalam format kolom. Silakan paste di Excel.")
print(f"{list(month_list.keys())[list(month_list.values()).index(month)]} finished in {time.time() - start_time} seconds")

notification.notify(
    title=f'Get {selected_month} data finished',
    message='Pengambilan data dari API telah selesai.',
    timeout=10  # durasi notifikasi dalam detik
)
