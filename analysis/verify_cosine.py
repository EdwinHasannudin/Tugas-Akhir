"""
Verifikasi Cosine Similarity: Nutrition + Texture One-Hot
Mencocokkan perhitungan manual dengan kode TypeScript
"""
import math

# Data Sapi (scaled) dari ingredientsData.ts
sapi = {"energy": 0.22, "protein": 0.23, "fat": 0.14, "carbs": 0.0, "texture": "padat"}
domba = {"energy": 0.22, "protein": 0.21, "fat": 0.15, "carbs": 0.0, "texture": "padat"}
ayam = {"energy": 0.32, "protein": 0.22, "fat": 0.25, "carbs": 0.0, "texture": "padat"}
tempe = {"energy": 0.16, "protein": 0.17, "fat": 0.08, "carbs": 0.01, "texture": "padat"}
kerbau = {"energy": 0.09, "protein": 0.23, "fat": 0.01, "carbs": 0.0, "texture": "padat"}
kambing = {"energy": 0.16, "protein": 0.20, "fat": 0.09, "carbs": 0.0, "texture": "padat"}
ikan = {"energy": 0.12, "protein": 0.20, "fat": 0.04, "carbs": 0.0, "texture": "lembut"}

# Textures sorted: ['cair', 'lembut', 'padat', 'renyah']
all_textures = ['cair', 'lembut', 'padat', 'renyah']

def build_vector(ing):
    """Nutrition + Texture One-Hot (sama dengan buildNutritionTextureVector di TS)"""
    nutrition = [ing["energy"], ing["protein"], ing["fat"], ing["carbs"]]
    texture_vec = [1 if t == ing["texture"] else 0 for t in all_textures]
    return nutrition + texture_vec

def cosine_sim(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a ** 2 for a in v1))
    mag2 = math.sqrt(sum(a ** 2 for a in v2))
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot / (mag1 * mag2)

def euclidean_dist(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def manhattan_dist(v1, v2):
    return sum(abs(a - b) for a, b in zip(v1, v2))

# ============================================================
print("=" * 90)
print("VERIFIKASI PERHITUNGAN: Sapi vs Bahan Lain")
print("Vector = [energy, protein, fat, carbs, tex_cair, tex_lembut, tex_padat, tex_renyah]")
print("=" * 90)

targets = [
    ("Domba", domba), ("Kambing", kambing), ("Tempe", tempe),
    ("Ayam", ayam), ("Kerbau", kerbau), ("Ikan", ikan)
]

v_sapi = build_vector(sapi)
print(f"\nSapi vector: {v_sapi}")
print()

print(f"{'Bahan':<10} {'Vector':<55} {'Euc':<10} {'Man':<10} {'Cos':<10} {'Avg':<10}")
print("-" * 105)

results = []
for name, ing in targets:
    v = build_vector(ing)
    euc = euclidean_dist(v_sapi, v)
    man = manhattan_dist(v_sapi, v)
    cos = cosine_sim(v_sapi, v)
    avg = (euc + man + cos) / 3
    results.append((name, v, euc, man, cos, avg))
    print(f"{name:<10} {str(v):<55} {euc:<10.4f} {man:<10.4f} {cos:<10.4f} {avg:<10.4f}")

print()
print("=" * 90)
print("DETAIL COSINE SIMILARITY: Sapi vs Domba (step by step)")
print("=" * 90)
v1 = v_sapi
v2 = build_vector(domba)
print(f"v1 (Sapi):  {v1}")
print(f"v2 (Domba): {v2}")
print()

# Step by step
dot_components = [a * b for a, b in zip(v1, v2)]
dot = sum(dot_components)
mag1_components = [a ** 2 for a in v1]
mag1 = math.sqrt(sum(mag1_components))
mag2_components = [a ** 2 for a in v2]
mag2 = math.sqrt(sum(mag2_components))

print("Dot product components:")
for i, (a, b, d) in enumerate(zip(v1, v2, dot_components)):
    label = ["energy", "protein", "fat", "carbs", "tex_cair", "tex_lembut", "tex_padat", "tex_renyah"][i]
    print(f"  {label:<15} {a:.4f} * {b:.4f} = {d:.6f}")
print(f"  SUM (dot product) = {dot:.6f}")
print()

print(f"|v1| components: {[round(x, 6) for x in mag1_components]}")
print(f"|v1| = sqrt({sum(mag1_components):.6f}) = {mag1:.6f}")
print(f"|v2| components: {[round(x, 6) for x in mag2_components]}")
print(f"|v2| = sqrt({sum(mag2_components):.6f}) = {mag2:.6f}")
print()
print(f"Cosine = {dot:.6f} / ({mag1:.6f} * {mag2:.6f})")
print(f"       = {dot:.6f} / {mag1 * mag2:.6f}")
print(f"       = {dot / (mag1 * mag2):.6f}")

print()
print("=" * 90)
print("DETAIL COSINE SIMILARITY: Sapi vs Ikan (BEDA TEKSTUR)")
print("=" * 90)
v2_ikan = build_vector(ikan)
print(f"v1 (Sapi): {v_sapi}  (texture=padat)")
print(f"v2 (Ikan): {v2_ikan}  (texture=lembut)")
print()

dot_components = [a * b for a, b in zip(v_sapi, v2_ikan)]
dot = sum(dot_components)
mag1 = math.sqrt(sum(a ** 2 for a in v_sapi))
mag2 = math.sqrt(sum(a ** 2 for a in v2_ikan))

print("Dot product components:")
for i, (a, b, d) in enumerate(zip(v_sapi, v2_ikan, dot_components)):
    label = ["energy", "protein", "fat", "carbs", "tex_cair", "tex_lembut", "tex_padat", "tex_renyah"][i]
    marker = " <-- BEDA TEKSTUR (0*1=0)" if label in ["tex_lembut", "tex_padat"] and a != b else ""
    print(f"  {label:<15} {a:.4f} * {b:.4f} = {d:.6f}{marker}")
print(f"  SUM (dot product) = {dot:.6f}")
print(f"  Cosine = {dot / (mag1 * mag2):.6f}")

print()
print("=" * 90)
print("RANKING FINAL (sorted by Avg ascending)")
print("=" * 90)
results.sort(key=lambda x: x[5])
for i, (name, v, euc, man, cos, avg) in enumerate(results):
    print(f"  {i+1}. {name:<10} Euc={euc:.4f}  Man={man:.4f}  Cos={cos:.4f}  Avg={avg:.4f}")
