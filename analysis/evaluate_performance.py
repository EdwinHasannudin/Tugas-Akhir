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
def cosine_sim(v1, v2):
    dot = sum(a*b for a,b in zip(v1, v2))
    mag1 = math.sqrt(sum(a*a for a in v1))
    mag2 = math.sqrt(sum(b*b for b in v2))
    if mag1 == 0 or mag2 == 0: return 0
    return dot / (mag1 * mag2)

def euclidean_dist(v1, v2):
    return math.sqrt(sum((a-b)**2 for a,b in zip(v1, v2)))
    
def manhattan_dist(v1, v2):
    return sum(abs(a-b) for a,b in zip(v1, v2))

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
        c = cosine_sim(qv, tv)
        e = euclidean_dist(qv, tv)
        m = manhattan_dist(qv, tv)
        
        # Hitung seberapa 'salah' fitur hasil rekomendasi (tv) dibandingkan target fitur asli (qv)
        mae = calc_mae(qv, tv)
        rmse = calc_rmse(qv, tv)
        
        results.append({
            'name': ing.get('name', 'Unknown'),
            'vector': tv,
            'cosine': c,
            'euclidean': e,
            'manhattan': m,
            'mae_score': mae,
            'rmse_score': rmse
        })
        
    # Ambil Top K berdasarkan ketiga fungsi jarak
    top_k_cosine = sorted(results, key=lambda x: x['cosine'], reverse=True)[:top_k]
    top_k_eucl = sorted(results, key=lambda x: x['euclidean'])[:top_k]
    top_k_man = sorted(results, key=lambda x: x['manhattan'])[:top_k]
    
    # Fungsi agregasi error dari top-K
    def get_avg_errors(top_k_group):
        avg_mae = sum(item['mae_score'] for item in top_k_group) / len(top_k_group)
        avg_rmse = sum(item['rmse_score'] for item in top_k_group) / len(top_k_group)
        return avg_mae, avg_rmse
    
    avg_mae_cos, avg_rmse_cos = get_avg_errors(top_k_cosine)
    avg_mae_euc, avg_rmse_euc = get_avg_errors(top_k_eucl)
    avg_mae_man, avg_rmse_man = get_avg_errors(top_k_man)

    # OUTPUT TERMINAL (TEKS-ANGKA)
    print("\n" + "=" * 60)
    print("HASIL EVALUASI ERROR (Lebih kecil = Semakin baik relevansi fiturnya)")
    print("=" * 60)
    
    print(f"\n1. COSINE SIMILARITY (Top {top_k})")
    for idx, item in enumerate(top_k_cosine, 1):
        print(f"   {idx}. {item['name']:<20} | MAE: {item['mae_score']:.5f} | RMSE: {item['rmse_score']:.5f} | Cosine Score: {item['cosine']:.4f}")
    print("-" * 50)
    print(f"   RATA-RATA SISTEM COSINE  => MAE: {avg_mae_cos:.5f} | RMSE: {avg_rmse_cos:.5f}")
    
    print(f"\n2. EUCLIDEAN DISTANCE (Top {top_k})")
    for idx, item in enumerate(top_k_eucl, 1):
        print(f"   {idx}. {item['name']:<20} | MAE: {item['mae_score']:.5f} | RMSE: {item['rmse_score']:.5f} | Eucl Distance: {item['euclidean']:.4f}")
    print("-" * 50)
    print(f"   RATA-RATA SISTEM EUCLIDEAN => MAE: {avg_mae_euc:.5f} | RMSE: {avg_rmse_euc:.5f}")

    print(f"\n3. MANHATTAN DISTANCE (Top {top_k})")
    for idx, item in enumerate(top_k_man, 1):
        print(f"   {idx}. {item['name']:<20} | MAE: {item['mae_score']:.5f} | RMSE: {item['rmse_score']:.5f} | Manh Distance: {item['manhattan']:.4f}")
    print("-" * 50)
    print(f"   RATA-RATA SISTEM MANHATTAN => MAE: {avg_mae_man:.5f} | RMSE: {avg_rmse_man:.5f}")

    # ====================================================================
    # VISUALISASI MATPLOTLIB (3 GRAPH)
    # ====================================================================
    print("\n[INFO] Mempersiapkan 3 grafik visualisasi Matplotlib...")

    def plot_algorithm_performance(top_k_results, title, metric_key, metric_name, avg_mae, avg_rmse):
        labels = [item['name'][:15] for item in top_k_results]
        mae_scores = [item['mae_score'] for item in top_k_results]
        rmse_scores = [item['rmse_score'] for item in top_k_results]
        metric_scores = [item[metric_key] for item in top_k_results]
        
        x = np.arange(len(labels))
        width = 0.25
        
        fig, ax1 = plt.subplots(figsize=(12, 7))
        fig.canvas.manager.set_window_title(f"Performance Analysis - {title}")
        
        rects1 = ax1.bar(x - width, mae_scores, width, label='MAE', color='#ff9999', edgecolor='black')
        rects2 = ax1.bar(x, rmse_scores, width, label='RMSE', color='#66b3ff', edgecolor='black')
        
        ax2 = ax1.twinx()
        rects3 = ax2.bar(x + width, metric_scores, width, label=metric_name, color='#99ff99', edgecolor='black')
        
        ax1.set_ylabel('Error Value (MAE & RMSE)', color='black', fontsize=11)
        ax2.set_ylabel(f'{metric_name} Score', color='green', fontsize=11)
        
        ax1.set_title(f"Performa Top-{top_k}: {title}\n(Bahan: '{query_ing['name']}')", pad=20, fontweight='bold', fontsize=14)
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, fontweight='bold', rotation=15, ha='right', fontsize=11)
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=3, fontsize=11)
        
        def autolabel(ax, rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f"{height:.4f}", xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
                            
        autolabel(ax1, rects1)
        autolabel(ax1, rects2)
        autolabel(ax2, rects3)
        
        avg_text = f"Rata-rata MAE: {avg_mae:.5f}\nRata-rata RMSE: {avg_rmse:.5f}"
        ax1.text(1.0, -0.20, avg_text, transform=ax1.transAxes, fontsize=10, fontweight='bold',
                 verticalalignment='top', horizontalalignment='right',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#F8F9FA', edgecolor='#DEE2E6', alpha=0.9))
        
        ax1.grid(axis='y', linestyle='--', alpha=0.6)
        fig.tight_layout()

    def plot_summary_comparison(avg_scores):
        methods = ['Cosine', 'Euclidean', 'Manhattan']
        mae_avgs = [avg_scores['cos'][0], avg_scores['euc'][0], avg_scores['man'][0]]
        rmse_avgs = [avg_scores['cos'][1], avg_scores['euc'][1], avg_scores['man'][1]]
        
        x = np.arange(len(methods))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title("Comparison of Average Performance")
        
        rects1 = ax.bar(x - width/2, mae_avgs, width, label='Avg MAE', color='#ff9999', edgecolor='black')
        rects2 = ax.bar(x + width/2, rmse_avgs, width, label='Avg RMSE', color='#66b3ff', edgecolor='black')
        
        ax.set_ylabel('Average Error Value')
        ax.set_title(f"Perbandingan Rata-rata Error antar Metode\n(Query: '{query_ing['name']}')", pad=20, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(methods, fontweight='bold')
        ax.legend()
        
        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.annotate(f"{height:.5f}",
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        autolabel(rects1)
        autolabel(rects2)
        
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        fig.tight_layout()

    # Data untuk grafik perbandingan rata-rata
    avg_data = {
        'cos': (avg_mae_cos, avg_rmse_cos),
        'euc': (avg_mae_euc, avg_rmse_euc),
        'man': (avg_mae_man, avg_rmse_man)
    }

    plot_algorithm_performance(top_k_cosine, 'Cosine Similarity', 'cosine', 'Cosine Score', avg_mae_cos, avg_rmse_cos)
    plot_algorithm_performance(top_k_eucl, 'Euclidean Distance', 'euclidean', 'Euclidean Dist', avg_mae_euc, avg_rmse_euc)
    plot_algorithm_performance(top_k_man, 'Manhattan Distance', 'manhattan', 'Manhattan Dist', avg_mae_man, avg_rmse_man)
    plot_summary_comparison(avg_data)

    print("       (Silakan cek 4 jendela Matplotlib yang terbuka untuk melihat grafik)")
    print("       (Tutup SEMUA jendela grafik/plot untuk mengakhiri program)")
    plt.show()

if __name__ == "__main__":
    import sys
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh user.")
        sys.exit(0)
