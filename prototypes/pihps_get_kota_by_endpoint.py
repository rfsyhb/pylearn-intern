import requests
import json
from datetime import datetime, timedelta

# Parameter URL
prov_id = 22
reg_id = 0
price_type_id = 1
cat_id = 1
is_pasokan = 1

# Definisi rentang tanggal
start_date = datetime(2024, 8, 20)  # Tanggal mulai (20 Agustus 2024)
end_date = datetime(2024, 8, 24)    # Tanggal akhir (24 Agustus 2024)

# Mengenerate daftar tanggal dalam rentang
date_list = [(start_date + timedelta(days=x)).strftime("%d/%m/%Y") for x in range((end_date - start_date).days + 1)]

# Variabel untuk menyimpan data masing-masing kota
palangkaraya_data = []
sampit_data = []

# Iterasi melalui setiap tanggal dalam rentang
for target_date in date_list:
    # Membuat format tanggal untuk parameter URL (misal "Aug 20, 2024")
    date_param = datetime.strptime(target_date, "%d/%m/%Y").strftime("%b %%20%d, %%20%Y")

    # Membuat URL dengan tanggal
    url = f"https://www.bi.go.id/hargapangan/Website/Home/GetDetailGridData?ProvId={prov_id}&RegId={reg_id}&PriceTypeId={price_type_id}&CatId={cat_id}&date={date_param}&isPasokan={is_pasokan}&_=1724939729406"

    # Mengambil data dari endpoint
    response = requests.get(url)

    # Periksa apakah respons sukses
    if response.status_code == 200:
        try:
            data = response.json()

            # Proses data untuk 'Kota Palangkaraya' dan 'Kota Sampit'
            for entry in data["data"]:
                if entry["name"] == "Kota Palangkaraya":
                    harga = entry.get(target_date, 0)  # Jika tidak tersedia, default ke 0
                    palangkaraya_data.append({
                        "name": entry["name"],
                        "date": target_date,
                        "harga": int(harga)  # Konversi harga menjadi integer
                    })
                elif entry["name"] == "Kota Sampit":
                    harga = entry.get(target_date, 0)  # Jika tidak tersedia, default ke 0
                    sampit_data.append({
                        "name": entry["name"],
                        "date": target_date,
                        "harga": int(harga)  # Konversi harga menjadi integer
                    })

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Response text:", response.text)  # Output respons untuk membantu debugging
    else:
        print(f"Error: Received response with status code {response.status_code}")

# Menampilkan hasil untuk Kota Palangkaraya terlebih dahulu
print("Data Kota Palangkaraya:")
for item in palangkaraya_data:
    print(f"{item['name']} pada tanggal {item['date']}: Harga {item['harga']}")

# Menampilkan hasil untuk Kota Sampit setelahnya
print("\nData Kota Sampit:")
for item in sampit_data:
    print(f"{item['name']} pada tanggal {item['date']}: Harga {item['harga']}")
