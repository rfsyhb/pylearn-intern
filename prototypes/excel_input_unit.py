import pandas as pd
import os

# Base path untuk folder input dan output
base_path = 'docs'
input_dir = os.path.join(base_path, 'output_final')
output_dir = os.path.join(base_path, 'output_unit_updated')
os.makedirs(output_dir, exist_ok=True)

# Daftar komoditas cair
komoditas_cair = [
    "MINYAK GORENG", 
]

# Fungsi untuk memperbarui kolom "unit" berdasarkan nilai di kolom "Komoditas"
def update_unit_column(df):
    if 'Komoditas' in df.columns and 'Unit' in df.columns:
        # Perbarui kolom "unit" berdasarkan kondisi di atas
        df['Unit'] = df['Komoditas'].apply(lambda x: 'L' if x in komoditas_cair else 'Kg')
    return df

# Iterasi melalui setiap file Excel di folder input
for input_file in os.listdir(input_dir):
    if input_file.endswith('.xlsx'):
        input_path = os.path.join(input_dir, input_file)
        excel_file = pd.ExcelFile(input_path)

        # Buat writer untuk file output baru
        output_path = os.path.join(output_dir, input_file)  # Menggunakan nama file yang sama untuk output
        writer = pd.ExcelWriter(output_path, engine='openpyxl')

        # Iterasi melalui setiap sheet di file input
        for sheet_name in excel_file.sheet_names:
            df = excel_file.parse(sheet_name)  # Baca sheet sebagai DataFrame
            
            # Perbarui kolom "unit"
            df = update_unit_column(df)
            
            # Tulis ke file output dengan sheet yang sama
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Simpan dan tutup file output
        writer.close()
        
        print(f"File {input_file} berhasil diperbarui dan disimpan ke {output_path} dengan kolom 'unit' yang diperbarui!")

print("Proses pembaruan kolom 'unit' selesai untuk semua file.")
