# =============================================================
# SISTEM REKOMENDASI BAHAN PENGGANTI MAKANAN
# METODE: CONTENT-BASED FILTERING (CBF)
# =============================================================

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import requests
from io import BytesIO

# ------------------------------
# 1️⃣ Konfigurasi halaman
# ------------------------------
st.set_page_config(
    page_title="Sistem Rekomendasi Bahan Pengganti",
    page_icon="🍳",
    layout="wide"
)

st.title("🍽️ Sistem Rekomendasi Bahan Pengganti Masakan")
st.markdown("Sistem ini menggunakan pendekatan **Content-Based Filtering** untuk merekomendasikan bahan pengganti berdasarkan kemiripan nutrisi, kategori, dan tekstur bahan.")

# ------------------------------
# 2️⃣ Baca dataset hasil labeling
# ------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("nutrition_data_with_categories_texture.xlsx")
    return df

df = load_data()

# ------------------------------
# 3️⃣ Siapkan fitur gabungan
# ------------------------------
df["combined_features"] = (
    df["kategori"].astype(str) + " " +
    df["texture"].astype(str) + " " +
    df["calories"].astype(str) + " " +
    df["proteins"].astype(str) + " " +
    df["fat"].astype(str) + " " +
    df["carbohydrate"].astype(str)
)

# TF-IDF dan cosine similarity
tfidf = TfidfVectorizer(stop_words=None)
tfidf_matrix = tfidf.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# ------------------------------
# 4️⃣ Fungsi rekomendasi
# ------------------------------
def rekomendasi_bahan(nama_bahan, top_n=5):
    nama_bahan = nama_bahan.lower()
    if nama_bahan not in df["name"].str.lower().values:
        return None
    idx = df[df["name"].str.lower() == nama_bahan].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, _ in sim_scores[1:top_n+1]]
    return df.iloc[top_indices]

# ------------------------------
# 5️⃣ Input dari pengguna
# ------------------------------
col1, col2 = st.columns([2, 3])

with col1:
    bahan_input = st.text_input("Masukkan nama bahan makanan:", placeholder="contoh: Nasi Goreng atau Ayam Goreng")

    top_n = st.slider("Jumlah rekomendasi yang ingin ditampilkan:", 1, 10, 5)

    if st.button("🔍 Cari Rekomendasi"):
        if bahan_input.strip() == "":
            st.warning("Masukkan nama bahan terlebih dahulu!")
        else:
            hasil = rekomendasi_bahan(bahan_input, top_n=top_n)

            if hasil is None:
                st.error(f"Bahan '{bahan_input}' tidak ditemukan dalam dataset.")
            else:
                st.success(f"Hasil rekomendasi bahan pengganti untuk **{bahan_input.title()}**:")

                for _, row in hasil.iterrows():
                    with st.container():
                        st.markdown(f"### 🥘 {row['name']}")
                        st.markdown(f"**Kategori:** {row['kategori'].title()}  |  **Tekstur:** {row['texture'].title()}")
                        st.markdown(
                            f"**Kalori:** {row['calories']} kcal  |  "
                            f"**Protein:** {row['proteins']} g  |  "
                            f"**Lemak:** {row['fat']} g  |  "
                            f"**Karbohidrat:** {row['carbohydrate']} g"
                        )
                        if "image" in df.columns and pd.notna(row["image"]):
                            try:
                                img = Image.open(BytesIO(requests.get(row["image"]).content))
                                st.image(img, width=250)
                            except:
                                st.info("📷 Gambar tidak tersedia.")
                        st.divider()

with col2:
    st.markdown("### 📊 Statistik Dataset")
    st.metric("Total Bahan", len(df))
    st.metric("Kategori Unik", df["kategori"].nunique())
    st.metric("Tekstur Unik", df["texture"].nunique())
    st.dataframe(df.head(10))
