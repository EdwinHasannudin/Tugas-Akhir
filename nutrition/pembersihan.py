import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def format_excel_sheet(worksheet, header_color="FF6B35"):
    """
    Format Excel sheet dengan styling profesional
    """
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    # Define styles
    header_fill = PatternFill(start_color=header_color, end_color=header_color, fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)
    
    center_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    left_alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    # Format header
    for cell in worksheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = center_alignment
        cell.border = border
    
    # Format data
    for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row):
        for cell in row:
            cell.border = border
            # Try to format numeric values
            try:
                if cell.value is not None:
                    float_val = float(cell.value)
                    cell.alignment = center_alignment
                    cell.number_format = '0.0000'
            except (ValueError, TypeError):
                cell.alignment = left_alignment
    
    # Auto-adjust column width
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width



# ============================================================
# MAIN PROCESS
# ============================================================
print("=" * 80)
print("[STEP 3] PEMBERSIHAN DATA - STEP 3 (Pipeline)")
print("=" * 80)

# Baca file Excel dari STEP 2
input_file = 'dataset/nutrition_pipeline.xlsx'
print(f"\n[INFO] Membaca file: {input_file}")

import os
if not os.path.exists(input_file):
    print(f"❌ File '{input_file}' tidak ditemukan!")
    print("   Pastikan Anda telah menjalankan step sebelumnya")
    exit(1)

try:
    # Baca sheet terakhir (One-Hot Encoded)
    df = pd.read_excel(input_file, sheet_name='One-Hot Encoded')
except:
    # Fallback ke sheet lain jika One-Hot Encoded belum ada
    print("⚠️  Sheet 'One-Hot Encoded' tidak ditemukan. Mencari sheet alternatif...")
    try:
        df = pd.read_excel(input_file, sheet_name='Nutrition Scaled')
    except:
        df = pd.read_excel(input_file, sheet_name=0)

df_original = df.copy()
print(f"✓ Total data awal: {len(df)} bahan makanan\n")

# Step 1: Hapus baris yang memiliki nilai "lainnya" pada kolom "kategori"
print("[STEP] 1: Menghapus kategori 'lainnya'...")
if 'kategori' in df.columns:
    df_cleaned = df[df['kategori'] != 'lainnya']
    removed_lainnya = len(df) - len(df_cleaned)
    print(f"   - Baris yang dihapus: {removed_lainnya}")
    print(f"   - Total setelah: {len(df_cleaned)}\n")
else:
    df_cleaned = df.copy()
    removed_lainnya = 0
    print("   WARNING Kolom ori tidak ditemukan, skip step ini\n")

# Step 2: Daftar kata kunci yang ingin dihapus dari kolom nama
print("[STEP] 2: Menghapus bahan makanan berdasarkan kata kunci...")
kata_kunci_dihapus = [
    'andaliman', 'pohon', 'babi', 'anjing', 'kuda', 'domba', 'burung', 'angsa', 
    'belut', 'katak', 'keong', 'kodok', 'kura-kura', 'ulat sagu', 'ham', 'hiu', 
    'kotiu', 'kelinci', 'buaya', 'dodol', 'penyu', 'masakan', 'goreng', 'kukus', 
    'ginjal', 'sosis', 'lilin', 'pempek', 'kue', 'martabak', 'otak', 'ular', 
    'purundawa', 'putri malu', 'purut', 'sate', 'sarimuka', 'tekwan', 'tinira', 
    'camilan', 'ketoprak', 'rusa', 'soto'
]

before_keyword = len(df_cleaned)
for kata in kata_kunci_dihapus:
    df_cleaned = df_cleaned[~df_cleaned['name'].str.contains(kata, case=False, na=False)]

# Tampilkan jumlah baris setelah dihapus
print(f"Jumlah baris setelah dihapus: {len(df_cleaned)}")

# Step 3: Simpan hasil
print(f"[WRITE] Menambahkan sheet baru ke {input_file}...")

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Gunakan ExcelWriter untuk append sheet
with pd.ExcelWriter(input_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    # Tulis sheet Data Cleaned
    df_cleaned.to_excel(writer, sheet_name='Data Cleaned', index=False)
    
    # Format sheet Data Cleaned
    worksheet = writer.sheets['Data Cleaned']
    format_excel_sheet(worksheet, header_color="FF6B35")

print("[OK] Sheet 'Data Cleaned' berhasil ditambahkan!\n")

# Summary
print("=" * 80)
print("[RESULT] RINGKASAN PEMBERSIHAN DATA")
print("=" * 80)
print(f"\nData Awal       : {len(df_original)} bahan makanan")
print(f"Hapus 'lainnya' : -{removed_lainnya} baris")
print(f"Hapus keyword   : -{removed_keywords} baris")
print(f"Data Akhir       : {len(df_cleaned)} bahan makanan")
print(f"Total dihapus   : {len(df_original) - len(df_cleaned)} baris ({((len(df_original) - len(df_cleaned))/len(df_original)*100):.1f}%)")

if 'kategori' in df_cleaned.columns:
    print(f"\n[KATEGORI] Kategori yang tersisa:")
    kategori_counts = df_cleaned['kategori'].value_counts()
    for cat, count in kategori_counts.items():
        print(f"   - {cat}: {count} items")

print("\n[DONE] STEP 3 SELESAI: Pembersihan data berhasil disimpan!")
print(f"📁 File: {input_file}")
print("\n" + "=" * 80)
print("NEXT STEP: Jalankan pembagian.py")
print("=" * 80)