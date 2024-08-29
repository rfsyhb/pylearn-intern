import pandas as pd

# Path to save the Excel file
output_path = './docs/excel_template.xlsx'
# Dates, month value is the number of days in that month
# THIS IS EXAMPLE! get the real date from https://www.timeanddate.com/calendar/
dates = {
    "year": 2023,
    "month": {
        "Januari": 31,
        "Februari": 28,
        "Maret": 31,
        "April": 30,
        "Mei": 31,
        "Juni": 30,
        "Juli": 31,
        "Agustus": 31,
        "September": 30,
        "Oktober": 31,
        "November": 30,
        "Desember": 31
    },
}

# Define variables
cities = ["Kota Palangkaraya", "Kota Sampit"]
markets = ["Pasar Tradisional", "Pasar Modern", "Pedagang Besar", "Produsen"]
commodities = {
    "Beras": [
        "Bawah I",
        "Bawah II",
        "Medium I",
        "Medium II",
        "Super I",
        "Super II"
    ],
    "Daging Ayam Ras": "Segar",
    "Daging Sapi": [
        "Kualitas 1",
        "Kualitas 2"
    ],
    "Telur Ayam Ras": "Segar",
    "Bawang Merah": "Ukuran Sedang",
    "Bawang Putih": "Ukuran Sedang",
    "Cabai Merah": [
        "Besar",
        "Keriting"
    ],
    "Cabai Rawit": [
        "Hijau",
        "Merah"
    ],
    "Minyak Goreng": [
        "Curah",
        "Kemasan Bermerk 1",
        "Kemasan Bermerk 2"
    ],
    "Gula Pasir": [
        "Kualitas Premium",
        "Lokal"
    ]
}

# Initialize Excel writer
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:

    # Loop through each month
    for month, days in dates["month"].items():
        # Create data for the Excel sheet
        data = []
        for day in range(1, days + 1):
            for city in cities:
                for market in markets:
                    for commodity, types in commodities.items():
                        if isinstance(types, list):
                            for type_name in types:
                                data.append([
                                    f"{dates['year']}-{list(dates['month'].keys()).index(month)+1:02d}-{day:02d}",  # TANGGAL
                                    "",  # PERIODE
                                    "BI",  # SUMBER
                                    "Konsumen",  # RESPONDEN
                                    "KALIMANTAN TENGAH",  # PROVINSI
                                    city,  # KOTA KAB
                                    market,  # PASAR
                                    commodity,  # KOMODITAS
                                    "Kg" if commodity != "Minyak Goreng" else "Lt",  # UNIT
                                    type_name,  # JENIS_MERK
                                    "",  # KEMASAN
                                    "",  # HARGA_SAT
                                    "",  # SAT
                                    markets.index(market)  # SORT_KEY for custom market order
                                ])
                        else:
                            data.append([
                                f"{dates['year']}-{list(dates['month'].keys()).index(month)+1:02d}-{day:02d}",  # TANGGAL
                                "",  # PERIODE
                                "BI",  # SUMBER
                                "Konsumen",  # RESPONDEN
                                "KALIMANTAN TENGAH",  # PROVINSI
                                city,  # KOTA KAB
                                market,  # PASAR
                                commodity,  # KOMODITAS
                                "Kg" if commodity != "Minyak Goreng" else "Lt",  # UNIT
                                types,  # JENIS_MERK
                                "",  # KEMASAN
                                "",  # HARGA_SAT
                                "",  # SAT
                                markets.index(market)  # SORT_KEY for custom market order
                            ])

        # Convert data to DataFrame
        df = pd.DataFrame(data, columns=[
            "TANGGAL", "PERIODE", "SUMBER", "RESPONDEN", "PROVINSI", 
            "KOTA_KAB", "PASAR", "KOMODITAS", "UNIT", "JENIS_MERK", 
            "KEMASAN", "HARGA_SAT", "SAT", "SORT_KEY"
        ])
        
        # Sort DataFrame by TANGGAL, KOTA_KAB, and custom SORT_KEY for PASAR
        df = df.sort_values(by=["TANGGAL", "KOTA_KAB", "SORT_KEY"], ascending=[True, True, True])

        # Drop the SORT_KEY column before saving to Excel
        df = df.drop(columns=["SORT_KEY"])

        # Save DataFrame to a new sheet in Excel file
        df.to_excel(writer, sheet_name=month, index=False)

print(f"Excel template created successfully as '{output_path}'.")
