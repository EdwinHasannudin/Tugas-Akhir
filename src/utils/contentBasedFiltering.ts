/**
 * Content-Based Filtering Algorithm - Pure Mathematical Approach
 * Menggunakan tiga metrik jarak/similarity: Cosine Similarity, Euclidean Distance, dan Manhattan Distance
 * 
 * Input: Feature vectors (sudah di-preprocess dengan Min-Max Scaling untuk numerik dan One-Hot Encoding untuk kategorik)
 * Output: Ketiga skor similarity/distance untuk perbandingan
 */

import { Ingredient } from '../App';

export interface SimilarityScores {
  cosineSimilarity: number;      // Range: -1 to 1 (1 = identical, higher is better)
  euclideanDistance: number;     // Range: 0 to infinity (0 = identical, lower is better)
  manhattanDistance: number;     // Range: 0 to infinity (0 = identical, lower is better)
}

/**
 * Menghitung Cosine Similarity antara dua vektor fitur
 * Rumus: similarity = (A · B) / (||A|| * ||B||)
 * 
 * @param vectorA - Feature vector dari bahan pertama
 * @param vectorB - Feature vector dari bahan kedua
 * @returns Cosine similarity score (range: -1 to 1, higher = more similar)
 */
export const calculateCosineSimilarity = (vectorA: number[], vectorB: number[]): number => {
  if (vectorA.length !== vectorB.length) {
    throw new Error('Vectors must have the same length');
  }
  
  // Dot product: A · B
  let dotProduct = 0;
  for (let i = 0; i < vectorA.length; i++) {
    dotProduct += vectorA[i] * vectorB[i];
  }
  
  // Magnitude/Norm: ||A|| dan ||B||
  let magnitudeA = 0;
  let magnitudeB = 0;
  for (let i = 0; i < vectorA.length; i++) {
    magnitudeA += vectorA[i] * vectorA[i];
    magnitudeB += vectorB[i] * vectorB[i];
  }
  magnitudeA = Math.sqrt(magnitudeA);
  magnitudeB = Math.sqrt(magnitudeB);
  
  // Avoid division by zero
  if (magnitudeA === 0 || magnitudeB === 0) {
    return 0;
  }
  
  return dotProduct / (magnitudeA * magnitudeB);
};

/**
 * Menghitung Euclidean Distance antara dua vektor fitur
 * Rumus: distance = sqrt(Σ(A[i] - B[i])²)
 * 
 * @param vectorA - Feature vector dari bahan pertama
 * @param vectorB - Feature vector dari bahan kedua
 * @returns Euclidean distance (range: 0 to infinity, lower = more similar)
 */
export const calculateEuclideanDistance = (vectorA: number[], vectorB: number[]): number => {
  if (vectorA.length !== vectorB.length) {
    throw new Error('Vectors must have the same length');
  }
  
  let sumSquaredDiff = 0;
  for (let i = 0; i < vectorA.length; i++) {
    const diff = vectorA[i] - vectorB[i];
    sumSquaredDiff += diff * diff;
  }
  
  return Math.sqrt(sumSquaredDiff);
};

/**
 * Menghitung Manhattan Distance antara dua vektor fitur
 * Rumus: distance = Σ|A[i] - B[i]|
 * 
 * @param vectorA - Feature vector dari bahan pertama
 * @param vectorB - Feature vector dari bahan kedua
 * @returns Manhattan distance (range: 0 to infinity, lower = more similar)
 */
export const calculateManhattanDistance = (vectorA: number[], vectorB: number[]): number => {
  if (vectorA.length !== vectorB.length) {
    throw new Error('Vectors must have the same length');
  }
  
  let sumAbsDiff = 0;
  for (let i = 0; i < vectorA.length; i++) {
    sumAbsDiff += Math.abs(vectorA[i] - vectorB[i]);
  }
  
  return sumAbsDiff;
};

/**
 * Menghitung ketiga skor similarity sekaligus untuk membandingkan hasil rekomendasi
 * 
 * @param queryVector - Feature vector dari bahan acuan (query)
 * @param targetVector - Feature vector dari bahan target
 * @returns Object berisi ketiga metrik scoring
 */
export const calculateAllSimilarityMetrics = (
  queryVector: number[],
  targetVector: number[]
): SimilarityScores => {
  return {
    cosineSimilarity: calculateCosineSimilarity(queryVector, targetVector),
    euclideanDistance: calculateEuclideanDistance(queryVector, targetVector),
    manhattanDistance: calculateManhattanDistance(queryVector, targetVector)
  };
};

/**
 * Mendapatkan top N recommendations berdasarkan metrik tertentu
 * 
 * @param queryVector - Feature vector dari bahan yang dicari penggantinya
 * @param candidates - Array of {id, vector} untuk bahan kandidat
 * @param metric - Metrik yang digunakan: 'cosine' | 'euclidean' | 'manhattan'
 * @param topN - Jumlah rekomendasi yang diinginkan
 * @returns Array of top N candidates dengan semua tiga skor
 */
export const getTopRecommendationsByMetric = (
  queryVector: number[],
  candidates: Array<{ id: string; vector: number[] }>,
  metric: 'cosine' | 'euclidean' | 'manhattan' = 'cosine',
  topN: number = 5
): Array<{ id: string; scores: SimilarityScores }> => {
  // Calculate all metrics for each candidate
  const scoredCandidates = candidates.map(candidate => ({
    id: candidate.id,
    scores: calculateAllSimilarityMetrics(queryVector, candidate.vector)
  }));
  
  // Sort berdasarkan metrik yang dipilih
  const sorted = scoredCandidates.sort((a, b) => {
    switch (metric) {
      case 'cosine':
        // Cosine: higher is better, sort descending
        return b.scores.cosineSimilarity - a.scores.cosineSimilarity;
      case 'euclidean':
      case 'manhattan':
        // Distance: lower is better, sort ascending
        return (metric === 'euclidean' 
          ? a.scores.euclideanDistance - b.scores.euclideanDistance
          : a.scores.manhattanDistance - b.scores.manhattanDistance);
      default:
        return 0;
    }
  });
  
  return sorted.slice(0, topN);
};

/**
 * ============================================================================
 * BACKWARD COMPATIBILITY LAYER - untuk integrasi dengan existing code
 * ============================================================================
 */

/**
 * Konversi Ingredient object menjadi feature vector
 * Struktur vektor: [energy, protein, carbs, fat, category_encoded..., texture_encoded...]
 * 
 * @param ingredient - Ingredient object
 * @returns Feature vector (number array)
 */
const ingredientToVector = (ingredient: Ingredient): number[] => {
  // Nutritional values (sudah di-normalize/scaled)
  const nutritionFeatures = [
    ingredient.energy,
    ingredient.protein,
    ingredient.carbs,
    ingredient.fat
  ];

  // Category One-Hot Encoding (kategori umum dalam masakan Indonesia)
  const categories = ['lauk', 'sayuran', 'rempah', 'tepung', 'cair'];
  const categoryEncoding = categories.map(cat => (ingredient.category === cat ? 1 : 0));

  // Texture One-Hot Encoding
  const textures = ['padat', 'cair', 'bubuk', 'biji'];
  const textureEncoding = textures.map(tex => (ingredient.texture === tex ? 1 : 0));

  // Gabungkan semua features
  return [...nutritionFeatures, ...categoryEncoding, ...textureEncoding];
};

/**
 * Backward compatibility function - hitung similarity dengan metrik cosine (default)
 * Menerima Ingredient objects seperti API lama
 * 
 * @param ingredient1 - Bahan pertama (Ingredient object)
 * @param ingredient2 - Bahan kedua (Ingredient object)
 * @param metric - Metrik yang digunakan: 'cosine' | 'euclidean' | 'manhattan'
 * @returns Normalized similarity score (0-1, higher = more similar)
 */
export const calculateSimilarity = (
  ingredient1: Ingredient,
  ingredient2: Ingredient,
  metric: 'cosine' | 'euclidean' | 'manhattan' = 'cosine'
): number => {
  const vector1 = ingredientToVector(ingredient1);
  const vector2 = ingredientToVector(ingredient2);
  const scores = calculateAllSimilarityMetrics(vector1, vector2);

  switch (metric) {
    case 'cosine':
      // Normalize cosine similarity from [-1,1] to [0,1]
      return (scores.cosineSimilarity + 1) / 2;
    case 'euclidean':
      // Normalize euclidean distance: lower distance = higher similarity
      // Max possible distance (rough estimate based on feature range)
      const maxDistance = Math.sqrt(4 + 5 + 4); // Sum of max squared differences
      return Math.max(0, 1 - (scores.euclideanDistance / maxDistance));
    case 'manhattan':
      // Normalize manhattan distance: lower distance = higher similarity
      const maxManhattan = 4 + 5 + 4; // Sum of max differences
      return Math.max(0, 1 - (scores.manhattanDistance / maxManhattan));
    default:
      return 0;
  }
};