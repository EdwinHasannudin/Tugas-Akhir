import pandas as pd

# Baca file Excel
df = pd.read_excel('nutrition_data_with_categories_texture.xlsx')

# Tampilkan jumlah baris sebelum dihapus
print(f"Jumlah baris sebelum dihapus: {len(df)}")

# Hapus baris yang memiliki nilai "lainnya" pada kolom "kategori"
df_cleaned = df[df['kategori'] != 'lainnya']

# Daftar kata kunci yang ingin dihapus dari kolom nama
kata_kunci_dihapus = ['andaliman', 'pohon', 'babi', 'anjing', 'kuda', 'domba', 'burung', 'angsa', 'belut', 
                      'katak', 'keong', 'kodok', 'kura-kura', 'anjing', 'ulat sagu', 'ham', 'hiu', 'kotiu',
                      'kelinci', 'buaya', 'dodol', 'penyu', 'masakan', 'goreng', 'kukus', 'ginjal', 'sosis',
                      'lilin', 'pempek', 'kue', 'martabak', 'otak', 'ular', 'purundawa', 'putri malu', 'purut',
                      'sate', 'sarimuka', 'tekwan', 'tinira', 'camilan', 'ketoprak', 'rusa', 'soto']  

# Hapus baris yang mengandung kata kunci pada kolom "nama"
for kata in kata_kunci_dihapus:
    df_cleaned = df_cleaned[~df_cleaned['name'].str.contains(kata, case=False, na=False)]

# Tampilkan jumlah baris setelah dihapus
print(f"Jumlah baris setelah dihapus: {len(df_cleaned)}")

# Simpan hasil ke file baru
df_cleaned.to_excel('nutrition_data_cleaned.xlsx', index=False)

print("Pembersihan selesai. Data telah disimpan ke 'nutrition_data_cleaned.xlsx'")