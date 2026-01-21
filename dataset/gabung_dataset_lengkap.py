import pandas as pd
import glob
import os

# 1. Cari semua file .csv di folder saat ini
# Anda bisa menyesuaikan polanya jika nama file Anda berbeda
files_to_merge = glob.glob("dataset-*.csv")

if not files_to_merge:
    print("Tidak ada file CSV dengan pola 'dataset-*.csv' yang ditemukan.")
    print("Pastikan script ini berada di folder yang sama dengan file-file CSV Anda.")
else:
    print("File CSV yang akan digabungkan:")
    print(files_to_merge)

    # 2. Siapkan list kosong untuk menampung data
    list_of_dfs = []

    # 3. Ulangi untuk setiap file yang ditemukan
    for filename in files_to_merge:
        # Baca file CSV
        df = pd.read_csv(filename)
        
        # Ambil nama kategori dari nama file
        # Contoh: "dataset-ayam.csv" -> "ayam"
        category = os.path.basename(filename).replace('dataset-', '').replace('.csv', '')
        
        # Tambahkan kolom 'kategori_utama'
        df['kategori_utama'] = category
        
        # Masukkan data ke dalam list
        list_of_dfs.append(df)

    # 4. Gabungkan semua data menjadi satu DataFrame
    combined_df = pd.concat(list_of_dfs, ignore_index=True)

    # 5. Simpan hasilnya ke file Excel (.xlsx)
    output_filename = 'dataset_lengkap.xlsx'
    
    # Gunakan .to_excel() untuk menyimpan ke format Excel
    # index=False agar nomor index tidak ikut ditulis di file Excel
    combined_df.to_excel(output_filename, index=False)
    
    print(f"\nBerhasil! Semua file CSV telah digabungkan menjadi satu file Excel:")
    print(f"--> {output_filename} <--")
    print(f"Jumlah total resep dalam file: {len(combined_df)}")