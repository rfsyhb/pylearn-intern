import pandas as pd
import os

# Base path untuk folder input dan output
base_path = 'docs'
input_dir = os.path.join(base_path, 'output_newcolumn')
output_dir = os.path.join(base_path, 'output_final')
os.makedirs(output_dir, exist_ok=True)

# Fungsi untuk memperbarui nama header dan menambahkan kolom "unit"
def update_headers_and_add_unit(df):
    # Periksa dan ganti nama kolom jika ada
    if 'Komoditi' in df.columns:
        df.rename(columns={'Komoditi': 'Komoditas'}, inplace=True)
    if 'Jenis Komoditi' in df.columns:
        df.rename(columns={'Jenis Komoditi': 'Jenis'}, inplace=True)
    
    # Tambahkan kolom "unit" di posisi kedua (index 1)
    df.insert(1, 'Unit', None)  # Menambahkan kolom "unit" dengan nilai kosong
    
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
            
            # Perbarui header dan tambahkan kolom "unit"
            df = update_headers_and_add_unit(df)
            
            # Tulis ke file output dengan sheet yang sama
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Simpan dan tutup file output
        writer.close()
        
        print(f"File {input_file} berhasil diperbarui dan disimpan ke {output_path}!")

print("Proses pembaruan header dan penambahan kolom selesai untuk semua file.")
