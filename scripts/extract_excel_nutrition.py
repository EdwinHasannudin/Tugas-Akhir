"""
Extract nutrition_pipeline.xlsx sheets ke JSON files
Kombinasi dengan kategori/texture dari existing data
"""
import pandas as pd
import json
from pathlib import Path

excel_file = Path('nutrition/dataset/nutrition_pipeline.xlsx')

# Read both sheets
df_raw = pd.read_excel(excel_file, sheet_name='Dataset Asli')
df_scaled = pd.read_excel(excel_file, sheet_name='Nutrition Scaled')

# Read kategori dari sheet lauk dan sayuran untuk mapping nama -> kategori
try:
    df_lauk = pd.read_excel(excel_file, sheet_name='lauk', usecols=['name'])
    df_sayuran = pd.read_excel(excel_file, sheet_name='sayuran', usecols=['name'])
    
    lauk_names = set(df_lauk['name'].str.lower().tolist())
    sayuran_names = set(df_sayuran['name'].str.lower().tolist())
    
    def get_category(name):
        name_lower = str(name).lower()
        if name_lower in lauk_names:
            return 'lauk'
        elif name_lower in sayuran_names:
            return 'sayuran'
        return 'other'
    
    df_raw['category'] = df_raw['name'].apply(get_category)
    df_scaled['category'] = df_scaled['name'].apply(get_category)
    
except Exception as e:
    print(f"Warning: Could not read category sheets: {e}")
    df_raw['category'] = 'other'
    df_scaled['category'] = 'other'

# Rename columns untuk sesuai dengan app standard
df_raw = df_raw.rename(columns={
    'calories': 'energy',
    'proteins': 'protein',
    'carbohydrate': 'carbs'
})

df_scaled = df_scaled.rename(columns={
    'calories': 'energy',
    'proteins': 'protein',
    'carbohydrate': 'carbs'
})

# Convert to dict
raw_data = df_raw.to_dict('records')
scaled_data = df_scaled.to_dict('records')

# Save to src/data/
output_dir = Path('src/data')
output_dir.mkdir(exist_ok=True)

with open(output_dir / 'nutrition_raw_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(raw_data, f, indent=2, ensure_ascii=False)
print(f"✓ Saved nutrition_raw_dataset.json ({len(raw_data)} records)")

with open(output_dir / 'nutrition_scaled_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(scaled_data, f, indent=2, ensure_ascii=False)
print(f"✓ Saved nutrition_scaled_dataset.json ({len(scaled_data)} records)")

print("\nSample record (raw):")
print(json.dumps(raw_data[0], indent=2, ensure_ascii=False))
print("\nSample record (scaled):")
print(json.dumps(scaled_data[0], indent=2, ensure_ascii=False))
