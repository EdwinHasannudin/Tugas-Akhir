import os
import re
import math
import matplotlib.pyplot as plt
import numpy as np

def load_ingredients_from_ts(filepath):
    """
    Extrak data dari ingredientsData.ts tanpa memerlukan Node.js.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_idx = content.find('[')
    end_idx = content.rfind(']')
    if start_idx == -1 or end_idx == -1:
        return []
        
    array_content = content[start_idx+1:end_idx]
    ingredients = []
    
    obj_pattern = re.compile(r'\{\s*(.*?)\s*\}', re.DOTALL)
    for match in obj_pattern.finditer(array_content):
        obj_str = match.group(1)
        ingredient = {}
        lines = obj_str.split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.endswith(','): line = line[:-1]
            if ':' not in line: continue
            
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            
            try:
                if '.' in val or val.isdigit() or val == '0':
                    val = float(val)
            except ValueError:
                pass
                
            ingredient[key] = val
            
        if 'id' in ingredient:
            ingredients.append(ingredient)
            
    return ingredients

def to_vector(ingredient):
    """Mengubah dictionary ke bentuk vektor numerik fitur"""
    features = [
        float(ingredient.get('energy', 0)),
        float(ingredient.get('protein', 0)),
        float(ingredient.get('carbs', 0)),
        float(ingredient.get('fat', 0))
    ]
    categories = ['lauk', 'sayuran', 'rempah', 'tepung', 'cair']
    for cat in categories:
        features.append(1 if ingredient.get('category') == cat else 0)
        
    textures = ['padat', 'cair', 'bubuk', 'biji']
    for tex in textures:
        features.append(1 if ingredient.get('texture') == tex else 0)
        
    return features

# ====================================================================
# SIMILARITY & DISTANCE FUNCTIONS
# ====================================================================
def euclidean_similarity(v1, v2):
    """Euclidean distance - normalized ke range 0-1"""
    dist = math.sqrt(sum((a-b)**2 for a,b in zip(v1, v2)))
    return dist

def manhattan_similarity(v1, v2):
    """Manhattan distance"""
    return sum(abs(a-b) for a,b in zip(v1, v2))

def cosine_similarity(v1, v2):
    """Cosine similarity"""
    dot = sum(a*b for a,b in zip(v1, v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(b*b for b in v2))
    if mag1 == 0 or mag2 == 0: return 0
    return dot / (mag1 * mag2)

# ====================================================================
# EVALUATION METRICS (MAE & RMSE for Content Feature Error)
# ====================================================================
def calc_mae(v_actual, v_predicted):
    """Mean Absolute Error (seberapa meleset nilai fitur rekomendasi secara numerik)"""
    v_a = v_actual[:4]
    v_p = v_predicted[:4]
    n = len(v_a)
    return sum(abs(a - b) for a, b in zip(v_a, v_p)) / n

def calc_rmse(v_actual, v_predicted):
    """Root Mean Squared Error (seberapa meleset nilai fitur rekomendasi, penalize lebih pada perbedaan fitur yang besar)"""
    v_a = v_actual[:4]
    v_p = v_predicted[:4]
    n = len(v_a)
    return math.sqrt(sum((a - b)**2 for a, b in zip(v_a, v_p)) / n)

def main():
    print("=" * 60)
    print("EVALUASI PERFORMA SISTEM (MAE & RMSE)")
    print("=" * 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    filepath = os.path.join(project_root, 'src', 'data', 'ingredientsData.ts')
    
    if not os.path.exists(filepath):
        print(f"[ERROR] File database tidak ditemukan di:\n{filepath}")
        return
        
    print("[1] Membaca database bahan...")
    db = load_ingredients_from_ts(filepath)
    if not db:
        print("[ERROR] Gagal memuat database bahan!")
        return
        
    query = input("\n[2] Masukkan nama bahan query target (contoh: 'ayam'): ").strip()
    if not query:
        print("Input kosong. Program dihentikan.")
        return
        
    try:
        k_input = input("[3] Berapa target Top-K rekomendasi yang ingin dievaluasi (default 5): ").strip()
        top_k = int(k_input) if k_input.isdigit() else 5
    except ValueError:
        top_k = 5
        
    query_lower = query.lower()
    query_ing = None
    for item in db:
        if str(item.get('name', '')).lower() == query_lower or str(item.get('id', '')).lower() == query_lower:
            query_ing = item
            break
            
    if not query_ing:
        print(f"\n[ERROR] Bahan '{query}' tidak ditemukan di database.")
        return
        
    print(f"\n[4] Memproses Rekomendasi Top-{top_k} untuk '{query_ing['name']}'...")
    
    qv = to_vector(query_ing)
    
    results = []
    for ing in db:
        if ing.get('id') == query_ing.get('id'): 
            continue
            
        tv = to_vector(ing)
        
        # Hitung ketiga similarity metrics
        euc = euclidean_similarity(qv, tv)
        man = manhattan_similarity(qv, tv)
        cos = cosine_similarity(qv, tv)
        
        # Hitung rata-rata dari ketiga metode
        avg = (euc + man + cos) / 3
        
        # Hitung MAE dan RMSE untuk setiap bahan pengganti
        mae = calc_mae(qv, tv)
        rmse = calc_rmse(qv, tv)
        
        results.append({
            'name': ing.get('name', 'Unknown'),
            'vector': tv,
            'euclidean': euc,
            'manhattan': man,
            'cosine': cos,
            'avg': avg,
            'mae_score': mae,
            'rmse_score': rmse
        })
        
    # Ambil Top K berdasarkan rata-rata (Avg)
    top_k_results = sorted(results, key=lambda x: x['avg'])[:top_k]
    
    # Hitung rata-rata metrics dari top-k
    avg_euc = sum(item['euclidean'] for item in top_k_results) / len(top_k_results)
    avg_man = sum(item['manhattan'] for item in top_k_results) / len(top_k_results)
    avg_cos = sum(item['cosine'] for item in top_k_results) / len(top_k_results)
    avg_mae = sum(item['mae_score'] for item in top_k_results) / len(top_k_results)
    avg_rmse = sum(item['rmse_score'] for item in top_k_results) / len(top_k_results)

    # OUTPUT TERMINAL (TEKS-ANGKA)
    print("\n" + "=" * 90)
    print("HASIL EVALUASI - REKOMENDASI PENGGANTI BAHAN")
    print("=" * 90)
    
    print(f"\n📌 BAHAN INPUT: '{query_ing['name']}'")
    print(f"   • Energy: {query_ing.get('energy', 0)} | Protein: {query_ing.get('protein', 0)} | Carbs: {query_ing.get('carbs', 0)} | Fat: {query_ing.get('fat', 0)}")
    print(f"   • Category: {query_ing.get('category', 'N/A')} | Texture: {query_ing.get('texture', 'N/A')}")
    
    print(f"\n📋 TOP-{top_k} BAHAN PENGGANTI (Diurutkan berdasarkan Avg):")
    print("-" * 90)
    print(f"{'No':<4} {'Bahan':<20} {'Euclidean':<12} {'Manhattan':<12} {'Cosine':<12} {'Avg':<12} {'MAE':<10} {'RMSE':<10}")
    print("-" * 90)
    
    for idx, item in enumerate(top_k_results, 1):
        print(f"{idx:<4} {item['name']:<20} {item['euclidean']:<12.5f} {item['manhattan']:<12.5f} {item['cosine']:<12.5f} {item['avg']:<12.5f} {item['mae_score']:<10.5f} {item['rmse_score']:<10.5f}")
    
    print("-" * 90)
    
    print(f"\n📊 RATA-RATA METRIK (Top {top_k}):") 
    print(f"   • Avg Euclidean:  {avg_euc:.5f}")
    print(f"   • Avg Manhattan:  {avg_man:.5f}")
    print(f"   • Avg Cosine:     {avg_cos:.5f}")
    print(f"   • Avg MAE:        {avg_mae:.5f}")
    print(f"   • Avg RMSE:       {avg_rmse:.5f}")

    # ====================================================================
    # VISUALISASI MATPLOTLIB - METRIK SIMILARITY & ERROR
    # ====================================================================
    print("\n[INFO] Mempersiapkan grafik visualisasi Matplotlib...")

    labels = [item['name'][:18] for item in top_k_results]
    mae_scores = [item['mae_score'] for item in top_k_results]
    rmse_scores = [item['rmse_score'] for item in top_k_results]
    
    # Buat grafik untuk Error Metrics (MAE & RMSE)
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.suptitle(f"Evaluasi Rekomendasi Bahan Pengganti vs Bahan Input: '{query_ing['name']}'", 
                 fontsize=14, fontweight='bold', y=0.995)
    fig.canvas.manager.set_window_title(f"Evaluation - {query_ing['name']}")
    
    x = np.arange(len(labels))
    width = 0.35
    
    # ====== Error Metrics (MAE & RMSE) ======
    rects1 = ax.bar(x - width/2, mae_scores, width, label='MAE (Mean Absolute Error)', 
                    color='#FFB347', edgecolor='black', linewidth=1)
    rects2 = ax.bar(x + width/2, rmse_scores, width, label='RMSE (Root Mean Squared Error)', 
                    color='#87CEEB', edgecolor='black', linewidth=1)
    
    ax.set_ylabel('Error Value', fontsize=11, fontweight='bold')
    ax.set_title('Error Metrics (MAE & RMSE)', fontsize=12, fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontweight='bold', rotation=20, ha='right', fontsize=10)
    ax.legend(loc='upper left', fontsize=10, framealpha=0.95)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add value labels
    def add_value_labels(ax, rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 2),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    for rects in [rects1, rects2]:
        add_value_labels(ax, rects)
    
    # Tambahkan garis rata-rata dan tampilkan nilai
    ax.axhline(y=avg_mae, color='#FF8C00', linestyle='--', linewidth=2, alpha=0.7, label=f'Avg MAE: {avg_mae:.5f}')
    ax.axhline(y=avg_rmse, color='#4169E1', linestyle='--', linewidth=2, alpha=0.7, label=f'Avg RMSE: {avg_rmse:.5f}')
    
    # Update legend
    ax.legend(loc='upper left', fontsize=10, framealpha=0.95)
    
    fig.tight_layout()

    print("\n✅ Grafik telah dibuat!")
    print("   (Tutup jendela grafik untuk mengakhiri program)")
    plt.show()

if __name__ == "__main__":
    import sys
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh user.")
        sys.exit(0)