import pandas as pd

excel_file = 'nutrition/dataset/nutrition_pipeline.xlsx'
xls = pd.ExcelFile(excel_file)
print("Sheet names:", xls.sheet_names)

print("\n--- Dataset Asli ---")
df_raw = pd.read_excel(excel_file, sheet_name='Dataset Asli')
print("Columns:", list(df_raw.columns))
print("Shape:", df_raw.shape)
print("\nFirst 3 rows:")
print(df_raw.head(3))

print("\n--- Nutrition Scaled ---")
df_scaled = pd.read_excel(excel_file, sheet_name='Nutrition Scaled')
print("Columns:", list(df_scaled.columns))
print("Shape:", df_scaled.shape)
print("\nFirst 3 rows:")
print(df_scaled.head(3))
