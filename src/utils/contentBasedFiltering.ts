import { Ingredient } from '../App';

/**
 * Content-Based Filtering Algorithm
 * Menghitung similarity antara dua bahan berdasarkan berbagai fitur
 */

// Hitung similarity untuk nilai numerik menggunakan inverse of absolute difference
const numericalSimilarity = (val1: number, val2: number, maxDiff: number): number => {
  const diff = Math.abs(val1 - val2);
  return Math.max(0, 1 - (diff / maxDiff));
};

// Hitung similarity untuk nilai kategorikal (exact match)
const categoricalSimilarity = (val1: string, val2: string): number => {
  return val1 === val2 ? 1 : 0;
};

// Weight untuk setiap fitur dalam perhitungan similarity
const WEIGHTS = {
  category: 0.20,      // Kategori bahan (20%)
  energy: 0.15,        // Energi/KKal (15%)
  protein: 0.15,       // Kandungan protein (15%)
  carbs: 0.15,         // Kandungan karbohidrat (15%)
  fat: 0.10,           // Kandungan lemak (10%)
  texture: 0.25        // Tekstur (25%)
};

/**
 * Menghitung similarity score antara dua ingredient
 * Menggunakan weighted sum dari berbagai fitur
 * 
 * @param ingredient1 - Bahan asli
 * @param ingredient2 - Bahan kandidat pengganti
 * @returns Similarity score antara 0-1 (1 = sangat mirip)
 */
export const calculateSimilarity = (ingredient1: Ingredient, ingredient2: Ingredient): number => {
  // 1. Category similarity (exact match)
  const categorySim = categoricalSimilarity(ingredient1.category, ingredient2.category);
  
  // 2. Nutritional similarities (menggunakan range maksimum untuk normalisasi)
  const energySim = numericalSimilarity(ingredient1.energy, ingredient2.energy, 500);
  const proteinSim = numericalSimilarity(ingredient1.protein, ingredient2.protein, 30);
  const carbsSim = numericalSimilarity(ingredient1.carbs, ingredient2.carbs, 50);
  const fatSim = numericalSimilarity(ingredient1.fat, ingredient2.fat, 100);
  
  // 3. Texture similarity (exact match)
  const textureSim = categoricalSimilarity(ingredient1.texture, ingredient2.texture);
  
  // 4. Weighted sum of all similarities
  const totalSimilarity = 
    (categorySim * WEIGHTS.category) +
    (energySim * WEIGHTS.energy) +
    (proteinSim * WEIGHTS.protein) +
    (carbsSim * WEIGHTS.carbs) +
    (fatSim * WEIGHTS.fat) +
    (textureSim * WEIGHTS.texture);
  
  return totalSimilarity;
};

/**
 * Build feature vector from ingredient (raw scaled numerics + one-hot categoricals)
 * Menggunakan raw values dengan scaling yang sesuai untuk better cosine similarity distribution
 */
const buildFeatureVector = (ing: Ingredient, allIngredients: Ingredient[]): number[] => {
  // Numeric features dengan scaling yang lebih baik untuk distribusi cosine similarity
  // Raw values dengan multiplier untuk memberi weight lebih pada nutrisi numerik
  const numericScaled = [
    ing.energy * 2,      // Scale energy 2x 
    ing.protein * 3,     // Scale protein 3x (lebih penting untuk rekomendasi)
    ing.fat * 2,         // Scale fat 2x
    ing.carbs * 2        // Scale carbs 2x
  ];

  // One-hot for texture
  const textures = [...new Set(allIngredients.map(i => i.texture))].sort();
  const textureVec = textures.map(t => t === ing.texture ? 1 : 0);

  // One-hot for category
  const categories = [...new Set(allIngredients.map(i => i.category))].sort();
  const categoryVec = categories.map(c => c === ing.category ? 1 : 0);

  return [...numericScaled, ...textureVec, ...categoryVec];
};

/** Euclidean Distance Similarity: 1 / (1 + dist) */
export const euclideanSimilarity = (ing1: Ingredient, ing2: Ingredient, all: Ingredient[]): number => {
  const v1 = buildFeatureVector(ing1, all);
  const v2 = buildFeatureVector(ing2, all);
  const dist = Math.sqrt(v1.reduce((sum, val, i) => sum + (val - v2[i]) ** 2, 0));
  return 1 / (1 + dist);
};

/** Manhattan Distance Similarity: 1 / (1 + dist) */
export const manhattanSimilarity = (ing1: Ingredient, ing2: Ingredient, all: Ingredient[]): number => {
  const v1 = buildFeatureVector(ing1, all);
  const v2 = buildFeatureVector(ing2, all);
  const dist = v1.reduce((sum, val, i) => sum + Math.abs(val - v2[i]), 0);
  return 1 / (1 + dist);
};

/** Cosine Similarity */
export const cosineSimilarity = (ing1: Ingredient, ing2: Ingredient, all: Ingredient[]): number => {
  const v1 = buildFeatureVector(ing1, all);
  const v2 = buildFeatureVector(ing2, all);
  const dot = v1.reduce((sum, val, i) => sum + val * v2[i], 0);
  const mag1 = Math.sqrt(v1.reduce((sum, val) => sum + val ** 2, 0));
  const mag2 = Math.sqrt(v2.reduce((sum, val) => sum + val ** 2, 0));
  if (mag1 === 0 || mag2 === 0) return 0;
  return dot / (mag1 * mag2);
};

/**
 * Mendapatkan top N recommendations untuk sebuah ingredient
 * 
 * @param targetIngredient - Bahan yang ingin dicari penggantinya
 * @param candidates - Array kandidat bahan pengganti
 * @param topN - Jumlah rekomendasi yang diinginkan
 * @returns Array of top N similar ingredients dengan similarity scores
 */
export const getTopRecommendations = (
  targetIngredient: Ingredient,
  candidates: Ingredient[],
  topN: number = 5
): Array<{ ingredient: Ingredient; similarity: number }> => {
  // Filter out the target ingredient itself
  const filteredCandidates = candidates.filter(
    candidate => candidate.id !== targetIngredient.id
  );
  
  // Calculate similarity for each candidate
  const scoredCandidates = filteredCandidates.map(candidate => ({
    ingredient: candidate,
    similarity: calculateSimilarity(targetIngredient, candidate)
  }));
  
  // Sort by similarity (descending) and return top N
  return scoredCandidates
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, topN);
};