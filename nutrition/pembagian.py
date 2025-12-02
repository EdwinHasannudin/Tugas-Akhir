import pandas as pd
import re

# Baca file Excel
file_path = "nutrition_data_cleaned.xlsx"
df = pd.read_excel(file_path)

# Fungsi untuk membersihkan nama sheet
def clean_sheet_name(name):
    # Ganti karakter yang tidak diizinkan dengan underscore
    cleaned = re.sub(r'[\\/*?\[\]:]', '_', str(name))
    # Potong maksimal 31 karakter
    return cleaned[:31]

# Buat file Excel baru dengan sheet per kategori
output_file = "nutrition_data_per_kategori.xlsx"

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Dapatkan daftar kategori unik
    kategori_list = df['kategori'].unique()
    
    # Loop melalui setiap kategori
    for kategori in kategori_list:
        # Filter data untuk kategori tertentu
        df_kategori = df[df['kategori'] == kategori]
        
        # Bersihkan nama sheet dari karakter tidak valid
        sheet_name = clean_sheet_name(kategori)
        
        # Tulis ke sheet baru
        df_kategori.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✅ Sheet '{sheet_name}' dibuat dengan {len(df_kategori)} baris data")

print(f"\n🎉 File berhasil disimpan sebagai: {output_file}")
print(f"📊 Total kategori: {len(kategori_list)}")