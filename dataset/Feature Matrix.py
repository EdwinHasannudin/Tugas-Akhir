import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def create_comprehensive_feature_matrix(knowledge_base):
    """
    Membuat feature matrix komprehensif dari semua bahan dalam knowledge base
    """
    # Definisikan nama fitur
    feature_names = [
        'rasa_asin', 'rasa_manis', 'rasa_asam', 'rasa_pahit', 'rasa_gurih',
        'tekstur_padat', 'tekstur_cair', 'tekstur_lembut', 
        'fungsi_penyedap', 'fungsi_pengental'
    ]
    
    # Siapkan data untuk feature matrix
    ingredients_list = []
    features_data = []
    
    for ingredient, features in knowledge_base.items():
        ingredients_list.append(ingredient)
        features_data.append(features)
    
    # Buat DataFrame
    feature_matrix = pd.DataFrame(features_data, columns=feature_names)
    feature_matrix['ingredient'] = ingredients_list
    feature_matrix = feature_matrix.set_index('ingredient')
    
    return feature_matrix

# Buat knowledge base (sama seperti sebelumnya)
def create_ingredient_knowledge_base():
    """
    Membuat knowledge base karakteristik untuk setiap bahan
    Skala 0-5 untuk setiap fitur
    """
    ingredient_features = {
        # Format: 'bahan': [rasa_asin, rasa_manis, rasa_asam, rasa_pahit, rasa_gurih, 
        #                  tekstur_padat, tekstur_cair, tekstur_lembut, fungsi_penyedap, fungsi_pengental]
        
        # Bumbu Dasar
        'garam': [5, 0, 0, 0, 1, 1, 0, 0, 5, 0],
        'gula': [0, 5, 0, 0, 0, 1, 0, 0, 3, 0],
        'gula merah': [0, 4, 1, 0, 0, 1, 0, 0, 3, 0],
        'merica': [2, 0, 0, 1, 1, 1, 0, 0, 4, 0],
        
        # Bawang-bawangan
        'bawang putih': [1, 1, 0, 0, 3, 1, 0, 0, 4, 0],
        'bawang merah': [1, 1, 0, 0, 3, 1, 0, 0, 4, 0],
        'bawang bombay': [1, 2, 1, 0, 2, 1, 0, 1, 3, 0],
        
        # Bumbu Rempah
        'kunyit': [1, 0, 0, 2, 1, 1, 0, 0, 3, 1],
        'jahe': [1, 1, 2, 2, 1, 1, 0, 0, 3, 0],
        'lengkuas': [1, 0, 0, 2, 1, 1, 0, 0, 3, 0],
        'serai': [1, 0, 0, 2, 1, 1, 0, 0, 3, 0],
        'daun salam': [1, 0, 0, 2, 1, 1, 0, 0, 3, 0],
        'daun jeruk': [1, 0, 2, 2, 1, 1, 0, 0, 3, 0],
        'kemiri': [1, 1, 0, 1, 3, 1, 0, 0, 3, 2],
        'ketumbar': [1, 0, 0, 1, 2, 1, 0, 0, 3, 0],
        
        # Cabai
        'cabai': [1, 0, 0, 0, 1, 1, 0, 0, 4, 0],
        'cabai merah': [1, 0, 0, 0, 1, 1, 0, 0, 4, 0],
        'cabai rawit': [1, 0, 0, 0, 1, 1, 0, 0, 4, 0],
        'cabai hijau': [1, 0, 0, 0, 1, 1, 0, 0, 4, 0],
        
        # Protein Hewani
        'ayam': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'dada ayam': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'ayam fillet': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'sayap ayam': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'ceker ayam': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'telur': [1, 0, 0, 0, 3, 1, 0, 1, 0, 2],
        'udang': [2, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'ikan': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'sapi': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'kambing': [1, 0, 0, 0, 4, 1, 0, 1, 0, 0],
        'tahu': [1, 0, 0, 0, 2, 1, 0, 1, 0, 1],
        'tempe': [1, 0, 0, 0, 3, 1, 0, 1, 0, 0],

        # Santan & Susu
        'santan': [1, 1, 0, 0, 4, 0, 1, 1, 1, 4],
        'susu': [1, 2, 1, 0, 2, 0, 1, 1, 1, 2],
        'susu evaporasi': [1, 2, 1, 0, 2, 0, 1, 1, 1, 3],
        'yogurt': [1, 2, 3, 0, 2, 0, 1, 1, 1, 3],
        'keju': [3, 1, 1, 0, 4, 1, 0, 1, 2, 3],
        
        # Sayuran
        'wortel': [1, 2, 0, 0, 1, 1, 0, 1, 0, 0],
        'kentang': [1, 1, 0, 0, 1, 1, 0, 1, 0, 2],
        'kol': [1, 1, 0, 1, 1, 1, 0, 1, 0, 0],
        'sawi': [1, 1, 0, 1, 1, 1, 0, 1, 0, 0],
        'daun bawang': [1, 1, 0, 0, 2, 1, 0, 1, 2, 0],
        'seledri': [1, 1, 0, 1, 2, 1, 0, 1, 2, 0],
        'tomat': [1, 2, 3, 0, 1, 1, 0, 1, 1, 0],
        'timun': [1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        'brokoli': [1, 1, 0, 1, 1, 1, 0, 1, 0, 0],
        'buncis': [1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        'kacang panjang': [1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        'tauge': [1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        
        # Tepung
        'tepung terigu': [0, 0, 0, 0, 1, 1, 0, 0, 0, 4],
        'tepung maizena': [0, 0, 0, 0, 1, 1, 0, 0, 0, 5],
        'tepung tapioka': [0, 0, 0, 0, 1, 1, 0, 0, 0, 4],
        'tepung beras': [0, 0, 0, 0, 1, 1, 0, 0, 0, 4],
        'tepung sagu': [0, 0, 0, 0, 1, 1, 0, 0, 0, 4],
        
        # Minyak & Lemak
        'minyak': [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        'minyak goreng': [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        'minyak wijen': [1, 0, 0, 0, 4, 0, 1, 0, 3, 0],
        'mentega': [2, 0, 0, 0, 4, 0, 0, 1, 1, 1],
        'margarin': [2, 0, 0, 0, 4, 0, 0, 1, 1, 1],
        
        # Kecap & Saus
        'kecap manis': [3, 4, 0, 0, 3, 0, 1, 0, 4, 1],
        'kecap asin': [5, 1, 0, 0, 3, 0, 1, 0, 4, 0],
        'saus tiram': [4, 2, 0, 0, 4, 0, 1, 0, 4, 2],
        'saus tomat': [2, 3, 2, 0, 2, 0, 1, 0, 3, 1],
        'saus sambal': [2, 2, 1, 0, 2, 0, 1, 0, 3, 1],
        
        # Buah & Asam
        'jeruk nipis': [0, 1, 5, 1, 0, 0, 1, 0, 2, 0],
        'jeruk lemon': [0, 1, 5, 1, 0, 0, 1, 0, 2, 0],
        'asam jawa': [0, 1, 5, 2, 0, 0, 1, 0, 2, 1],
        'belimbing wuluh': [0, 1, 5, 1, 0, 1, 0, 0, 2, 0],
        
        # Lain-lain
        'air': [0, 0, 0, 0, 0, 0, 5, 0, 0, 0],
        'kaldu': [3, 1, 0, 0, 4, 0, 1, 0, 4, 1],
    }
    
    return ingredient_features

# Buat knowledge base dan feature matrix
print("Membuat knowledge base...")
knowledge_base = create_ingredient_knowledge_base()

print("Membuat feature matrix...")
feature_matrix = create_comprehensive_feature_matrix(knowledge_base)

print(f"Feature matrix berhasil dibuat!")
print(f"Dimensi: {feature_matrix.shape}")
print(f"Jumlah bahan: {len(feature_matrix)}")
print(f"Jumlah fitur: {len(feature_matrix.columns)}")

# Tampilkan feature matrix
print("\n=== FEATURE MATRIX ===")
print(feature_matrix.head(15))

# Statistik deskriptif
print("\n=== STATISTIK DESKRIPTIF ===")
print(feature_matrix.describe())

def visualize_feature_distribution(feature_matrix):
    """
    Visualisasi distribusi fitur dalam feature matrix
    """
    plt.figure(figsize=(15, 12))
    
    # Distribusi setiap fitur
    plt.subplot(2, 2, 1)
    feature_matrix.mean().sort_values(ascending=False).plot(kind='bar', color='skyblue')
    plt.title('Rata-rata Nilai Setiap Fitur')
    plt.xticks(rotation=45)
    plt.ylabel('Rata-rata Nilai')
    plt.grid(axis='y', alpha=0.3)
    
    # Heatmap korelasi fitur
    plt.subplot(2, 2, 2)
    correlation_matrix = feature_matrix.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, fmt='.2f')
    plt.title('Korelasi Antar Fitur')
    
    # Distribusi nilai fitur
    plt.subplot(2, 2, 3)
    feature_matrix.boxplot(figsize=(12, 6))
    plt.title('Distribusi Nilai Fitur')
    plt.xticks(rotation=45)
    plt.ylabel('Skala (0-5)')
    
    # Top 10 bahan dengan nilai gurih tertinggi
    plt.subplot(2, 2, 4)
    feature_matrix.nlargest(10, 'rasa_gurih')['rasa_gurih'].plot(kind='barh', color='lightgreen')
    plt.title('10 Bahan dengan Rasa Gurih Tertinggi')
    plt.xlabel('Skala Rasa Gurih')
    
    plt.tight_layout()
    plt.show()

# Visualisasi distribusi fitur
print("\nVisualisasi distribusi fitur...")
visualize_feature_distribution(feature_matrix)

def analyze_ingredient_similarity(feature_matrix):
    """
    Menganalisis similarity antara bahan-bahan menggunakan cosine similarity
    """
    print("Menghitung similarity matrix...")
    similarity_matrix = cosine_similarity(feature_matrix)
    similarity_df = pd.DataFrame(
        similarity_matrix, 
        index=feature_matrix.index, 
        columns=feature_matrix.index
    )
    
    return similarity_df

# Hitung similarity matrix
similarity_df = analyze_ingredient_similarity(feature_matrix)

print(f"Similarity matrix shape: {similarity_df.shape}")
print("\nContoh similarity matrix (10x10 pertama):")
print(similarity_df.iloc[:10, :10].round(3))

def find_most_similar_ingredients(similarity_df, top_n=10):
    """
    Mencari pasangan bahan yang paling mirip
    """
    similarities = []
    ingredients = similarity_df.index
    
    for i in range(len(ingredients)):
        for j in range(i+1, len(ingredients)):
            similarities.append({
                'bahan_1': ingredients[i],
                'bahan_2': ingredients[j],
                'similarity': similarity_df.iloc[i, j]
            })
    
    similarities_df = pd.DataFrame(similarities)
    return similarities_df.nlargest(top_n, 'similarity')

# Cari bahan yang paling mirip
print("\n=== 10 PASANGAN BAHAN PALING MIRIP ===")
most_similar = find_most_similar_ingredients(similarity_df)
print(most_similar)

def recommend_substitutes(target_ingredient, feature_matrix, similarity_df, top_n=5):
    """
    Merekomendasikan bahan pengganti berdasarkan similarity
    """
    if target_ingredient not in feature_matrix.index:
        return f"Bahan '{target_ingredient}' tidak ditemukan dalam database"
    
    # Dapatkan similarity scores untuk bahan target
    target_similarities = similarity_df[target_ingredient]
    
    # Buat dataframe hasil
    results = pd.DataFrame({
        'bahan': target_similarities.index,
        'similarity_score': target_similarities.values
    })
    
    # Urutkan dan ambil top_n (exclude diri sendiri)
    results = results[results['bahan'] != target_ingredient]
    results = results.sort_values('similarity_score', ascending=False).head(top_n)
    
    return results

# Test rekomendasi untuk beberapa bahan
print("\n=== TEST REKOMENDASI BAHAN PENGGANTI ===")
test_ingredients = ['santan', 'ayam', 'bawang putih', 'telur', 'keju']

for ingredient in test_ingredients:
    recommendations = recommend_substitutes(ingredient, feature_matrix, similarity_df)
    print(f"\nPengganti untuk '{ingredient}':")
    for idx, row in recommendations.iterrows():
        similarity_percent = row['similarity_score'] * 100
        print(f"  {row['bahan']} ({similarity_percent:.1f}% similar)")

def analyze_ingredient_clusters(feature_matrix, n_clusters=6):
    """
    Menganalisis kelompok bahan menggunakan clustering
    """
    print(f"\n=== CLUSTERING BAHAN ({n_clusters} KELOMPOK) ===")
    
    # Normalisasi features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(feature_matrix)
    
    # Clustering dengan KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(features_scaled)
    
    # PCA untuk visualisasi 2D
    pca = PCA(n_components=2)
    features_2d = pca.fit_transform(features_scaled)
    
    # Buat dataframe hasil clustering
    cluster_df = feature_matrix.copy()
    cluster_df['cluster'] = clusters
    cluster_df['pca_x'] = features_2d[:, 0]
    cluster_df['pca_y'] = features_2d[:, 1]
    
    # Visualisasi clustering
    plt.figure(figsize=(14, 10))
    
    colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))
    
    for cluster_id in range(n_clusters):
        cluster_data = cluster_df[cluster_df['cluster'] == cluster_id]
        plt.scatter(cluster_data['pca_x'], cluster_data['pca_y'], 
                   c=[colors[cluster_id]], label=f'Cluster {cluster_id}', 
                   s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Tambah label untuk beberapa bahan per cluster
        for idx, row in cluster_data.iterrows():
            if np.random.random() < 0.3:  # Label 30% bahan secara acak
                plt.annotate(idx, (row['pca_x'], row['pca_y']),
                           xytext=(5, 5), textcoords='offset points', 
                           fontsize=8, alpha=0.7)
    
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.title('Clustering Bahan Berdasarkan Karakteristik')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
    
    # Analisis cluster
    print("\nKarakteristik setiap cluster:")
    for cluster_id in range(n_clusters):
        cluster_ingredients = cluster_df[cluster_df['cluster'] == cluster_id].index.tolist()
        cluster_features = cluster_df[cluster_df['cluster'] == cluster_id].mean()
        
        print(f"\n--- Cluster {cluster_id} ({len(cluster_ingredients)} bahan) ---")
        print(f"Bahan: {', '.join(cluster_ingredients[:8])}{'...' if len(cluster_ingredients) > 8 else ''}")
        
        # Tampilkan fitur dominan
        top_features = cluster_features.nlargest(3)
        print(f"Fitur dominan: {', '.join([f'{feat}({val:.2f})' for feat, val in top_features.items()])}")
    
    return cluster_df

# Analisis clustering
cluster_results = analyze_ingredient_clusters(feature_matrix)

def save_feature_analysis(feature_matrix, similarity_df, cluster_results, knowledge_base):
    """
    Menyimpan hasil analisis feature matrix
    """
    with pd.ExcelWriter('ingredient_feature_analysis.xlsx') as writer:
        # 1. Feature matrix lengkap
        feature_matrix.reset_index().to_excel(writer, sheet_name='Feature_Matrix', index=False)
        
        # 2. Similarity matrix (sample)
        similarity_sample = similarity_df.iloc[:15, :15].reset_index()
        similarity_sample.to_excel(writer, sheet_name='Similarity_Sample', index=False)
        
        # 3. Cluster results
        cluster_results.reset_index().to_excel(writer, sheet_name='Clustering_Results', index=False)
        
        # 4. Knowledge base
        kb_df = pd.DataFrame([
            {'ingredient': ing, **dict(zip(feature_matrix.columns, features))}
            for ing, features in knowledge_base.items()
        ])
        kb_df.to_excel(writer, sheet_name='Knowledge_Base', index=False)
        
        # 5. Statistik
        stats_df = feature_matrix.describe()
        stats_df.to_excel(writer, sheet_name='Statistics')
    
    print("\nHasil analisis disimpan sebagai 'ingredient_feature_analysis.xlsx'")

# Simpan hasil analisis
save_feature_analysis(feature_matrix, similarity_df, cluster_results, knowledge_base)

# Ringkasan akhir
print("\n" + "="*50)
print("RINGKASAN FEATURE MATRIX")
print("="*50)
print(f"Total bahan: {len(feature_matrix)}")
print(f"Total fitur: {len(feature_matrix.columns)}")
print(f"\nFitur yang dianalisis: {list(feature_matrix.columns)}")
print(f"\nContoh bahan dalam database:")
print(f"- Bumbu: {', '.join([b for b in feature_matrix.index if b in ['garam', 'merica', 'bawang putih']])}")
print(f"- Protein: {', '.join([b for b in feature_matrix.index if b in ['ayam', 'telur', 'ikan']])}")
print(f"- Sayuran: {', '.join([b for b in feature_matrix.index if b in ['wortel', 'kentang', 'tomat']])}")
print(f"- Cairan: {', '.join([b for b in feature_matrix.index if b in ['santan', 'susu', 'air']])}")

print("\nFeature matrix siap digunakan untuk:")
print("✓ Rekomendasi bahan pengganti")
print("✓ Analisis similarity antar bahan")
print("✓ Clustering bahan berdasarkan karakteristik")
print("✓ Optimasi resep berdasarkan profil rasa")