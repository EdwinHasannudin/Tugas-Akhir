import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity

# Set page config
st.set_page_config(
    page_title="Sistem Rekomendasi Bahan Makanan",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

class IngredientRecommender:
    def __init__(self, excel_file_path):
        """
        Inisialisasi recommender dengan data dari file Excel
        """
        try:
            # Load data dari berbagai sheet
            self.feature_matrix = pd.read_excel(excel_file_path, sheet_name='Feature_Matrix')
            self.similarity_sample = pd.read_excel(excel_file_path, sheet_name='Similarity_Sample')
            self.clustering_results = pd.read_excel(excel_file_path, sheet_name='Clustering_Results')
            self.knowledge_base = pd.read_excel(excel_file_path, sheet_name='Knowledge_Base')
            self.statistics = pd.read_excel(excel_file_path, sheet_name='Statistics')
            
            # Set index untuk memudahkan pencarian
            self.feature_matrix.set_index('ingredient', inplace=True)
            self.similarity_sample.set_index('ingredient', inplace=True)
            self.clustering_results.set_index('ingredient', inplace=True)
            self.knowledge_base.set_index('ingredient', inplace=True)
            
            # Daftar semua bahan yang tersedia
            self.all_ingredients = list(self.feature_matrix.index)
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    def calculate_cosine_similarity(self, vec1, vec2):
        """Menghitung cosine similarity antara dua vektor"""
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0
        return dot_product / (norm_vec1 * norm_vec2)
    
    def get_ingredient_features(self, ingredient_name):
        """Mendapatkan fitur-fitur dari sebuah bahan"""
        if ingredient_name in self.feature_matrix.index:
            return self.feature_matrix.loc[ingredient_name].values
        else:
            return None
    
    def find_similar_ingredients(self, target_ingredient, top_n=5):
        """Mencari bahan-bahan yang mirip dengan bahan target"""
        if target_ingredient not in self.all_ingredients:
            return f"Bahan '{target_ingredient}' tidak ditemukan dalam database."
        
        similarities = []
        target_features = self.get_ingredient_features(target_ingredient)
        
        for ingredient in self.all_ingredients:
            if ingredient != target_ingredient:
                other_features = self.get_ingredient_features(ingredient)
                similarity = self.calculate_cosine_similarity(target_features, other_features)
                similarities.append((ingredient, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]
    
    def get_precomputed_similarities(self, target_ingredient, top_n=5):
        """Menggunakan similarity yang sudah dihitung sebelumnya"""
        if target_ingredient not in self.similarity_sample.index:
            return f"Bahan '{target_ingredient}' tidak ditemukan dalam similarity sample."
        
        target_similarities = self.similarity_sample.loc[target_ingredient]
        similarities = []
        
        for ingredient in self.similarity_sample.columns:
            if ingredient != target_ingredient:
                similarity = target_similarities[ingredient]
                similarities.append((ingredient, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]

def main():
    # Header
    st.title("🍳 Sistem Rekomendasi Bahan Makanan")
    st.markdown("""
    Temukan bahan makanan yang mirip berdasarkan karakteristik rasa, tekstur, dan fungsi!
    """)
    
    # Inisialisasi recommender
    if 'recommender' not in st.session_state:
        with st.spinner('Memuat data bahan makanan...'):
            st.session_state.recommender = IngredientRecommender('ingredient_feature_analysis.xlsx')
    
    recommender = st.session_state.recommender
    
    # Sidebar
    st.sidebar.title("Navigasi")
    app_mode = st.sidebar.selectbox(
        "Pilih Mode",
        ["Rekomendasi Bahan", "Informasi Bahan", "Eksplorasi Data", "Tentang"]
    )
    
    if app_mode == "Rekomendasi Bahan":
        show_recommendation_page(recommender)
    elif app_mode == "Informasi Bahan":
        show_ingredient_info_page(recommender)
    elif app_mode == "Eksplorasi Data":
        show_data_exploration_page(recommender)
    elif app_mode == "Tentang":
        show_about_page()

def show_recommendation_page(recommender):
    st.header("🔍 Rekomendasi Bahan Mirip")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input bahan target
        target_ingredient = st.selectbox(
            "Pilih bahan yang ingin dicari kemiripannya:",
            options=recommender.all_ingredients,
            index=recommender.all_ingredients.index("bawang putih") if "bawang putih" in recommender.all_ingredients else 0
        )
    
    with col2:
        # Jumlah rekomendasi
        top_n = st.slider("Jumlah rekomendasi:", min_value=3, max_value=15, value=5)
    
    # Metode similarity
    use_precomputed = st.checkbox("Gunakan similarity yang sudah dihitung (lebih cepat)", value=True)
    
    if st.button("Cari Rekomendasi", type="primary"):
        with st.spinner('Mencari bahan yang mirip...'):
            if use_precomputed and target_ingredient in recommender.similarity_sample.index:
                recommendations = recommender.get_precomputed_similarities(target_ingredient, top_n)
                method = "Precomputed Similarity"
            else:
                recommendations = recommender.find_similar_ingredients(target_ingredient, top_n)
                method = "Calculated Cosine Similarity"
            
            if isinstance(recommendations, str):
                st.error(recommendations)
            else:
                # Display results
                st.success(f"✅ Menemukan {len(recommendations)} rekomendasi untuk **{target_ingredient}**")
                
                # Create results dataframe
                results_df = pd.DataFrame(recommendations, columns=['Bahan', 'Skor Kemiripan'])
                results_df['No'] = range(1, len(results_df) + 1)
                results_df['Keterangan'] = results_df['Skor Kemiripan'].apply(
                    lambda x: "Sangat Mirip" if x >= 0.9 else 
                             "Mirip" if x >= 0.7 else 
                             "Cukup Mirip" if x >= 0.5 else "Agak Mirip"
                )
                
                # Display table
                st.subheader("📊 Hasil Rekomendasi")
                display_df = results_df[['No', 'Bahan', 'Skor Kemiripan', 'Keterangan']].set_index('No')
                st.dataframe(display_df, use_container_width=True)
                
                # Visualisasi
                st.subheader("📈 Visualisasi Kemiripan")
                
                fig = px.bar(
                    results_df,
                    x='Skor Kemiripan',
                    y='Bahan',
                    orientation='h',
                    title=f'Skor Kemiripan dengan {target_ingredient}',
                    color='Skor Kemiripan',
                    color_continuous_scale='viridis'
                )
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
                
                # Comparison radar chart untuk top 3
                if len(recommendations) >= 3:
                    st.subheader("🔄 Perbandingan Profil (Top 3)")
                    show_comparison_radar(recommender, target_ingredient, recommendations[:3])

def show_comparison_radar(recommender, target, top_recommendations):
    """Menampilkan radar chart untuk perbandingan"""
    ingredients_to_compare = [target] + [ing[0] for ing in top_recommendations]
    
    # Prepare data for radar chart
    categories = ['rasa_asin', 'rasa_manis', 'rasa_asam', 'rasa_pahit', 'rasa_gurih']
    
    fig = go.Figure()
    
    for ingredient in ingredients_to_compare:
        features = recommender.feature_matrix.loc[ingredient]
        values = [features[cat] for cat in categories]
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the circle
            theta=categories + [categories[0]],
            fill='toself',
            name=ingredient
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True,
        title="Perbandingan Profil Rasa"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_ingredient_info_page(recommender):
    st.header("📋 Informasi Detail Bahan")
    
    ingredient = st.selectbox(
        "Pilih bahan untuk melihat informasi detail:",
        options=recommender.all_ingredients,
        index=recommender.all_ingredients.index("bawang putih") if "bawang putih" in recommender.all_ingredients else 0
    )
    
    if ingredient:
        features = recommender.feature_matrix.loc[ingredient]
        cluster = recommender.clustering_results.loc[ingredient, 'cluster']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Profil Rasa")
            taste_data = {
                'Rasa': ['Asin', 'Manis', 'Asam', 'Pahit', 'Gurih'],
                'Skor': [
                    features['rasa_asin'],
                    features['rasa_manis'],
                    features['rasa_asam'],
                    features['rasa_pahit'],
                    features['rasa_gurih']
                ]
            }
            taste_df = pd.DataFrame(taste_data)
            
            fig_taste = px.bar(taste_df, x='Rasa', y='Skor', title='Profil Rasa', color='Skor')
            st.plotly_chart(fig_taste, use_container_width=True)
        
        with col2:
            st.subheader("🔧 Fungsi dan Tekstur")
            
            # Fungsi
            st.metric("Fungsi Penyedap", f"{features['fungsi_penyedap']}/5")
            st.metric("Fungsi Pengental", f"{features['fungsi_pengental']}/5")
            
            # Tekstur
            texture_data = {
                'Tekstur': ['Padat', 'Cair', 'Lembut'],
                'Nilai': [
                    features['tekstur_padat'],
                    features['tekstur_cair'],
                    features['tekstur_lembut']
                ]
            }
            texture_df = pd.DataFrame(texture_data)
            fig_texture = px.pie(texture_df, values='Nilai', names='Tekstur', title='Profil Tekstur')
            st.plotly_chart(fig_texture, use_container_width=True)
        
        st.subheader("📈 Informasi Cluster")
        st.info(f"Bahan ini termasuk dalam **Cluster {cluster}**")
        
        # Tampilkan bahan lain dalam cluster yang sama
        cluster_members = recommender.clustering_results[recommender.clustering_results['cluster'] == cluster].index.tolist()
        cluster_members.remove(ingredient)  # Remove current ingredient
        
        if cluster_members:
            st.write(f"Bahan lain dalam cluster {cluster}:")
            cols = st.columns(3)
            for i, member in enumerate(cluster_members[:6]):  # Show max 6 members
                with cols[i % 3]:
                    st.write(f"• {member}")

def show_data_exploration_page(recommender):
    st.header("📊 Eksplorasi Data Bahan")
    
    tab1, tab2, tab3 = st.tabs(["Statistik Dataset", "Distribusi Cluster", "Heatmap Similarity"])
    
    with tab1:
        st.subheader("📈 Statistik Dataset")
        st.dataframe(recommender.statistics, use_container_width=True)
        
        # Visualisasi distribusi fitur
        st.subheader("Distribusi Fitur Rasa")
        taste_features = ['rasa_asin', 'rasa_manis', 'rasa_asam', 'rasa_pahit', 'rasa_gurih']
        
        fig_dist = px.box(recommender.feature_matrix[taste_features], title="Distribusi Skor Rasa")
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with tab2:
        st.subheader("👥 Distribusi Cluster")
        cluster_counts = recommender.clustering_results['cluster'].value_counts().sort_index()
        
        fig_cluster = px.pie(
            values=cluster_counts.values,
            names=[f'Cluster {i}' for i in cluster_counts.index],
            title="Distribusi Bahan per Cluster"
        )
        st.plotly_chart(fig_cluster, use_container_width=True)
        
        # Tampilkan contoh bahan per cluster
        st.subheader("Contoh Bahan per Cluster")
        for cluster_num in sorted(recommender.clustering_results['cluster'].unique()):
            with st.expander(f"Cluster {cluster_num} ({cluster_counts[cluster_num]} bahan)"):
                cluster_ingredients = recommender.clustering_results[recommender.clustering_results['cluster'] == cluster_num].index.tolist()
                cols = st.columns(3)
                for i, ingredient in enumerate(cluster_ingredients[:9]):  # Show max 9 per cluster
                    with cols[i % 3]:
                        st.write(f"• {ingredient}")
    
    with tab3:
        st.subheader("🔥 Heatmap Kemiripan")
        st.info("Pilih beberapa bahan untuk melihat heatmap kemiripan antar bahan")
        
        selected_ingredients = st.multiselect(
            "Pilih bahan:",
            options=recommender.all_ingredients,
            default=recommender.all_ingredients[:6] if len(recommender.all_ingredients) >= 6 else recommender.all_ingredients
        )
        
        if len(selected_ingredients) >= 2:
            # Create similarity matrix for selected ingredients
            similarity_matrix = []
            for ing1 in selected_ingredients:
                row = []
                for ing2 in selected_ingredients:
                    if ing1 == ing2:
                        row.append(1.0)
                    else:
                        vec1 = recommender.get_ingredient_features(ing1)
                        vec2 = recommender.get_ingredient_features(ing2)
                        similarity = recommender.calculate_cosine_similarity(vec1, vec2)
                        row.append(similarity)
                similarity_matrix.append(row)
            
            # Create heatmap
            fig_heatmap = px.imshow(
                similarity_matrix,
                x=selected_ingredients,
                y=selected_ingredients,
                title="Heatmap Kemiripan Antar Bahan",
                color_continuous_scale="viridis",
                aspect="auto"
            )
            fig_heatmap.update_layout(xaxis_title="Bahan", yaxis_title="Bahan")
            st.plotly_chart(fig_heatmap, use_container_width=True)

def show_about_page():
    st.header("ℹ️ Tentang Aplikasi")
    
    st.markdown("""
    ## Sistem Rekomendasi Bahan Makanan
    
    Aplikasi ini menggunakan **Machine Learning** untuk merekomendasikan bahan makanan 
    yang mirip berdasarkan karakteristik:
    
    - **Rasa**: Asin, Manis, Asam, Pahit, Gurih
    - **Tekstur**: Padat, Cair, Lembut
    - **Fungsi**: Penyedap, Pengental
    
    ### 🎯 Kegunaan:
    1. **Mencari pengganti bahan** yang tidak tersedia
    2. **Eksperimen resep** dengan bahan yang mirip
    3. **Memahami hubungan** antar bahan makanan
    4. **Eksplorasi bahan baru** dalam memasak
    
    ### 🔧 Teknologi:
    - **Cosine Similarity** untuk menghitung kemiripan
    - **Clustering** untuk pengelompokan bahan
    - **PCA** untuk visualisasi dimensi tinggi
    
    ### 📊 Data:
    Sistem ini menggunakan dataset dengan **69 bahan makanan** yang telah dianalisis 
    berdasarkan 10 karakteristik berbeda.
    """)
    
    st.success("🍳 Selamat bereksperimen dengan bahan makanan!")

if __name__ == "__main__":
    main()