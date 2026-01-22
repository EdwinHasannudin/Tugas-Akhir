# Nutrition Data Processing

## 📊 Files Overview

### `scaling_nutrition.py` ⭐ (RECOMMENDED)
**Clean code untuk Min-Max Scaling nutrisi**

- **Fungsi:**
  - `apply_minmax_scaling()` - Melakukan min-max scaling pada kolom: calories, proteins, fat, carbohydrate
  - `save_to_excel()` - Menyimpan hasil ke Excel dengan format rapi dan mudah dibaca

- **Input:** `nutrition.csv`
- **Output:** `nutrition_scaled.xlsx` (Excel dengan formatting profesional)

- **Cara Menggunakan:**
  ```bash
  python scaling_nutrition.py
  ```

- **Formula Min-Max Scaling:**
  ```
  X_scaled = (X - X_min) / (X_max - X_min)
  Result: 0 ≤ X_scaled ≤ 1
  ```

### `process_nutrition.py`
File lama untuk klasifikasi kategori dan texture makanan. 
**Gunakan jika ingin:** menambahkan kolom kategori dan texture pada data nutrisi.

### `nutrition.csv`
Data nutrisi original (1346 bahan makanan) dengan kolom:
- `id` - Identitas unik
- `name` - Nama makanan
- `calories` - Energi (kkal)
- `proteins` - Protein (g)
- `fat` - Lemak (g)
- `carbohydrate` - Karbohidrat (g)
- `image` - URL gambar

### `nutrition_scaled.xlsx` 
**Output file - Excel hasil scaling dengan format:**
- Header: Warna biru, text putih, bold
- Data: Center aligned, 4 desimal untuk kolom numerik
- Border: Semua cell terborder rapi
- Column width: Auto-adjusted untuk readability

---

## 🎯 Quick Start

```python
from scaling_nutrition import apply_minmax_scaling, save_to_excel
import pandas as pd

# Baca data
df = pd.read_csv('nutrition.csv')

# Apply scaling
df_scaled = apply_minmax_scaling(df)

# Simpan ke Excel
save_to_excel(df_scaled, 'nutrition_scaled.xlsx')
```

---

## 📈 Data Scaling Example

**Sebelum Scaling:**
| Name | Calories | Proteins | Fat | Carbohydrate |
|------|----------|----------|-----|--------------|
| Abon | 280 | 9.2 | 28.4 | 0 |
| Abon haruwan | 513 | 23.7 | 37 | 21.3 |

**Setelah Scaling (0-1):**
| Name | Calories | Proteins | Fat | Carbohydrate |
|------|----------|----------|-----|--------------|
| Abon | 0.2979 | 0.1108 | 0.284 | 0.0000 |
| Abon haruwan | 0.5457 | 0.2855 | 0.370 | 0.0329 |

---

## 🔧 Dependencies

```
pandas
scikit-learn (MinMaxScaler)
openpyxl (untuk Excel formatting)
```

Install dengan:
```bash
pip install pandas scikit-learn openpyxl
```

---

## ✅ Notes

- Min-Max Scaling normalize nilai ke range 0-1
- Cocok untuk: machine learning, content-based filtering, similarity calculation
- File original tidak berubah, output ke file baru
- Excel output mudah dibaca dan professional-looking
