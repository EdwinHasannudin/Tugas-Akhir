import pandas as pd
import json

def load_recipes_from_excel(file_path):
    """
    Memuat resep dari file Excel dan mengorganisir berdasarkan kategori
    """
    try:
        # Baca file Excel
        df = pd.read_excel(file_path)
        
        # Inisialisasi dictionary untuk menyimpan resep
        recipes_database = {}
        
        # Iterasi melalui setiap baris dalam DataFrame
        for index, row in df.iterrows():
            kategori = row['kategori_utama']
            title = row['Title']
            ingredients = row['Ingredients']
            steps = row['Steps']
            
            # Jika kategori belum ada, buat list baru
            if kategori not in recipes_database:
                recipes_database[kategori] = []
            
            # Tambahkan resep ke kategori yang sesuai (tanpa loves dan url)
            recipe = {
                'nama': title,
                'bahan': parse_ingredients(ingredients),
                'langkah': steps,
                'kesulitan': estimate_difficulty(steps, ingredients)
            }
            
            recipes_database[kategori].append(recipe)
        
        return recipes_database
    
    except Exception as e:
        print(f"Error loading recipes from Excel: {e}")
        return {}

def parse_ingredients(ingredients_text):
    """
    Mem-parse teks bahan menjadi list yang terstruktur
    """
    if pd.isna(ingredients_text):
        return []
    
    # Split berdasarkan '--' yang merupakan pemisah dalam data
    ingredients_list = [ing.strip() for ing in str(ingredients_text).split('--') if ing.strip()]
    
    # Bersihkan bahan dari karakter tidak perlu
    cleaned_ingredients = []
    for ingredient in ingredients_list:
        # Hapus angka dan karakter khusus di awal
        cleaned = ingredient.strip()
        if cleaned and not cleaned.isspace():
            cleaned_ingredients.append(cleaned)
    
    return cleaned_ingredients

def estimate_difficulty(steps, ingredients):
    """
    Mengestimasi tingkat kesulitan berdasarkan langkah dan bahan
    """
    if pd.isna(steps):
        return "Tidak Diketahui"
    
    steps_text = str(steps)
    ingredients_count = len(parse_ingredients(ingredients))
    
    # Hitung jumlah langkah dengan split berdasarkan '--'
    steps_count = len([step for step in steps_text.split('--') if step.strip()])
    
    if steps_count <= 3 and ingredients_count <= 5:
        return "Mudah"
    elif steps_count <= 6 and ingredients_count <= 8:
        return "Sedang"
    else:
        return "Sulit"

def save_recipes_to_excel(recipes_database, output_file='resep_database.xlsx'):
    """
    Menyimpan database resep ke file Excel dengan multiple sheets
    """
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            
            # Sheet 1: Semua Resep (tanpa loves dan url)
            all_recipes_data = []
            for category, recipes in recipes_database.items():
                for recipe in recipes:
                    all_recipes_data.append({
                        'Kategori': category,
                        'Nama Resep': recipe['nama'],
                        'Bahan': ' | '.join(recipe['bahan']),
                        'Jumlah Bahan': len(recipe['bahan']),
                        'Langkah Masak': recipe['langkah'],
                        'Tingkat Kesulitan': recipe['kesulitan']
                    })
            
            df_all = pd.DataFrame(all_recipes_data)
            df_all.to_excel(writer, sheet_name='Semua_Resep', index=False)
            
            # Sheet 2: Statistik per Kategori (tanpa loves)
            stats_data = []
            for category, recipes in recipes_database.items():
                # Hitung distribusi kesulitan
                difficulties = {'Mudah': 0, 'Sedang': 0, 'Sulit': 0}
                for recipe in recipes:
                    if recipe['kesulitan'] in difficulties:
                        difficulties[recipe['kesulitan']] += 1
                
                stats_data.append({
                    'Kategori': category,
                    'Jumlah Resep': len(recipes),
                    'Resep Mudah': difficulties['Mudah'],
                    'Resep Sedang': difficulties['Sedang'],
                    'Resep Sulit': difficulties['Sulit']
                })
            
            df_stats = pd.DataFrame(stats_data)
            df_stats.to_excel(writer, sheet_name='Statistik', index=False)
            
            # Sheet 3: Resep Populer (tanpa loves, diurutkan berdasarkan jumlah bahan)
            all_recipes = []
            for category, recipes in recipes_database.items():
                for recipe in recipes:
                    recipe['kategori'] = category
                    all_recipes.append(recipe)
            
            # Urutkan berdasarkan jumlah bahan (resep dengan bahan paling sedikit dianggap sederhana/populer)
            popular_recipes = sorted(all_recipes, key=lambda x: len(x['bahan']))[:10]
            
            popular_data = []
            for recipe in popular_recipes:
                popular_data.append({
                    'Peringkat': popular_recipes.index(recipe) + 1,
                    'Nama Resep': recipe['nama'],
                    'Kategori': recipe['kategori'],
                    'Tingkat Kesulitan': recipe['kesulitan'],
                    'Jumlah Bahan': len(recipe['bahan']),
                    'Bahan Utama': ' | '.join(recipe['bahan'][:3])  # 3 bahan pertama
                })
            
            df_popular = pd.DataFrame(popular_data)
            df_popular.to_excel(writer, sheet_name='Resep_Sederhana', index=False)
            
            # Sheets per Kategori (tanpa loves dan url)
            for category, recipes in recipes_database.items():
                category_data = []
                for recipe in recipes:
                    category_data.append({
                        'Nama Resep': recipe['nama'],
                        'Bahan': '\n'.join(recipe['bahan']),
                        'Langkah Masak': recipe['langkah'],
                        'Tingkat Kesulitan': recipe['kesulitan'],
                        'Jumlah Bahan': len(recipe['bahan'])
                    })
                
                # Batasi nama sheet maks 31 karakter
                sheet_name = category[:31]
                df_category = pd.DataFrame(category_data)
                df_category.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✓ Database resep berhasil disimpan ke {output_file}")
        print(f"✓ Sheets yang dibuat: Semua_Resep, Statistik, Resep_Sederhana, dan sheets per kategori")
        return True
        
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return False

def get_recipes_by_category(recipes_database, category):
    """
    Mendapatkan semua resep dari kategori tertentu
    """
    return recipes_database.get(category, [])

def search_recipes_by_ingredient(recipes_database, ingredient):
    """
    Mencari resep berdasarkan bahan tertentu
    """
    matching_recipes = {}
    
    for category, recipes in recipes_database.items():
        category_matches = []
        for recipe in recipes:
            # Cek apakah bahan ada dalam daftar bahan resep
            if any(ingredient.lower() in bahan.lower() for bahan in recipe['bahan']):
                category_matches.append(recipe)
        
        if category_matches:
            matching_recipes[category] = category_matches
    
    return matching_recipes

def analyze_recipes_database(recipes_database):
    """
    Menganalisis database resep dan menampilkan statistik
    """
    print("=== ANALISIS DATABASE RESEP ===")
    
    total_recipes = 0
    category_stats = {}
    
    for category, recipes in recipes_database.items():
        category_stats[category] = len(recipes)
        total_recipes += len(recipes)
        
        # Hitung rata-rata tingkat kesulitan
        difficulties = {'Mudah': 0, 'Sedang': 0, 'Sulit': 0, 'Tidak Diketahui': 0}
        
        for recipe in recipes:
            difficulties[recipe['kesulitan']] += 1
        
        print(f"\n📊 Kategori: {category.upper()}")
        print(f"   📝 Jumlah resep: {len(recipes)}")
        print(f"   🎯 Tingkat kesulitan: {difficulties}")
    
    print(f"\n📈 TOTAL RESEP: {total_recipes}")
    print(f"🏷️  KATEGORI: {list(recipes_database.keys())}")

def get_simple_recipes(recipes_database, top_n=5):
    """
    Mendapatkan resep paling sederhana berdasarkan jumlah bahan
    """
    all_recipes = []
    
    for category, recipes in recipes_database.items():
        for recipe in recipes:
            recipe['kategori'] = category  # Tambahkan info kategori
            all_recipes.append(recipe)
    
    # Urutkan berdasarkan jumlah bahan (ascending - paling sedikit bahan)
    simple_recipes = sorted(all_recipes, key=lambda x: len(x['bahan']))
    
    return simple_recipes[:top_n]

def display_recipe_details(recipe):
    """
    Menampilkan detail resep dengan format yang rapi
    """
    print(f"\n{'='*60}")
    print(f"🍳 RESEP: {recipe['nama']}")
    print(f"{'='*60}")
    print(f"📁 Kategori: {recipe.get('kategori', 'Tidak diketahui')}")
    print(f"🎯 Kesulitan: {recipe['kesulitan']}")
    print(f"📊 Jumlah Bahan: {len(recipe['bahan'])}")
    
    print(f"\n🛒 BAHAN-BAHAN:")
    for i, bahan in enumerate(recipe['bahan'][:8], 1):  # Tampilkan 8 bahan pertama
        print(f"   {i}. {bahan}")
    if len(recipe['bahan']) > 8:
        print(f"   ... dan {len(recipe['bahan']) - 8} bahan lainnya")
    
    # Tampilkan 3 langkah pertama
    steps_list = [step.strip() for step in str(recipe['langkah']).split('--') if step.strip()]
    print(f"\n👨‍🍳 LANGKAH-LANGKAH (preview):")
    for i, step in enumerate(steps_list[:3], 1):
        shortened_step = step[:80] + "..." if len(step) > 80 else step
        print(f"   {i}. {shortened_step}")
    if len(steps_list) > 3:
        print(f"   ... dan {len(steps_list) - 3} langkah lainnya")

# Fungsi utama untuk menjalankan program
def main():
    """
    Fungsi utama untuk menjalankan seluruh proses
    """
    print("🚀 MEMUAT DATA RESEP DARI EXCEL...")
    
    # Ganti dengan path file Excel Anda
    file_path = "dataset_lengkap.xlsx"  # Pastikan file ini ada di folder yang sama
    
    try:
        # 1. Load data dari Excel
        recipes_db = load_recipes_from_excel(file_path)
        
        if not recipes_db:
            print("❌ Tidak ada data yang berhasil dimuat. Periksa file Excel Anda.")
            return
        
        print("✅ Data berhasil dimuat dari Excel")
        
        # 2. Simpan ke Excel (tanpa loves dan url)
        save_recipes_to_excel(recipes_db, 'resep_database_terorganisir.xlsx')
        
        # 3. Tampilkan analisis
        analyze_recipes_database(recipes_db)
        
        # 4. Contoh penggunaan lainnya
        print("\n" + "="*70)
        print("🎯 CONTOH PENGGUNAAN FUNGSI")
        print("="*70)
        
        # a. Tampilkan resep sederhana (paling sedikit bahan)
        print("\n--- 🥘 RESEP SEDERHANA (paling sedikit bahan) ---")
        simple_recipes = get_simple_recipes(recipes_db, 3)
        for i, recipe in enumerate(simple_recipes, 1):
            print(f"\n⭐ {i}. {recipe['nama']} - {len(recipe['bahan'])} bahan")
            display_recipe_details(recipe)
        
        # b. Cari resep berdasarkan kategori
        print("\n--- 🍗 RESEP AYAM (contoh) ---")
        resep_ayam = get_recipes_by_category(recipes_db, 'ayam')
        print(f"Jumlah resep ayam: {len(resep_ayam)}")
        if resep_ayam:
            display_recipe_details(resep_ayam[0])  # Tampilkan resep pertama
        
        # c. Cari resep berdasarkan bahan
        print("\n--- 🧄 RESEP DENGAN BAWANG PUTIH ---")
        resep_bawang_putih = search_recipes_by_ingredient(recipes_db, 'bawang putih')
        total_with_garlic = sum(len(recipes) for recipes in resep_bawang_putih.values())
        print(f"Jumlah resep dengan bawang putih: {total_with_garlic}")
        
        # d. Tampilkan statistik kategori
        print("\n--- 📊 STATISTIK KATEGORI ---")
        for category in recipes_db.keys():
            count = len(recipes_db[category])
            print(f"   {category}: {count} resep")
        
        print(f"\n🎉 Proses selesai! File Excel telah dibuat: 'resep_database_terorganisir.xlsx'")
        print("📁 File berisi multiple sheets untuk analisis yang lebih mudah.")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' tidak ditemukan.")
        print("   Pastikan file Excel ada di folder yang sama dengan script ini.")
    except Exception as e:
        print(f"❌ Error: {e}")

# Jalankan program utama
if __name__ == "__main__":
    main()