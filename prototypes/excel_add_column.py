import pandas as pd
import os

# Base path (ganti sesuai dengan lokasi folder utama Anda)
base_path = 'docs'

# Daftar file Excel dan nilai lokasi yang sesuai
excel_lists = {
    "SIGAP_Barito Selatan_2024.xlsx": "Barito Selatan",
    "SIGAP_Barito Utara_2024.xlsx": "Barito Utara",
    "SIGAP_Kapuas_2024.xlsx": "Kapuas",
    "SIGAP_Kotawaringin Barat_2024.xlsx": "Kotawaringin Barat",
    "SIGAP_Palangka Raya_2024.xlsx": "Palangka Raya",
    "SIGAP_Kotawaringin Timur_2024.xlsx": "Kotawaringin Timur",
}

# Buat folder output jika belum ada
output_dir = os.path.join(base_path, 'output_newcolumn')
os.makedirs(output_dir, exist_ok=True)

# Iterasi melalui setiap file Excel dan nilai lokasi
for input_file, lokasi_value in excel_lists.items():
    # Baca semua sheets dari file .xlsx input
    input_path = os.path.join(base_path, 'output', input_file)  # Sesuaikan dengan path input file Anda
    excel_file = pd.ExcelFile(input_path)

    # Buat writer untuk file .xlsx output baru
    output_file = input_file.replace(".xlsx", ".xlsx")  # Membuat nama file output baru
    output_path = os.path.join(output_dir, output_file)  # Sesuaikan dengan path output file Anda
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # Iterasi melalui setiap sheet, tambahkan kolom "Lokasi", dan simpan ke file output
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)  # Baca sheet sebagai DataFrame
        
        # Tambahkan kolom "Lokasi" di sisi kiri dengan nilai sesuai dengan lokasi_value
        df.insert(0, 'Lokasi', lokasi_value)
        
        # Tulis ke file output dengan nama sheet yang sama
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Simpan dan tutup file .xlsx output
    writer.close()

    print(f"File {input_file} berhasil dikonversi ke {output_file} dengan kolom 'Lokasi' ditambahkan!")
