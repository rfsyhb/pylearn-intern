import requests

url = "https://api-sp2kp.kemendag.go.id/report/api/average-price/generate-perbandingan-harga"

# Data yang dikirim dalam form
payload = {
    'tanggal': '2024-09-11',
    'tanggal_pembanding': '2024-09-10',
    'kode_provinsi': '62',
    'kode_kab_kota': '6271'
}

# Header untuk memastikan request dikirim sebagai form data
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Melakukan POST request
response = requests.post(url, data=payload, headers=headers)

# Memeriksa respon
if response.status_code == 200:
    print("Response Data:", response.json())  # Jika respon dalam format JSON
else:
    print(f"Error {response.status_code}: {response.text}")
