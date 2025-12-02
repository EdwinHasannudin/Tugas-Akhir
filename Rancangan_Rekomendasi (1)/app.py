import random
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics.pairwise import cosine_similarity
import requests
from PIL import Image
import io
import base64
import re

# Set page config
st.set_page_config(
    page_title="Sistem Rekomendasi Bahan Makanan",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

class IngredientRecommender:
    def __init__(self, excel_file_path, dataset_path='resep_database_terorganisir.xlsx'):
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
            
            # Inisialisasi database resep
            self.dataset_path = dataset_path
            self.recipes_database = self._initialize_recipes_database()
            
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    def _initialize_recipes_database(self):
        """Inisialisasi database resep dari dataset Excel"""
        try:
            # Load data resep dari sheet yang sesuai
            recipes_data = pd.read_excel('resep_database_terorganisir.xlsx', sheet_name='Semua_Resep')

            recipes_dict = {}

            for _, row in recipes_data.iterrows():
                kategori = row['Kategori']
                title = row['Nama Resep']
                ingredients_text = row['Bahan']

                # Parse bahan-bahan dari teks
                ingredients_list = self._parse_ingredients(ingredients_text)

                # Tentukan kesulitan berdasarkan jumlah bahan
                difficulty = self._determine_difficulty(ingredients_list)

                # Gunakan kategori sebagai main_ingredient
                main_ingredient = kategori.lower() if pd.notna(kategori) else 'umum'

                # Tambahkan ke dictionary
                if main_ingredient not in recipes_dict:
                    recipes_dict[main_ingredient] = []

                recipes_dict[main_ingredient].append({
                    'nama': title,
                    'bahan': ingredients_list,
                    'kesulitan': difficulty,
                })

            return recipes_dict

        except Exception as e:
            st.error(f"Error loading recipes from Excel: {e}")
            # Fallback ke data statis jika error
            return self._get_fallback_recipes()
    
    def _get_fallback_recipes(self):
        """Fallback recipes jika gagal load dari Excel"""
        return {
            'ayam': [
                {'nama': 'Ayam Goreng', 'bahan': ['ayam', 'bawang putih', 'garam'], 'kesulitan': 'Mudah'},
                {'nama': 'Ayam Bakar', 'bahan': ['ayam', 'kecap', 'bawang merah'], 'kesulitan': 'Sedang'},
            ],
            'ikan': [
                {'nama': 'Ikan Bakar', 'bahan': ['ikan', 'bawang putih', 'jeruk nipis'], 'kesulitan': 'Mudah'},
                {'nama': 'Ikan Goreng', 'bahan': ['ikan', 'tepung', 'minyak'], 'kesulitan': 'Mudah'},
            ],
            'sapi': [
                {'nama': 'Semur Daging', 'bahan': ['daging sapi', 'kentang', 'kecap'], 'kesulitan': 'Sedang'},
            ],
            'telur': [
                {'nama': 'Telur Dadar', 'bahan': ['telur', 'bawang merah', 'garam'], 'kesulitan': 'Mudah'},
            ]
        }
    
    def _parse_ingredients(self, ingredients_text):
        """Parse teks ingredients menjadi list yang terstruktur"""
        if pd.isna(ingredients_text):
            return []
        
        # Split berdasarkan ' | ' yang digunakan dalam file terorganisir
        ingredients_list = []
        if ' | ' in str(ingredients_text):
            lines = str(ingredients_text).split(' | ')
        else:
            # Fallback ke split biasa
            lines = str(ingredients_text).split(',')
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 2:  # Filter out empty or very short lines
                ingredients_list.append(line.lower())
        
        return list(set(ingredients_list))  # Remove duplicates
    
    def _determine_difficulty(self, ingredients_list):
        """Tentukan tingkat kesulitan berdasarkan jumlah bahan"""
        ingredients_count = len(ingredients_list)
        
        if ingredients_count <= 5:
            return "Mudah"
        elif ingredients_count <= 8:
            return "Sedang"
        else:
            return "Sulit"
        
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
    
    def detect_ingredient_from_text(self, text_input):
        """Mendeteksi bahan makanan dari input teks - DIPERBAIKI"""
        text_lower = text_input.lower()
        detected_ingredients = []
        
        # Mapping yang lebih komprehensif untuk kategori utama
        ingredient_keywords = {
            'ayam': ['ayam', 'chicken', 'daging ayam', 'filet ayam', 'paha ayam', 'dada ayam'],
            'ikan': ['ikan', 'fish', 'salmon', 'tuna', 'gurame', 'lele', 'bandeng', 'mujair', 'kakap', 'tongkol'],
            'kambing': ['kambing', 'daging kambing', 'goat', 'gigiting', 'kambing muda'],
            'sapi': ['sapi', 'daging sapi', 'beef', 'daging', 'sapi muda', 'dagingsapi'],
            'udang': ['udang', 'shrimp', 'prawn', 'udang besar', 'udang kecil', 'udang windu', 'udang galah'],
            'cumi': ['cumi', 'squid', 'cumi-cumi', 'cumicumi'],
            'telur': ['telur', 'egg', 'telor', 'telur ayam', 'telur bebek', 'telur puyuh'],
            'tahu': ['tahu', 'tofu', 'tahu putih', 'tahu kuning'],
            'tempe': ['tempe', 'tempeh', 'tempe kedelai'],
            'wortel': ['wortel', 'carrot'],
            'kentang': ['kentang', 'potato', 'kentang merah', 'kentang putih'],
            'bawang merah': ['bawang merah', 'red onion', 'bamer', 'bawangmerah'],
            'bawang putih': ['bawang putih', 'garlic', 'baput', 'bawangputih'],
            'bawang bombay': ['bawang bombay', 'onion', 'bombay'],
            'cabai': ['cabai', 'cabe', 'chili', 'lombok', 'cabai merah', 'cabai hijau', 'cabai rawit'],
            'tomat': ['tomat', 'tomato'],
            'sawi': ['sawi', 'caisim', 'pakcoy', 'sawi hijau', 'sawi putih'],
            'bayam': ['bayam', 'spinach'],
            'jagung': ['jagung', 'corn', 'jagung manis'],
            'brokoli': ['brokoli', 'broccoli'],
            'jamur': ['jamur', 'mushroom', 'jamur tiram', 'jamur merang'],
        }
        
        # Debug: Tampilkan bahan yang tersedia di database
        available_main_ingredients = [ing for ing in ingredient_keywords.keys() if ing in self.all_ingredients]

        # Cari kata kunci dalam teks input
        for ingredient, keywords in ingredient_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Cek apakah bahan ada dalam database
                    if ingredient in self.all_ingredients:
                        if ingredient not in detected_ingredients:
                            detected_ingredients.append(ingredient)
                    break
        
        # Jika tidak ada yang terdeteksi, coba cari kata individual
        if not detected_ingredients:
            words = text_lower.split()
            for word in words:
                for ingredient in self.all_ingredients:
                    if word == ingredient and ingredient not in detected_ingredients:
                        detected_ingredients.append(ingredient)
                        break
        
        return detected_ingredients
    
    def get_recipes_by_ingredient(self, ingredient_name, max_recipes=3):
        """Mendapatkan resep berdasarkan bahan - DIPERBAIKI"""
        recipes = []

        # Debug info
        available_categories = list(self.recipes_database.keys())
        
        # Cari resep berdasarkan kategori yang sesuai dengan bahan
        if ingredient_name in self.recipes_database:
            category_recipes = self.recipes_database[ingredient_name]
            # Acak urutan resep untuk variasi
            random.shuffle(category_recipes)
            recipes.extend(category_recipes[:max_recipes])
        
        # Jika tidak ditemukan di kategori utama, cari di semua resep yang mengandung bahan tersebut
        if not recipes:
            for category, recipe_list in self.recipes_database.items():
                for recipe in recipe_list:
                    # Cek apakah bahan ada dalam resep
                    if any(ingredient_name in bahan.lower() for bahan in recipe['bahan']):
                        recipes.append(recipe)
                        if len(recipes) >= max_recipes:
                            break
                if len(recipes) >= max_recipes:
                    break
        
        return recipes[:max_recipes]
    
    def get_substitute_recommendations(self, target_ingredient, top_n=5):
        """Mendapatkan rekomendasi bahan pengganti"""
        if target_ingredient not in self.all_ingredients:
            return []
        
        # Cari bahan yang mirip
        similar_ingredients = self.find_similar_ingredients(target_ingredient, top_n)
        
        recommendations = []
        for ingredient, similarity in similar_ingredients:
            # Berikan penjelasan mengapa bahan ini mirip
            target_features = self.feature_matrix.loc[target_ingredient]
            ingredient_features = self.feature_matrix.loc[ingredient]
            
            # Cari karakteristik yang paling mirip
            feature_columns = ['rasa_asin', 'rasa_manis', 'rasa_asam', 'rasa_pahit', 'rasa_gurih']
            similarities = []
            
            for feature in feature_columns:
                sim = 1 - abs(target_features[feature] - ingredient_features[feature]) / 5
                similarities.append((feature, sim))
            
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_similar_features = [feat for feat, _ in similarities[:2]]
            
            explanation = f"Mirip dalam: {', '.join(top_similar_features).replace('rasa_', '')}"
            
            recommendations.append({
                'bahan': ingredient,
                'skor_kemiripan': similarity,
                'penjelasan': explanation
            })
        
        return recommendations

class ImageIngredientDetector:
    """Class untuk deteksi bahan makanan dari gambar"""
    
    def __init__(self):
        self.ingredient_mapping = {
            'ayam': ['ayam', 'chicken', 'daging ayam'],
            'ikan': ['ikan', 'fish', 'salmon', 'tuna'],
            'kambing': ['kambing', 'daging kambing', 'goat'],
            'sapi': ['sapi', 'daging sapi', 'beef'],
            'udang': ['udang', 'shrimp', 'prawn'],
            'cumi': ['cumi', 'squid'],
            'telur': ['telur', 'egg'],
            'tahu': ['tahu', 'tofu'],
            'tempe': ['tempe', 'tempeh'],
            'wortel': ['wortel', 'carrot'],
            'kentang': ['kentang', 'potato'],
            'bawang': ['bawang merah', 'bawang putih', 'bawang bombay'],
            'cabai': ['cabai', 'chili'],
            'tomat': ['tomat', 'tomato'],
        }
    
    def detect_from_image(self, image_file):
        """
        Simulasi deteksi bahan dari gambar
        """
        st.info("🔍 Menganalisis gambar...")
        
        # Simulasi processing time
        import time
        time.sleep(2)
        
        # Untuk demo, kita return beberapa bahan umum
        common_ingredients = ['ayam', 'ikan', 'kambing', 'sapi', 'udang', 'cumi', 'telur', 
                             'tahu', 'tempe', 'wortel', 'kentang', 'bawang', 'cabai', 'tomat']
        
        # Return 2-3 bahan acak untuk demo
        np.random.seed(hash(image_file.name) % 10000)
        detected = np.random.choice(common_ingredients, size=min(3, len(common_ingredients)), replace=False)
        
        return list(detected)

def main():
    # Header
    st.title("🍳 Sistem Rekomendasi Bahan Makanan")
    st.markdown("""
    Temukan bahan makanan yang mirip berdasarkan karakteristik rasa, tekstur, dan fungsi!
    Upload gambar atau ketik bahan yang Anda miliki untuk mendapatkan rekomendasi.
    """)
    
    # Inisialisasi recommender
    if 'recommender' not in st.session_state:
        with st.spinner('Memuat data bahan makanan...'):
            try:
                st.session_state.recommender = IngredientRecommender('ingredient_feature_analysis.xlsx', 'resep_database_terorganisir.xlsx')
                st.session_state.image_detector = ImageIngredientDetector()
                st.success("✅ Data berhasil dimuat!")
            except Exception as e:
                st.error(f"❌ Gagal memuat data: {e}")
                return
    
    recommender = st.session_state.recommender
    image_detector = st.session_state.image_detector
    
    # Sidebar
    st.sidebar.title("Navigasi")
    app_mode = st.sidebar.selectbox(
        "Pilih Mode",
        ["Input Bahan", "Rekomendasi Bahan", "Informasi Bahan", "Eksplorasi Data", "Tentang"]
    )
    
    if app_mode == "Input Bahan":
        show_input_page(recommender, image_detector)
    elif app_mode == "Rekomendasi Bahan":
        show_recommendation_page(recommender)
    elif app_mode == "Informasi Bahan":
        show_ingredient_info_page(recommender)
    elif app_mode == "Eksplorasi Data":
        show_data_exploration_page(recommender)
    elif app_mode == "Tentang":
        show_about_page()

def show_input_page(recommender, image_detector):
    st.header("📥 Input Bahan Makanan")
    
    tab1, tab2 = st.tabs(["📝 Input Teks", "🖼️ Upload Gambar"])
    
    with tab1:
        st.subheader("Masukkan Bahan yang Anda Miliki")
        
        # Quick buttons untuk bahan populer
        st.write("**Bahan Populer:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🐔 Ayam", use_container_width=True):
                st.session_state.quick_input = "ayam"
        with col2:
            if st.button("🐟 Ikan", use_container_width=True):
                st.session_state.quick_input = "ikan"
        with col3:
            if st.button("🐄 Sapi", use_container_width=True):
                st.session_state.quick_input = "sapi"
        with col4:
            if st.button("🥚 Telur", use_container_width=True):
                st.session_state.quick_input = "telur"
        
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            if st.button("🦐 Udang", use_container_width=True):
                st.session_state.quick_input = "udang"
        with col6:
            if st.button("🐐 Kambing", use_container_width=True):
                st.session_state.quick_input = "kambing"
        with col7:
            if st.button("🧈 Tahu", use_container_width=True):
                st.session_state.quick_input = "tahu"
        with col8:
            if st.button("🍘 Tempe", use_container_width=True):
                st.session_state.quick_input = "tempe"
        
        text_input = st.text_area(
            "Atau ketik bahan makanan yang Anda miliki (pisahkan dengan koma):",
            placeholder="Contoh: ayam, wortel, bawang putih, garam...",
            height=100,
            value=st.session_state.get('quick_input', '')
        )
        
        if st.button("🔍 Analisis Bahan", key="text_analyze", type="primary"):
            if text_input:
                with st.spinner('Mendeteksi bahan dari teks...'):
                    detected_ingredients = recommender.detect_ingredient_from_text(text_input)
                    
                    if detected_ingredients:
                        st.success(f"✅ Berhasil mendeteksi {len(detected_ingredients)} bahan:")
                        
                        # Tampilkan bahan yang terdeteksi
                        cols = st.columns(3)
                        for i, ingredient in enumerate(detected_ingredients):
                            with cols[i % 3]:
                                st.info(f"🍳 **{ingredient}**")
                        
                        # Tampilkan rekomendasi untuk setiap bahan yang terdeteksi
                        for ingredient in detected_ingredients:
                            show_ingredient_recommendations(recommender, ingredient)
                        
                        # Tampilkan resep yang mungkin
                        show_recipe_suggestions(recommender, detected_ingredients)
                    else:
                        st.warning("❌ Tidak dapat mendeteksi bahan makanan dari teks yang dimasukkan.")
                        st.info("""
                        **Tips:** Gunakan nama bahan yang umum seperti:
                        - 🐔 ayam, 🐟 ikan, 🐄 sapi, 🐐 kambing
                        - 🥚 telur, 🦐 udang, 🦑 cumi
                        - 🧈 tahu, 🍘 tempe
                        - 🥕 wortel, 🥔 kentang, 🧄 bawang
                        """)
            else:
                st.warning("Silakan masukkan teks terlebih dahulu.")
    
    with tab2:
        st.subheader("Upload Gambar Bahan Makanan")
        
        uploaded_file = st.file_uploader(
            "Pilih gambar bahan makanan:",
            type=['jpg', 'jpeg', 'png'],
            help="Upload gambar bahan makanan yang ingin Anda analisis"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Gambar yang diupload", use_column_width=True)
            
            if st.button("🔍 Analisis Gambar", key="image_analyze", type="primary"):
                with st.spinner('Menganalisis gambar...'):
                    detected_ingredients = image_detector.detect_from_image(uploaded_file)
                    
                    if detected_ingredients:
                        st.success(f"✅ Berhasil mendeteksi {len(detected_ingredients)} bahan dari gambar:")
                        
                        cols = st.columns(3)
                        for i, ingredient in enumerate(detected_ingredients):
                            with cols[i % 3]:
                                st.info(f"🍳 **{ingredient}**")
                        
                        # Tampilkan rekomendasi untuk setiap bahan yang terdeteksi
                        for ingredient in detected_ingredients:
                            show_ingredient_recommendations(recommender, ingredient)
                        
                        # Tampilkan resep yang mungkin
                        show_recipe_suggestions(recommender, detected_ingredients)
                    else:
                        st.warning("❌ Tidak dapat mendeteksi bahan makanan dari gambar.")
                        st.info("Pastikan gambar jelas dan mengandung bahan makanan yang dapat dikenali.")

def show_ingredient_recommendations(recommender, ingredient):
    """Menampilkan rekomendasi untuk satu bahan"""
    st.subheader(f"🔍 Rekomendasi untuk {ingredient}")
    
    # Rekomendasi bahan pengganti
    substitutes = recommender.get_substitute_recommendations(ingredient, 3)
    
    if substitutes:
        st.write("**Bahan Pengganti:**")
        for sub in substitutes:
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• **{sub['bahan']}** - {sub['penjelasan']}")
                with col2:
                    st.metric("Kemiripan", f"{sub['skor_kemiripan']:.2f}")
                st.markdown("---")
    else:
        st.info(f"Tidak ada rekomendasi pengganti untuk {ingredient}")

def show_recipe_suggestions(recommender, ingredients):
    """Menampilkan saran resep berdasarkan bahan"""
    st.subheader("🍽️ Resep yang Dapat Dicoba")
    
    all_recipes = []
    for ingredient in ingredients:
        recipes = recommender.get_recipes_by_ingredient(ingredient, 2)
        all_recipes.extend(recipes)
    
    # Remove duplicates
    unique_recipes = []
    seen_names = set()
    for recipe in all_recipes:
        if recipe['nama'] not in seen_names:
            unique_recipes.append(recipe)
            seen_names.add(recipe['nama'])
    
    if unique_recipes:
        st.success(f"🎉 Ditemukan {len(unique_recipes)} resep yang cocok!")
        
        for i, recipe in enumerate(unique_recipes[:4]):  # Show max 4 recipes
            with st.expander(f"📖 {recipe['nama']} ({recipe['kesulitan']})", expanded=i==0):
                st.write("**Bahan-bahan:**")
                for bahan in recipe['bahan']:
                    st.write(f"• {bahan}")
                
                # Highlight bahan yang tersedia
                available_ingredients = [ing for ing in recipe['bahan'] if any(avail in ing for avail in ingredients)]
                if available_ingredients:
                    st.success(f"✅ Anda memiliki {len(available_ingredients)} bahan dari resep ini")
                
                st.write(f"**Tingkat Kesulitan:** {recipe['kesulitan']}")
    else:
        st.info("💡 Coba kombinasikan bahan-bahan Anda dengan bahan lain untuk lebih banyak pilihan resep")



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
    
    ### 🎯 Fitur Baru:
    1. **Input Teks**: Ketik bahan yang Anda miliki untuk mendapatkan rekomendasi
    2. **Upload Gambar**: Upload gambar bahan untuk deteksi otomatis
    3. **Rekomendasi Bahan Pengganti**: Temukan alternatif bahan yang mirip
    4. **Saran Resep**: Dapatkan ide masakan berdasarkan bahan yang tersedia
    
    ### 🔧 Teknologi:
    - **Cosine Similarity** untuk menghitung kemiripan
    - **Clustering** untuk pengelompokan bahan
    - **Computer Vision** untuk deteksi gambar (simulasi)
    - **NLP** untuk pemrosesan teks input
    
    ### 📊 Data:
    Sistem ini menggunakan dataset dengan **69 bahan makanan** yang telah dianalisis 
    berdasarkan 10 karakteristik berbeda.
    """)
    
    st.success("🍳 Selamat bereksperimen dengan bahan makanan!")

if __name__ == "__main__":
    main() 