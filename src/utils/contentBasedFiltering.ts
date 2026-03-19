import { Ingredient } from '../App';

/**
 * Content-Based Filtering Algorithm
 * Menghitung similarity antara dua bahan berdasarkan berbagai fitur
 */

// Normalisasi nilai numerik ke range 0-1
const normalize = (value: number, min: number, max: number): number => {
  if (max === min) return 0;
  return (value - min) / (max - min);
};

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
  fat: 0.15,           // Kandungan lemak (10% + 5%)
  texture: 0.20        // Tekstur (15% + 5%)
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