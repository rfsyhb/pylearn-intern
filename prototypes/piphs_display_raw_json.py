import requests
from datetime import datetime, timedelta
import time
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

# Iterasi setiap tanggal
current_date = start_date

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
                    # Print seluruh data JSON yang didapatkan
                    print(json.dumps(data, indent=2))
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                    print("Response text:", response.text)  # Output respons untuk membantu debugging
            else:
                print(f"Error fetching data for {current_date.strftime('%d-%m-%Y')} with commodity {commodity} and priceType {priceType}")
    
    # Lanjut ke tanggal berikutnya
    current_date += timedelta(days=1)
