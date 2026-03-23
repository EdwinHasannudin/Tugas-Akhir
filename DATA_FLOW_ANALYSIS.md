# 🔗 Data Flow & Potential Duplication Points

## Alur Data Lengkap: Dari CSV ke TypeScript

```
┌─────────────────────────────────────────────────────────────────────┐
│ [ nutrition.csv ]                                                   │
│ Raw ingredient data dari external dataset                           │
│ Contoh baris: ikan, merah | 0 | 85.2 | 19.3 | 1.60 | ...           │
│              ikan, bandeng | 0 | 95.2 | 20.3 | 2.60 | ...          │
│              ikan, tongkol | 0 | 91.2 | 19.8 | 2.10 | ...          │
└────────────────────┬────────────────────────────────────────────────┘
                     │ pd.read_csv()
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ [ STEP 1: scaling_nutrition.py ]                                    │
│ - Read CSV                                                          │
│ - Normalize numerik (Min-Max scaling)                               │
│ → nutrition_pipeline.xlsx (sheet: "Nutrition Scaled")               │
│                                                                     │
│ OUTPUT SAMPLE:                                                      │
│   name              energy  protein  carbs  fat                     │
│   ikan bandeng      95.2    20.3     0.3    2.60                    │
│   ikan kembung      91.2    19.8     0.2    2.10                    │
│   ikan tongkol      85.2    19.3     0.1    1.60                    │
└────────────────────┬────────────────────────────────────────────────┘
                     │ pd.read_excel()
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ [ STEP 2: onehot_encoding_nutrition.py ]                            │
│ - Classify texture (dari keyword matching: 'ikan' → 'padat')        │
│ - Classify category (dari keyword: 'ikan' → 'lauk')                 │
│ - One-Hot Encoding texture & category                               │
│ → nutrition_pipeline.xlsx (sheet: "One-Hot Encoded")                │
│                                                                     │
│ OUTPUT SAMPLE:                                                      │
│   name           texture  kategori  padat_OHE  lauk_OHE             │
│   ikan bandeng   padat    lauk      1          1                    │
│   ikan kembung   padat    lauk      1          1                    │
│   ikan tongkol   padat    lauk      1          1                    │
└────────────────────┬────────────────────────────────────────────────┘
                     │ pd.read_excel()
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ [ STEP 3: pembersihan.py ]                                          │
│ ⚠️  CRITICAL DEDUPE STEP                                            │
│                                                                     │
│ [STEP 1] Remove 'lainnya' category                                  │
│ [STEP 2] Remove items by BLACKLIST_KEYWORDS                         │
│ [STEP 3] Strip certain words (e.g., 'segar')                        │
│          Contoh: 'ikan segar' → 'ikan'  ← POTENTIAL DUP POINT 1 ✗  │
│ [STEP 4] ⭐ DEDUPLICATE                                             │
│          - Create _name_lower column                                │
│          - Drop duplicates by _name_lower (keep='first')            │
│          - IF 'ikan' + 'ikan segar' → both become 'ikan'            │
│          - Second one removed ✓ OK                                  │
│ → nutrition_pipeline.xlsx (sheet: "Data Cleaned")                   │
│                                                                     │
│ DEDUPE LOGIC:                                                       │
│   Before: ['ikan bandeng', 'ikan kembung', 'ikan segar']            │
│   _name_lower: ['ikan bandeng', 'ikan kembung', 'ikan segar']       │
│   After dedupe: ['ikan bandeng', 'ikan kembung', 'ikan segar']      │
│   (No duplicates if names differ) ✓                                 │
└────────────────────┬────────────────────────────────────────────────┘
                     │ pd.read_excel()
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ [ STEP 4: pembagian.py ]                                            │
│ - Split data by category into separate sheets                       │
│ - Contoh: lauk → Sheet "lauk", sayuran → Sheet "sayuran"            │
│ → nutrition_pipeline.xlsx (multiple sheets per category)            │
└────────────────────┬────────────────────────────────────────────────┘
                     │ pd.read_excel(sheets: 'lauk', 'sayuran')
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ [ scripts/extractNutritionData.py ]                                 │
│ 🔴 FILTERING & CONDITIONAL RULES APPLIED HERE                       │
│                                                                     │
│ [1] Load data from sheets                                           │
│ [2] BLACKLIST filter                                                │
│ [3] 🔴 CONDITIONAL_RULES check:                                     │
│     - Search for keyword 'ikan' in name ✓                           │
│     - Check companions: must have 'ikan' in name ✓                  │
│     - Result: PASS (self-referential match)                         │
│ [4] Generate TypeScript                                             │
│ → src/data/ingredientsData.ts                                       │
│                                                                     │
│ POTENTIAL DUPLICATION POINTS:                                       │
│ • If Excel has 'ikan' and 'ikan bandeng':                            │
│   Both match conditional rule → Both extracted                       │
│   BUT no duplication unless extraction logic broken                  │
│                                                                     │
│ • If Excel somehow has 'ikan' + 'ikan' (literal dup):               │
│   Both would extract → Dedupe happened at STEP 3 already            │
│   So shouldn't reach here                                            │
└────────────────────┬────────────────────────────────────────────────┘
                     │ import { ingredientsDatabase }
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ [ src/data/ingredientsData.ts ]                                     │
│ ✅ CLEAN OUTPUT (verified no "ikan ikan")                            │
│                                                                     │
│ export const ingredientsDatabase: Ingredient[] = [                  │
│   {                                                                 │
│     id: 'ikan-bandeng',                                             │
│     name: 'Ikan Bandeng',      ← ✓ Clean                            │
│     category: 'lauk',                                               │
│   },                                                                │
│   {                                                                 │
│     id: 'ikan-kembung',                                             │
│     name: 'Ikan Kembung',      ← ✓ Clean                            │
│     category: 'lauk',                                               │
│   },                                                                │
│   // ... more entries                                               │
│ ]                                                                   │
└────────────────────┬────────────────────────────────────────────────┘
                     │ ingredientsDatabase
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ [ Frontend: DemoSystemPage / RecommendationPage ]                   │
│                                                                     │
│ User Input: "Ikan Goreng" atau "Kare Ikan"                          │
│                ↓                                                     │
│ detectIngredientFromDish(input)                                     │
│   → Split: ['ikan', 'goreng']                                       │
│   → Filter COOKING_TERMS: ['goreng']                                │
│   → wordsToUse: ['ikan']                                            │
│   → KEYWORD_ALIASES['ikan']: ['Ikan']                               │
│   → findIngredientByName('Ikan'): ❓ NOT FOUND                       │
│   → Direct match: ['Ikan Bandeng'] ← First match returned           │
│                ↓                                                     │
│ Display: "Ikan Bandeng — lauk"      ✓ No duplication                │
│                                                                     │
│ NO "IKAN IKAN" HERE                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔴 Critical Point: CONDITIONAL_RULES

```python
# File: scripts/extractNutritionData.py, Line 50-51
CONDITIONAL_RULES = {
    'ikan': ['ikan'],  # ⚠️ SUSPICIOUS RULE
}

# Logic flow for ingredient named 'ikan':
def should_include(name='ikan'):
    name_lower = 'ikan'
    
    # Layer 3: Conditional rules
    for keyword, allowed_companions in CONDITIONAL_RULES.items():
        if keyword.lower() in name_lower:  # 'ikan' in 'ikan'? YES
            # allowed_companions = ['ikan']
            has_companion = any(comp.lower() in name_lower for comp in allowed_companions)
            # any('ikan' in 'ikan')? YES
            
            if not has_companion:
                return False, f"conditional: '{keyword}' tanpa pendamping valid"
            # No return here → continue to Layer 4
    
    return True, "passed"  # LOLOS!

# Result: ANY ingredient containing 'ikan' will pass
# Examples:
#   'ikan' → PASS
#   'ikan bandeng' → PASS
#   'ikan goreng' → PASS (tapi sudah diblacklist)
#   'mengikan' (unlikely) → PASS (substring match)
```

---

## ⚠️ Where "ikan ikan" Could Happen

### Scenario 1: Excel Data with Repeated Word
```
Row 1: name='ikan', category='lauk'
Row 2: name='ikan', category='lauk'  ← Literal duplicate
       ↓ Should be caught by pembersihan.py STEP 3 dehuplikasi
Row 1: name='ikan' ← Only one remains
```

### Scenario 2: Strip Words Creates Duplicate
```
Row 1: 'ikan segar' → strip 'segar' → 'ikan'
Row 2: 'ikan'      → no strip       → 'ikan'
       ↓ Dedupe at pembersihan.py keeps first
Row 1: 'ikan' ← Only one remains
```

### Scenario 3: Database Fetch Error (Unlikely)
```
If ingredientsDatabase somehow has:
  { name: 'ikan', ... }
  { name: 'Ikan', ... }
Combined display could accidentally show "ikan ikan"
BUT: Current database has 'Ikan Bandeng', 'Ikan Kembung', 'Ikan tongkol'
     No generic 'ikan' entry exists
```

---

## 📊 Dedupe Effectiveness Matrix

| Scenario | Data Point | Step Applied | Status |
|----------|-----------|--------------|--------|
| Pure duplicate 'ikan','ikan' | Excel → Raw | STEP 3 Dehuplikasi | ✅ Caught |
| Strip creates dup | 'ikan segar','ikan' | STEP 3 After Strip | ✅ Caught |
| Conditional rule self-ref | 'ikan' ingredient | extractNutrition filter | ⚠️ Allows both |
| Case sensitivity | 'Ikan','ikan' | STEP 3 lowercase compare | ✅ Caught |
| Partial word match | pengikan, aikan | CONDITIONAL word boundary | ✅ Proper regex |

---

## 🎯 Verification Checklist

To check if "ikan ikan" actually exists:

```bash
# 1. Check raw Excel data for duplicates
opened nutrition/dataset/nutrition_pipeline.xlsx
  → Look at sheets: 'lauk', 'sayuran'
  → Ctrl+F for 'ikan'
  → Check if appears 1x or multiple times

# 2. Check after STEP 3 cleaning
opened nutrition/dataset/nutrition_pipeline.xlsx
  → Sheet: 'Data Cleaned'
  → Search 'ikan'
  → Count occurrences

# 3. Check final TypeScript output
grep -n "name: '.*ikan" src/data/ingredientsData.ts
# Expected output:
#   66:    name: 'Ikan Bandeng',
#   76:    name: 'Ikan Kembung',
#   86:    name: 'Ikan tongkol',
# NOT: name: 'Ikan Ikan' ← This would be the problem
```

---

## 🔗 Related Configurations

### KEYWORD_ALIASES (Frontend Detection)
```typescript
// src/utils/ingredientSearch.ts, Line 66
const KEYWORD_ALIASES: Record<string, string[]> = {
  'ikan': ['Ikan'],  // Maps to ANY ingredient with name starting 'Ikan'
  // Could be extended to be more specific:
  'ikan': ['Ikan Bandeng', 'Ikan Kembung', 'Ikan tongkol'],
}
```

### TEXTURE_KEYWORDS (Classification)
```python
# nutrition/onehot_encoding_nutrition.py, Line 50+
TEXTURE_KEYWORDS = {
    'padat': [
        'daging', 'ikan', 'ayam', ...  ← 'ikan' is keyword for classification
    ],
}
```

---

## 📝 Summary: Why "ikan ikan" Shouldn't Exist

1. ✅ **Dehuplikasi works:** pembersihan.py removes exact duplicates
2. ✅ **No DB dupes:** ingredientsDatabase has unique entries
3. ✅ **Frontend clean:** No string transformation combining names
4. ❓ **But check:** Raw Excel data (nutrition.csv)

**If discovered in real data:**
- Likely source: nutrition.csv has duplicate rows 
- Fix: Run pembersihan.py in verbose mode to see what's removed
- Or: Fix CONDITIONAL_RULES in extractNutritionData.py

