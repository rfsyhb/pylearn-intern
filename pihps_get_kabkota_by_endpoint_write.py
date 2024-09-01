""" Data linked with excel_create_pihps.py variables """

import requests
from datetime import datetime, timedelta
import time
import pyperclip
import json
import excel_create_pihps as ecp
import pymsgbox
import pandas as pd

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
year = ecp.dates["year"]
print(f'year is {year}')

month_list = {
    "Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5,
    "Juni": 6, "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10,
    "November": 11, "Desember": 12
}
print(", ".join(list(month_list.keys())))
selected_month = input("Masukkan nama bulan (huruf pertama kapital): ")
month = month_list[selected_month]

start = 1
end = int(ecp.dates["month"][selected_month])
print(f'end month is {end}')

start_date = datetime(year, month, start)
end_date = datetime(year, month, end)

def format_date(date):
    return date.strftime("%b%%20%d%%2C%%20%Y")

output_data = []
current_date = start_date
iteration = 0

start_time = time.time()

while current_date <= end_date:
    formatted_date = format_date(current_date)
    for priceType, priceTypeDesc in priceType_dict.items():
        for commodity, description in commodity_dict.items():
            url = f"https://www.bi.go.id/hargapangan/Website/Home/GetDetailGridData?ProvId={prov_id}&RegId={reg_id}&PriceTypeId={priceType}&CatId={commodity}&date={formatted_date}&isPasokan={is_pasokan}&_=1724939729406"
            print(f"Fetching data for URL: {url}")

            response = requests.get(url)

            if response.status_code == 200:
                try:
                    data = response.json()
                    palangkaraya_found = False
                    sampit_found = False

                    for entry in data["data"]:
                        if entry["name"] == "Kota Palangkaraya":
                            harga = entry.get(current_date.strftime("%d/%m/%Y"), "")
                            if harga:
                                harga = f"{float(harga):.0f}"
                            print(f"Data ditemukan untuk Kota Palangkaraya pada tanggal {current_date.strftime('%Y-%m-%d')}, commodity {description}, priceType {priceTypeDesc}: Harga {harga}")
                            output_data.append({
                                "TANGGAL": current_date.strftime("%Y-%m-%d"),
                                "KOTA_KAB": entry["name"],
                                "CAT_ID": description,
                                "PRICE_TYPE": priceTypeDesc,
                                "HARGA_SAT": harga
                            })
                            palangkaraya_found = True
                        elif entry["name"] == "Kota Sampit":
                            harga = entry.get(current_date.strftime("%d/%m/%Y"), "")
                            if harga:
                                harga = f"{float(harga):.0f}"
                            print(f"Data ditemukan untuk Kota Sampit pada tanggal {current_date.strftime('%Y-%m-%d')}, commodity {description}, priceType {priceTypeDesc}: Harga {harga}")
                            output_data.append({
                                "TANGGAL": current_date.strftime("%Y-%m-%d"),
                                "KOTA_KAB": entry["name"],
                                "CAT_ID": description,
                                "PRICE_TYPE": priceTypeDesc,
                                "HARGA_SAT": harga
                            })
                            sampit_found = True
                    
                    if not palangkaraya_found:
                        print(f"Tidak ada data ditemukan untuk Kota Palangkaraya pada tanggal {current_date.strftime('%Y-%m-%d')}, commodity {description}, priceType {priceTypeDesc}")
                        output_data.append({
                            "TANGGAL": current_date.strftime("%Y-%m-%d"),
                            "KOTA_KAB": "Kota Palangkaraya",
                            "CAT_ID": description,
                            "PRICE_TYPE": priceTypeDesc,
                            "HARGA_SAT": ""
                        })
                    if not sampit_found:
                        print(f"Tidak ada data ditemukan untuk Kota Sampit pada tanggal {current_date.strftime('%Y-%m-%d')}, commodity {description}, priceType {priceTypeDesc}")
                        output_data.append({
                            "TANGGAL": current_date.strftime("%Y-%m-%d"),
                            "KOTA_KAB": "Kota Sampit",
                            "CAT_ID": description,
                            "PRICE_TYPE": priceTypeDesc,
                            "HARGA_SAT": ""
                        })

                    print("")

                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                    print("Response text:", response.text)
            else:
                print(f"Error fetching data for {current_date.strftime('%Y-%m-%d')} with commodity {commodity} and priceType {priceType}")
        
        iteration += 1
        print(f"Completed iteration {iteration}: date {current_date.strftime('%Y-%m-%d')}, commodity {commodity}, priceType {priceType}")

    current_date += timedelta(days=1)

output_data.sort(key=lambda x: (x['TANGGAL'], x['KOTA_KAB']))

# Mengonversi data menjadi DataFrame
df = pd.DataFrame(output_data)

# Menyimpan DataFrame ke file Excel
output_filename = f"data_pihps_{selected_month}_{year}.xlsx"
df.to_excel(output_filename, index=False)

print(f"Data telah disimpan ke {output_filename}.")

pymsgbox.alert(f'Get {selected_month} data finished.', 'Finished')
