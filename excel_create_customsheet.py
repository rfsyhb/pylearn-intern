import pandas as pd
import os

# Variables
year_create = 2024
excel_list = {
    "Palangka Raya" : [
        "Hypermart",
        "Supermarket",
        "Minimarket",
        "Besar (Payang)",
        "Kahayan"
    ],
    "Kotawaringin Timur" : [
        "Supermarket",
        "Minimarket",
        "Kramat",
        "Berdikari",
    ],
    "Kapuas" : [
        "Supermarket",
        "Minimarket",
        "Sari Mulya"
    ],
    "Kotawaringin Barat": [
        "Supermarket",
        "Minimarket",
        "Indrasari",
    ],
    "Barito Utara": [
        "Supermarket",
        "Minimarket",
        "Pendopo",
    ],
    "Barito Selatan": [
        "Plaza Beringin"
    ]
}

month_list = [
    # "Januari",
    # "Februari",
    # "Maret",
    # "April",
    # "Mei",
    # "Juni",
    # "Juli",
    # "Agustus",
    "September",
    # "Oktober",
    # "November",
    # "Desember"
]

# Create output directory if not exists
output_dir = "docs/output"
os.makedirs(output_dir, exist_ok=True)

# Create Excel files for each city
for city, markets in excel_list.items():
    file_name = f"SIGAP_{city}_{year_create}.xlsx"
    file_path = os.path.join(output_dir, file_name)
    
    # Create a new Excel file with multiple sheets
    with pd.ExcelWriter(file_path) as writer:
        for month in month_list:
            for market in markets:
                sheet_name = f"{market} {month}"
                # Create an empty DataFrame for each market per month
                df = pd.DataFrame()
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Excel file '{file_name}' created with empty sheets for each market and month in '{output_dir}' directory.")

