"""
Script untuk extract nutrition_pipeline.xlsx ke JSON files
"""
import pandas as pd
import json
from pathlib import Path

# Read Excel file
excel_file = Path('nutrition/dataset/nutrition_pipeline.xlsx')
print(f"Reading {excel_file}...")

# Read Dataset Asli
df_raw = pd.read_excel(excel_file, sheet_name='Dataset Asli')
print(f"Dataset Asli shape: {df_raw.shape}")
print(f"Columns: {list(df_raw.columns)}")

# Read Nutrition Scaled
df_scaled = pd.read_excel(excel_file, sheet_name='Nutrition Scaled')
print(f"Nutrition Scaled shape: {df_scaled.shape}")
print(f"Columns: {list(df_scaled.columns)}")

# Convert to JSON and save
raw_json = df_raw.to_dict('records')
scaled_json = df_scaled.to_dict('records')

# Save to src/data/
output_dir = Path('src/data')
output_dir.mkdir(exist_ok=True)

with open(output_dir / 'nutrition_raw.json', 'w', encoding='utf-8') as f:
    json.dump(raw_json, f, indent=2, ensure_ascii=False)
print(f"✓ Saved nutrition_raw.json ({len(raw_json)} records)")

with open(output_dir / 'nutrition_scaled.json', 'w', encoding='utf-8') as f:
    json.dump(scaled_json, f, indent=2, ensure_ascii=False)
print(f"✓ Saved nutrition_scaled.json ({len(scaled_json)} records)")

print("\nDone! Now update DemoSystemPage.tsx to use these JSON files.")
