import pandas as pd

excel_path = './docs/learn.xlsx'

def print_all_sheet_raw():
    df = pd.read_excel(excel_path, sheet_name=None)
    print(df)

def print_all_sheet():
    df = pd.read_excel(excel_path, sheet_name=None)
    for sheet_name, sheet in df.items():
        print(f"Sheet: {sheet_name}")
        print(sheet)

def merge_sheets():
    df_all_sheets = pd.read_excel(excel_path, sheet_name=None)

    df_sheet1 = df_all_sheets['Sheet Satu']
    df_sheet2 = df_all_sheets['Sheet Dua']

    df_merged = pd.concat([df_sheet1, df_sheet2], ignore_index=True)

    df_merged.to_excel('./docs/learn_merged.xlsx', index=False, sheet_name='Merged Sheet')

if __name__ == '__main__':
    merge_sheets()