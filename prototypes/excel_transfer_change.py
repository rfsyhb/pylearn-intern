import pandas as pd
import os

# Base path (ganti sesuai dengan lokasi folder utama Anda)
base_path = 'docs'

# List file input dan output
xlsx_input_list = [
    "SIGAP_Barito Selatan_2024.xlsx",
    "SIGAP_Muara Teweh_2024.xlsx",
    "SIGAP_Kapuas_2024.xlsx",
    "SIGAP_Pangkalan Bun_2024.xlsx",
    "SIGAP_Palangka Raya_2024.xlsx",
    "SIGAP_Sampit_2024.xlsx",
]

xlsx_output_list = [
    "SIGAP_Barito Selatan_2024.xlsx",
    "SIGAP_Barito Utara_2024.xlsx",
    "SIGAP_Kapuas_2024.xlsx",
    "SIGAP_Kotawaringin Barat_2024.xlsx",
    "SIGAP_Palangka Raya_2024.xlsx",
    "SIGAP_Kotawaringin TImur_2024.xlsx",
]

# Buat folder output jika belum ada
output_dir = os.path.join(base_path, 'output')
os.makedirs(output_dir, exist_ok=True)

# Fungsi untuk mengubah nama sheet
def rename_sheet(sheet_name):
    # Mengubah nama sheet berdasarkan kondisi tertentu
    if sheet_name.startswith("Pasar Mini"):
        return sheet_name.replace("Pasar Mini", "Minimarket", 1)
    elif sheet_name.startswith("Pasar Super"):
        return sheet_name.replace("Pasar Super", "Supermarket", 1)
    elif sheet_name.startswith("Pasar Hyper"):
        return sheet_name.replace("Pasar Hyper", "Hypermart", 1)
    elif sheet_name.startswith("Pasar "):
        return sheet_name.replace("Pasar ", "", 1)
    return sheet_name

# Iterasi melalui setiap pasangan file input dan output
for input_file, output_file in zip(xlsx_input_list, xlsx_output_list):
    # Baca semua sheets dari file .xlsx input
    input_path = os.path.join(base_path, 'input', input_file)  # Sesuaikan dengan path input file Anda
    excel_file = pd.ExcelFile(input_path)

    # Buat writer untuk file .xlsx output baru
    output_path = os.path.join(output_dir, output_file)  # Sesuaikan dengan path output file Anda
    writer = pd.ExcelWriter(output_path, engine='openpyxl')

    # Iterasi melalui setiap sheet, ubah nama sheet, dan simpan ke file output
    for sheet_name in excel_file.sheet_names:
        df = excel_file.parse(sheet_name)  # Baca sheet sebagai DataFrame
        new_sheet_name = rename_sheet(sheet_name)  # Ubah nama sheet
        df.to_excel(writer, sheet_name=new_sheet_name, index=False)  # Tulis ke file output dengan nama sheet baru

    # Simpan dan tutup file .xlsx output
    writer.close()

    print(f"File {input_file} berhasil dikonversi ke {output_file} dengan nama sheet yang telah diubah!")
