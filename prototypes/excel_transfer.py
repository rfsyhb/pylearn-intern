import pandas as pd
import os

# Base path (ganti sesuai dengan lokasi folder utama Anda)
base_path = 'docs'

# List file input dan output
xls_list = [
  "SIGAP_Kapuas_2023.xls",
  "SIGAP_Palangka Raya_2023.xls",
]

xlsx_list = [
  "SIGAP_Kapuas_2023.xlsx",
  "SIGAP_Palangka Raya_2023.xlsx",
]

# Buat folder output jika belum ada
output_dir = os.path.join(base_path, 'output')
os.makedirs(output_dir, exist_ok=True)

# Iterasi melalui setiap pasangan file .xls dan .xlsx
for xls_file, xlsx_file in zip(xls_list, xlsx_list):
    # Baca semua sheets dari file .xls
    xls_path = os.path.join(base_path, 'input', xls_file)  # Sesuaikan dengan path input file Anda
    xls = pd.ExcelFile(xls_path)

    # Buat writer untuk file .xlsx baru
    xlsx_path = os.path.join(output_dir, xlsx_file)  # Sesuaikan dengan path output file Anda
    writer = pd.ExcelWriter(xlsx_path, engine='openpyxl')

    # Iterasi melalui setiap sheet dan simpan ke file .xlsx
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)  # Baca sheet sebagai DataFrame
        df.to_excel(writer, sheet_name=sheet_name, index=False)  # Tulis ke file .xlsx

    # Simpan dan tutup file .xlsx
    writer.close()

    print(f"File {xls_file} berhasil dikonversi ke {xlsx_file}!")
