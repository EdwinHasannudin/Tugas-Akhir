# 🔍 Analisis Duplikasi Nama Ingredient - "ikan ikan"

## 📋 Executive Summary
Pencarian komprehensif dilakukan di seluruh workspace untuk mengidentifikasi logika pemrosesan nama ingredient yang mungkin menghasilkan duplikasi seperti "ikan ikan". Analisis mencakup 5 file Python pipeline dan 7+ file TypeScript frontend.

---

## 🗂️ Struktur Pipeline Data

```
[nutrition.csv] 
    ↓
[STEP 1: scaling_nutrition.py] → nutrition_pipeline.xlsx
    ↓
[STEP 2: onehot_encoding_nutrition.py] → One-Hot Encoded + Normalisasi + Klasifikasi texture & kategori
    ↓
[STEP 3: pembersihan.py] → Data Cleaned (dehuplikasi)
    ↓
[STEP 4: pembagian.py] → Split ke sheet terpisah per kategori
    ↓
[scripts/extractNutritionData.py] → ingredientsData.ts (TypeScript)
    ↓
[Frontend React: DemoSystemPage, RecommendationPage] → Display
```

---

## 🔴 AREA KRITIS: Potensi Duplikasi

### 1. **CONDITIONAL_RULES Bug** ⚠️ SUSPICIOUS
📍 **File:** `scripts/extractNutritionData.py` (baris 50-51)

```python
CONDITIONAL_RULES = {
    'daun': ['bawang', 'singkong', 'katuk', 'bayam', 'pepaya', 'kelor'],  
    'jagung': ['jagung kuning'], 
    'jamur': ['kuping', 'tiram'],
    'tomat': ['merah'], 
    'ikan': ['ikan'],  # ⚠️ SELF-REFERENTIAL!
}
```

**Masalah:**
- Keyword `'ikan'` dipetakan ke companion `['ikan']`
- Logika checking (baris 81-87):
  ```python
  for keyword, allowed_companions in CONDITIONAL_RULES.items():
      if keyword.lower() in name_lower:  # 'ikan' in 'ikan'? YES
          has_companion = any(comp.lower() in name_lower for comp in allowed_companions)
          # any('ikan' in 'ikan')? YES → LOLOS
          if not has_companion:
              return False
  ```
  
- **Impact:** Bahan apapun yang mengandung kata 'ikan' akan LOLOS
- **Contoh:** 
  - `"ikan"` ✓ lolos 
  - `"ikan bandeng"` ✓ lolos 
  - `"ikan tongkol"` ✓ lolos
  
**Rekomendasi Fix:**
```python
'ikan': ['bandeng', 'kembung', 'tongkol', 'salmon', 'tuna'],  # Specific types
# ATAU hapus sama sekali jika semua ingredient ikan ingin dimasukkan
```

---

### 2. **Data Cleaning Pipeline - Dehuplikasi** ✅ WORKING
📍 **File:** `nutrition/pembersihan.py` (STEP 3, baris 220-238)

```python
# Step 4: Hapus duplikat
df_cleaned['_name_lower'] = df_cleaned['name'].str.lower().str.strip()
duplicated_mask = df_cleaned.duplicated(subset='_name_lower', keep='first')
df_cleaned = df_cleaned.drop_duplicates(subset='_name_lower', keep='first')
```

**Status:** ✅ Logika dengan benar:
- Membuat kolom bantu normalisasi (lowercase + strip)
- Perbandingan case-insensitive
- Keep only first occurrence
- Hapus kolom bantu setelah selesai

---

### 3. **Ingredient Detection dari Dish Name** 🔎 POTENTIAL ISSUE
📍 **File:** `src/utils/ingredientSearch.ts` (baris 225-330)

**Fungsi:** `detectIngredientFromDish(dishName)`

**Alur Kerja:**
```
Input: "Ikan Goreng" / "Kare Ikan" / "Ikan Ikan"
   ↓
Split: ['ikan', 'goreng'] → ['ikan', 'kare', 'ikan']
   ↓
Filter COOKING_TERMS: ['ikan'] → ['ikan']
   ↓
1. Tahap 1: Cocokkan 2-word combos (ikan goreng, kare ikan, ikan ikan)
2. Tahap 2: Single word alias matching (ikan → ['Ikan Bandeng', 'Ikan Kembung', ...])
3. Tahap 3: Direct database word-boundary match
```

**KEYWORD_ALIASES (baris 66):**
```typescript
'ikan': ['Ikan'],  // Direferensikan ke nama generic
```

**Potensi Issue:**
- Jika database punya ingredient dengan nama tepat `"Ikan"` (tanpa suffix), 
  dan user input `"ikan ikan"` → kedua kata akan di-map ke `"Ikan"` di database
- Tapi hasil akhir adalah single ingredient object, tidak duplikasi literal

**Status:** ❓ Tidak ditemukan duplikasi di database saat ini

---

### 4. **Data Ekstraksi TypeScript** ✅ CLEAN
📍 **File:** `scripts/extractNutritionData.py` (baris 133-164)

```python
def generate_typescript_file(ingredients):
    ts_lines.append(f"    name: '{ingredient['name']}',")
    # Tidak ada penggabungan/transformasi tambahan
```

**Status:** ✅ Tidak ada transformasi yang menggandakan nama

**Hasil Current di `ingredientsData.ts`:**
```typescript
{ 
  id: 'ikan-bandeng',
  name: 'Ikan Bandeng',      // ✓ Clean name
  category: 'lauk',
  ...
},
{
  id: 'ikan-kembung',
  name: 'Ikan Kembung',        // ✓ Clean name
  category: 'lauk',
  ...
},
{
  id: 'ikan-tongkol',
  name: 'Ikan tongkol',        // ✓ Clean name (case inconsistent tapi OK)
  category: 'lauk',
  ...
}
```

---

### 5. **Frontend Display** ✅ NO DUPLICATION
📍 **File:** `src/components/RecommendationPage.tsx` & `DemoSystemPage.tsx`

**Display Template:**
```typescript
// RecommendationPage.tsx (line 180)
<span className="font-semibold text-gray-800">{ingredient.name}</span>
<span>{ingredient.category}</span>

// DemoSystemPage.tsx (line 184)
<span className="text-gray-900">{rec.ingredient.name}</span>
<span className="text-xs text-gray-400">{rec.ingredient.category}</span>
```

**Status:** ✅ Tidak ada penggabungan atau transformasi string yang menghasilkan duplikasi

---

## 📊 Temuan Kandidat Terkuat untuk Duplikasi

### Kandidat 1: Data Asli Excel (MOST LIKELY)
- File: `nutrition/dataset/nutrition.csv` atau `nutrition_pipeline.xlsx`
- Ada kemungkinan sheet "Lauk" atau "Sayuran" memiliki 2+ baris dengan nama "Ikan"
- Jika dehuplikasi tidak sepenuhnya bekerja, bisa menghasilkan duplikat

**Cara Check:**
```bash
# Buka nutrition_pipeline.xlsx
# Check sheet "Lauk" dan "Sayuran" 
# Cari berapa baris dengan nama mengandung "ikan"
```

### Kandidat 2: CONDITIONAL_RULES Logic (LIKELY)
- Jika ada data "ikan" (lowercase) di Excel
- Setelah cleaning, menjadi "Ikan" 
- Tapi sebelum dehuplikasi di pembersihan.py, ada 2 baris dengan nama similar
- Misal: "ikan" + "ikan merah" → after strip → "ikan" + "ikan merah"
- Kemudian lowercasing untuk dedupe: "ikan" vs "ikan merah" = berbeda

### Kandidat 3: onehot_encoding Classification (UNLIKELY)
- Kategori dibuat dari CATEGORY_KEYWORDS matching
- Bukan dari penggabungan string

---

## 🛠️ Rekomendasi Perbaikan

### 1. **Perbaiki CONDITIONAL_RULES** - PRIORITY HIGH
```python
# Sebelum:
'ikan': ['ikan'],

# Sesudah - Opsi A: Hapus aturan
# (biarkan semua ingredient "ikan" masuk tanpa syarat)
# CONDITIONAL_RULES = {
#     'daun': [...],
#     'jagung': [...],
#     'tomat': [...],
#     # 'ikan' dihapus
# }

# Atau Opsi B: Spesifikkan tipe ikan
'ikan': ['bandeng', 'kembung', 'tongkol', 'salmon'],
```

### 2. **Tambah Validation di extractNutritionData.py**
```python
# Cek sebelum generate_typescript_file()
def validate_ingredients(ingredients):
    """Cek duplikasi dan anomali"""
    names = [ing['name'].lower() for ing in ingredients]
    duplicates = set([x for x in names if names.count(x) > 1])
    if duplicates:
        print(f"⚠️  WARNING: Duplikasi ditemukan: {duplicates}")
        for dup in duplicates:
            matching = [ing for ing in ingredients if ing['name'].lower() == dup]
            print(f"   - '{dup}': {len(matching)} entries")
    return len(duplicates) == 0
```

### 3. **Enhance Dehuplikasi di pembersihan.py**
```python
# Tambah check untuk partial matches
# Contoh: "ikan" vs "ikan merah" jika stemming sama
def enhanced_dedupe(df):
    # Sudah ada logic baik, tapi bisa tambah logging
    before = len(df)
    df_deduped = df.drop_duplicates(subset=['_name_lower'], keep='first')
    removed = before - len(df_deduped)
    print(f"[DEDUPE] Removed {removed} exact duplicates")
    return df_deduped
```

### 4. **Test Coverage - Add Unit Test**
```python
# nutrition/test_pendant.py
def test_no_duplicates_after_cleaning():
    """Pastikan tidak ada duplikasi setelah pembersihan"""
    df = load_cleaned_data()
    names_lower = df['name'].str.lower().str.strip()
    duplicates = names_lower[names_lower.duplicated(keep=False)]
    assert len(duplicates) == 0, f"Found duplicates: {duplicates.unique()}"

def test_conditional_rules():
    """Test bahwa conditional rules tidak menciptakan weird patterns"""
    from scripts.extractNutritionData import should_include
    
    # Test case: ingredient dengan nama "ikan"
    result, reason = should_include("ikan")
    assert result == True, "Pure 'ikan' should pass"
    
    # Test case: ingredient khusus
    result2, reason2 = should_include("ikan bandeng")
    assert result2 == True, "Specific fish should pass"
```

---

## 📝 Checklist: Verifikasi No Duplikasi

- [x] ✅ Cek data TypeScript current: Tidak ada "ikan ikan" atau duplikasi literal
- [x] ✅ Cek pipeline cleaning: Dehuplikasi berfungsi dengan baik
- [x] ✅ Cek frontend display: Tidak ada transformasi yang menggandakan
- [ ] ❓ **PERLU DICHECK:** Raw data di `nutrition.csv` / Excel
- [ ] ❓ **PERLU DITEST:** Jalankan pembersihan.py dengan logging verbose
- [ ] ❓ **PERLU REVIEW:** CONDITIONAL_RULES logic di extractNutritionData.py

---

## 🔗 File-file Terkait

| File | Lokasi | Fungsi | Status |
|------|--------|--------|--------|
| `nutrition.csv` | `nutrition/dataset/` | Data asli | ⚠️ BELUM DICHECK (Raw) |
| `scaling_nutrition.py` | `nutrition/` | STEP 1: Normalisasi | ✅ OK |
| `onehot_encoding_nutrition.py` | `nutrition/` | STEP 2: Klasifikasi | ✅ OK |
| `pembersihan.py` | `nutrition/` | STEP 3: Dehuplikasi | ✅ OK |
| `pembagian.py` | `nutrition/` | STEP 4: Split kategori | ✅ OK |
| `extractNutritionData.py` | `scripts/` | Extract ke TS | ⚠️ CONDITIONAL_RULES ISSUE |
| `ingredientsData.ts` | `src/data/` | Output data | ✅ CLEAN |
| `ingredientSearch.ts` | `src/utils/` | Detection logic | ✅ OK |
| `RecommendationPage.tsx` | `src/components/` | Display | ✅ OK |

---

## 🎯 Kesimpulan

**Sumber Potensial Duplikasi "ikan ikan":**
1. **Data asli Excel** - Ada kemungkinan 2 baris dengan nama mirip
2. **CONDITIONAL_RULES** - Self-referential rule bisa menyebabkan odd behavior
3. **Frontend** - Tidak ada duplikasi di tampilan akhir

**Rekomendasi Utama:**
1. ✅ Perbaiki CONDITIONAL_RULES (priority HIGH)
2. ✅ Run comprehensive test di pipeline pembersihan
3. ✅ Add validation untuk duplikasi
4. ✅ Review raw data Excel

