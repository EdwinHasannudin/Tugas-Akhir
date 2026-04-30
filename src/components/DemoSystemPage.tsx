import { useState } from 'react';
import { Search, ArrowLeft, ArrowRight, Utensils, ChevronRight } from 'lucide-react';
import { Ingredient } from '../App';
import { ingredientsDatabase } from '../data/ingredientsData';
import nutritionRawData from '../data/nutrition_raw_dataset.json';
import nutritionScaledData from '../data/nutrition_scaled_dataset.json';
import laukData from '../data/lauk_dataset.json';
import sayuranData from '../data/sayuran_dataset.json';
import { euclideanDistance_NutritionOnly, manhattanDistance_NutritionOnly, cosineSimilarity_NutritionOnly } from '../utils/contentBasedFiltering';
import { detectIngredientFromDish, searchIngredients } from '../utils/ingredientSearch';
import { HeaderLogo } from './HeaderLogo';

interface NutritionData {
  id: number | string;
  name: string;
  energy: number;
  protein: number;
  fat: number;
  carbs: number;
  category?: string;
  image?: string;
}

interface DemoSystemPageProps {
  onBack: () => void;
}

// Note: oneHotEncode function dipindahkan ke relatedIngredients computation
// Tabel One-Hot Encoding sekarang menggunakan data dari lauk_dataset.json dan sayuran_dataset.json


export function DemoSystemPage({ onBack }: DemoSystemPageProps) {
  const [dishInput, setDishInput] = useState('');
  const [detectedIngredient, setDetectedIngredient] = useState<Ingredient | null>(null);
  const [recommendations, setRecommendations] = useState<Array<{
    ingredient: Ingredient;
    euc: number;
    man: number;
    cos: number;
    avg: number;
  }>>([]);
  const [showResults, setShowResults] = useState(false);
  const [currentStep, setCurrentStep] = useState(0); // 0=input, 1=minmax, 2=onehot, 3=results

  // Helper: Smart ingredient detection
  // Prioritas: detectIngredientFromDish (for "kare ayam" → "ayam") → searchIngredients
  const detectIngredient = (dish: string): Ingredient | null => {
    if (!dish.trim()) return null;
    
    // Coba deteksi dari nama masakan (smart parsing)
    // Misal: "kare ayam" → filter "kare" → detect "ayam" → return Ayam
    const detected = detectIngredientFromDish(dish);
    if (detected) return detected;
    
    // Fallback: cari langsung sebagai nama bahan
    const searchResults = searchIngredients(dish);
    if (searchResults.length === 0) return null;
    
    return searchResults[0].ingredient;
  };

  const handleSearch = () => {
    if (!dishInput.trim()) return;

    // Gunakan smart detection dengan prioritas detectIngredientFromDish
    const detected = detectIngredient(dishInput);

    if (!detected) {
      alert('Maaf, bahan tidak terdeteksi. Coba masukkan nama masakan seperti "Kare Ayam", "Rendang Sapi", "Soto Ayam", atau nama bahan seperti "Ayam", "Bayam", dll.');
      return;
    }

    // Set detected ingredient (dari ingredientsDatabase)
    setDetectedIngredient(detected);

    const recs = ingredientsDatabase
      .filter(item => item.id !== detected.id)
      .map(item => {
        const euc = euclideanDistance_NutritionOnly(detected, item);
        const man = manhattanDistance_NutritionOnly(detected, item);
        const cos = cosineSimilarity_NutritionOnly(detected, item);
        
        // Konversi Cosine Similarity menjadi Cosine Distance agar selaras dengan Euclidean & Manhattan
        // Euclidean & Manhattan: lebih kecil = lebih mirip
        // Cosine Similarity: lebih besar = lebih mirip -> Cosine Distance (1 - cos): lebih kecil = lebih mirip
        const cos_distance = 1 - cos;
        const avg = (euc + man + cos_distance) / 3;
        return { ingredient: item, euc, man, cos, avg };
      })
      .sort((a, b) => {
        // Prioritas 1: Kategori yang sama (kategori yang cocok di depan)
        const categoryMatch_a = a.ingredient.category === detected.category ? 0 : 1;
        const categoryMatch_b = b.ingredient.category === detected.category ? 0 : 1;
        if (categoryMatch_a !== categoryMatch_b) {
          return categoryMatch_a - categoryMatch_b;
        }

        // Prioritas 2: Tekstur yang sama (tekstur yang cocok di depan)
        const textureMatch_a = a.ingredient.texture === detected.texture ? 0 : 1;
        const textureMatch_b = b.ingredient.texture === detected.texture ? 0 : 1;
        
        if (textureMatch_a !== textureMatch_b) {
          return textureMatch_a - textureMatch_b;
        }
        
        // Prioritas 2: Average metrics (lebih rendah = lebih mirip)
        return a.avg - b.avg;
      })
      .slice(0, 5);

    setRecommendations(recs);
    setShowResults(true);
    setCurrentStep(1);
  };

  const handleReset = () => {
    setDishInput('');
    setDetectedIngredient(null);
    setRecommendations([]);
    setShowResults(false);
    setCurrentStep(0);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  // Prepare data tables FIRST:
  // Tampilkan SEMUA data dari Excel JSON files tanpa filter (all data in dataset)
  const rawDataForDisplay: NutritionData[] = nutritionRawData as NutritionData[];
  
  const scaledDataForDisplay: NutritionData[] = nutritionScaledData as NutritionData[];

  if (detectedIngredient) {
    // HANYA untuk highlight detected ingredient di UI, tapi tetap tampilkan semua data
  }

  // Compute min/max from displayed data untuk normalisasi
  const getMinMaxValues = (data: NutritionData[]) => {
    if (data.length === 0) return { mins: { energy: 0, protein: 0, fat: 0, carbs: 0 }, maxs: { energy: 0, protein: 0, fat: 0, carbs: 0 } };
    
    return {
      mins: {
        energy: Math.min(...data.map(d => typeof d.energy === 'number' ? d.energy : 0)),
        protein: Math.min(...data.map(d => typeof d.protein === 'number' ? d.protein : 0)),
        fat: Math.min(...data.map(d => typeof d.fat === 'number' ? d.fat : 0)),
        carbs: Math.min(...data.map(d => typeof d.carbs === 'number' ? d.carbs : 0)),
      },
      maxs: {
        energy: Math.max(...data.map(d => typeof d.energy === 'number' ? d.energy : 0)),
        protein: Math.max(...data.map(d => typeof d.protein === 'number' ? d.protein : 0)),
        fat: Math.max(...data.map(d => typeof d.fat === 'number' ? d.fat : 0)),
        carbs: Math.max(...data.map(d => typeof d.carbs === 'number' ? d.carbs : 0)),
      }
    };
  };

  const { mins, maxs } = getMinMaxValues(rawDataForDisplay);

  // Get relevant ingredients for One-Hot Encoding (detected + top 5 recs)
  const relevantIngredients = detectedIngredient
    ? [detectedIngredient, ...recommendations.map(r => r.ingredient)]
    : [];

  // For encoded data (One-Hot), gunakan relevantIngredients (detected + top 5 recs)
  // Note: encoded, textures, categories tidak digunakan setelah mengganti tabel dengan data dari JSON
  // oneHotEncode(relevantIngredients) masih disimpan jika diperlukan di masa depan

  const steps = [
    { num: 1, label: 'Min-Max Scaling' },
    { num: 2, label: 'One-Hot Encoding' },
    { num: 3, label: 'Hasil Rekomendasi' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <HeaderLogo onClick={onBack} />
          <nav className="flex gap-6">
            <span className="text-blue-600 text-sm" style={{ fontWeight: 600 }}>Demo Sistem</span>
            <button onClick={onBack} className="text-gray-500 hover:text-blue-600 text-sm">Beranda</button>
          </nav>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-6 py-10">
        {!showResults ? (
          <>
            {/* Title */}
            <div className="mb-8">
              <h1 className="text-2xl text-gray-900 mb-2" style={{ fontWeight: 700 }}>Demo Sistem Rekomendasi</h1>
              <p className="text-gray-500" style={{ fontSize: '14px', lineHeight: '1.6' }}>
                Masukkan nama masakan, sistem akan mendeteksi bahan utama dan mencarikan pengganti
                berdasarkan energi, protein, lemak, karbohidrat, tekstur, dan kategori.
              </p>
            </div>

            {/* Input Card */}
            <div className="bg-white border border-gray-200 rounded-lg p-6 max-w-2xl">
              <label className="block text-gray-900 mb-3" style={{ fontSize: '15px', fontWeight: 600 }}>
                Mau masak apa?
              </label>

              <div className="flex gap-2 mb-4">
                <input
                  type="text"
                  value={dishInput}
                  onChange={(e) => setDishInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Contoh: Kare Ayam, Rendang Sapi, Soto Ayam..."
                  className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                  style={{ fontSize: '14px' }}
                />
                <button
                  onClick={handleSearch}
                  disabled={!dishInput.trim()}
                  className="px-5 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  <Search className="w-4 h-4" />
                  Cari
                </button>
              </div>

              {/* Suggestions */}
              <div>
                <p className="text-xs text-gray-400 mb-2">Coba salah satu:</p>
                <div className="flex flex-wrap gap-1.5">
                  {['Kare Ayam', 'Rendang Sapi', 'Gulai Kambing', 'Soto Ayam', 'Pepes Ikan'].map((s) => (
                    <button
                      key={s}
                      onClick={() => setDishInput(s)}
                      className="px-3 py-1 bg-gray-100 text-gray-600 rounded text-xs hover:bg-gray-200 transition-colors"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </>
        ) : (
          <div>
            {/* Header info */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-blue-100 rounded flex items-center justify-center">
                  <Utensils className="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <p className="text-xs text-gray-400">Masakan: {dishInput}</p>
                  <p className="text-gray-900" style={{ fontSize: '15px', fontWeight: 600 }}>
                    Bahan terdeteksi: {detectedIngredient?.name}
                    <span className="text-gray-400 ml-1" style={{ fontWeight: 400, fontSize: '13px' }}>({detectedIngredient?.category})</span>
                  </p>
                </div>
              </div>
              <button
                onClick={handleReset}
                className="text-sm text-gray-500 hover:text-blue-600 flex items-center gap-1.5"
              >
                <ArrowLeft className="w-4 h-4" />
                Cari lagi
              </button>
            </div>

            {/* Step indicators */}
            <div className="flex items-center gap-2 mb-6">
              {steps.map((step, i) => (
                <div key={step.num} className="flex items-center gap-2">
                  <button
                    onClick={() => setCurrentStep(step.num)}
                    className={`flex items-center gap-2 px-3 py-1.5 rounded text-sm transition-colors ${
                      currentStep === step.num
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border border-gray-200 text-gray-500 hover:border-gray-300'
                    }`}
                    style={{ fontWeight: currentStep === step.num ? 600 : 400 }}
                  >
                    <span className="w-5 h-5 rounded-full flex items-center justify-center text-xs" style={{
                      background: currentStep === step.num ? 'rgba(255,255,255,0.2)' : '#f3f4f6',
                      fontWeight: 600
                    }}>
                      {step.num}
                    </span>
                    {step.label}
                  </button>
                  {i < steps.length - 1 && <ChevronRight className="w-4 h-4 text-gray-300" />}
                </div>
              ))}
            </div>

            {/* Step 1: Min-Max Scaling */}
            {currentStep === 1 && (
              <div>
                <div className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
                  <h2 className="text-gray-900 mb-1" style={{ fontSize: '16px', fontWeight: 600 }}>Min-Max Scaling</h2>
                  <p className="text-xs text-gray-400 mb-4" style={{ lineHeight: '1.5' }}>
                    Normalisasi fitur numerik (energi, protein, lemak, karbohidrat) ke rentang 0–1 agar setiap fitur punya bobot yang setara saat perhitungan similarity.
                  </p>

                  {/* Original data */}
                  <p className="text-xs text-gray-500 mb-2" style={{ fontWeight: 600 }}>Data Asli dari Nutrition Dataset</p>
                  <div className="overflow-x-auto mb-5" style={{ maxHeight: '250px', overflowY: 'auto' }}>
                    <table className="w-full text-xs border-collapse">
                      <thead className="sticky top-0 bg-gray-50">
                        <tr>
                          <th className="text-left text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Bahan</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Energi (KKal)</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Protein (g)</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Lemak (g)</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Karbo (g)</th>
                        </tr>
                      </thead>
                      <tbody>
                        {rawDataForDisplay.map((ing) => (
                          <tr key={ing.id}>
                            <td className="px-3 py-2 border border-gray-200 text-gray-800">
                              {ing.name}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700">
                              {typeof ing.energy === 'number' ? ing.energy.toFixed(4) : ing.energy}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700">
                              {typeof ing.protein === 'number' ? ing.protein.toFixed(4) : ing.protein}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700">
                              {typeof ing.fat === 'number' ? ing.fat.toFixed(4) : ing.fat}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700">
                              {typeof ing.carbs === 'number' ? ing.carbs.toFixed(4) : ing.carbs}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Min/Max info */}
                  <div className="flex gap-4 mb-4 text-xs">
                    <div className="bg-gray-50 px-3 py-2 rounded border border-gray-100">
                      <span className="text-gray-400">Min: </span>
                      <span className="text-gray-600">E={mins.energy} | P={mins.protein} | L={mins.fat} | K={mins.carbs}</span>
                    </div>
                    <div className="bg-gray-50 px-3 py-2 rounded border border-gray-100">
                      <span className="text-gray-400">Max: </span>
                      <span className="text-gray-600">E={maxs.energy} | P={maxs.protein} | L={maxs.fat} | K={maxs.carbs}</span>
                    </div>
                  </div>

                  {/* Formula */}
                  <div className="bg-gray-50 border border-gray-200 rounded px-3 py-2 mb-5">
                    <p className="text-xs text-gray-500" style={{ fontFamily: 'monospace' }}>
                      X_scaled = (X - X_min) / (X_max - X_min)
                    </p>
                  </div>

                  {/* Scaled data */}
                  <p className="text-xs text-gray-500 mb-2" style={{ fontWeight: 600 }}>Hasil Normalisasi (0–1) dari nutrition_scaled_dataset.json</p>
                  <div className="overflow-x-auto mb-5" style={{ maxHeight: '250px', overflowY: 'auto' }}>
                    <table className="w-full text-xs border-collapse">
                      <thead className="sticky top-0 bg-gray-50">
                        <tr>
                          <th className="text-left text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Bahan</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Energi</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Protein</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Lemak</th>
                          <th className="text-right text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Karbo</th>
                        </tr>
                      </thead>
                      <tbody>
                        {(scaledDataForDisplay as Record<string, any>[]).map((row: Record<string, any>) => (
                          <tr key={row.id}>
                            <td className="px-3 py-2 border border-gray-200 text-gray-800">
                              {row.name}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700 tabular-nums">
                              {typeof row.energy === 'number' ? row.energy.toFixed(4) : row.energy}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700 tabular-nums">
                              {typeof row.protein === 'number' ? row.protein.toFixed(4) : row.protein}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700 tabular-nums">
                              {typeof row.fat === 'number' ? row.fat.toFixed(4) : row.fat}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-right text-gray-700 tabular-nums">
                              {typeof row.carbs === 'number' ? row.carbs.toFixed(4) : row.carbs}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={() => setCurrentStep(2)}
                    className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                  >
                    Selanjutnya: One-Hot Encoding
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

            {/* Step 2: One-Hot Encoding */}
            {currentStep === 2 && (
              <div>
                <div className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
                  <h2 className="text-gray-900 mb-1" style={{ fontSize: '16px', fontWeight: 600 }}>One-Hot Encoding</h2>
                  <p className="text-xs text-gray-400 mb-4" style={{ lineHeight: '1.5' }}>
                    Mengubah fitur kategorikal (tekstur dan kategori) menjadi representasi biner (0/1) agar bisa dihitung secara numerik dalam similarity.
                  </p>

                  {/* Original categorical data */}
                  <p className="text-xs text-gray-500 mb-2" style={{ fontWeight: 600 }}>Data Kategorikal Asli</p>
                  <div className="overflow-x-auto mb-5">
                    <table className="w-full text-xs border-collapse">
                      <thead>
                        <tr className="bg-gray-50">
                          <th className="text-left text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Bahan</th>
                          <th className="text-left text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Tekstur</th>
                          <th className="text-left text-gray-500 px-3 py-2 border border-gray-200" style={{ fontWeight: 600 }}>Kategori</th>
                        </tr>
                      </thead>
                      <tbody>
                        {relevantIngredients.map((ing, i) => (
                          <tr key={ing.id} className={i === 0 ? 'bg-blue-50' : ''}>
                            <td className="px-3 py-2 border border-gray-200 text-gray-800" style={{ fontWeight: i === 0 ? 600 : 400 }}>
                              {ing.name} {i === 0 && <span className="text-blue-600 text-[10px]">(target)</span>}
                            </td>
                            <td className="px-3 py-2 border border-gray-200 text-gray-700">{ing.texture}</td>
                            <td className="px-3 py-2 border border-gray-200 text-gray-700">{ing.category}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>

                  {/* Encoded data - One-Hot Encoding tables */}
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <p className="text-xs text-gray-500 mb-4" style={{ fontWeight: 600 }}>Hasil One-Hot Encoding</p>
                    
                    {/* Tabel One-Hot Encoding Bahan Lauk */}
                    <div className="mb-6">
                      <p className="text-sm text-gray-700 mb-2" style={{ fontWeight: 600 }}>A. Hasil One-Hot Encoding Bahan Lauk</p>
                      <p className="text-xs text-gray-400 mb-3">Fitur tekstur dan kategori diubah menjadi representasi biner (0/1)</p>
                      <div className="overflow-x-auto border border-gray-200 rounded-lg" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                        <table className="text-xs border-collapse" style={{ minWidth: '100%' }}>
                          <thead style={{ position: 'sticky', top: 0 }}>
                            <tr className="bg-blue-50">
                              <th className="text-left text-gray-600 px-2 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, minWidth: '150px' }}>Bahan</th>
                              {/* Texture columns */}
                              <th className="text-center text-gray-500 px-1 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, fontSize: '10px' }}>Tekstur Padat</th>
                              <th className="text-center text-gray-500 px-1 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, fontSize: '10px' }}>Tekstur Lembut</th>
                              <th className="text-center text-gray-500 px-1 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, fontSize: '10px' }}>Tekstur Cair</th>
                            </tr>
                          </thead>
                          <tbody>
                            {(laukData as any[]).map((item, idx) => (
                              <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                                <td className="px-2 py-2 border border-gray-200 text-gray-800 whitespace-nowrap" style={{ fontWeight: 600, minWidth: '150px' }}>
                                  {item.name}
                                </td>
                                <td className="px-1 py-2 border border-gray-200 text-center" style={{ color: item.texture_padat === 1 ? '#059669' : '#d1d5db', fontWeight: item.texture_padat === 1 ? 600 : 400 }}>
                                  {item.texture_padat ? '1' : '0'}
                                </td>
                                <td className="px-1 py-2 border border-gray-200 text-center" style={{ color: item.texture_lembut === 1 ? '#059669' : '#d1d5db', fontWeight: item.texture_lembut === 1 ? 600 : 400 }}>
                                  {item.texture_lembut ? '1' : '0'}
                                </td>
                                <td className="px-1 py-2 border border-gray-200 text-center" style={{ color: item.texture_cair === 1 ? '#059669' : '#d1d5db', fontWeight: item.texture_cair === 1 ? 600 : 400 }}>
                                  {item.texture_cair ? '1' : '0'}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>

                    {/* Tabel One-Hot Encoding Bahan Sayuran */}
                    <div>
                      <p className="text-sm text-gray-700 mb-2" style={{ fontWeight: 600 }}>B. Hasil One-Hot Encoding Bahan Sayuran</p>
                      <p className="text-xs text-gray-400 mb-3">Fitur tekstur dan kategori diubah menjadi representasi biner (0/1)</p>
                      <div className="overflow-x-auto border border-gray-200 rounded-lg" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                        <table className="text-xs border-collapse" style={{ minWidth: '100%' }}>
                          <thead style={{ position: 'sticky', top: 0 }}>
                            <tr className="bg-green-50">
                              <th className="text-left text-gray-600 px-2 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, minWidth: '150px' }}>Bahan</th>
                              {/* Texture columns */}
                              <th className="text-center text-gray-500 px-1 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, fontSize: '10px' }}>Tekstur Padat</th>
                              <th className="text-center text-gray-500 px-1 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, fontSize: '10px' }}>Tekstur Lembut</th>
                              <th className="text-center text-gray-500 px-1 py-2 border border-gray-200 whitespace-nowrap" style={{ fontWeight: 600, fontSize: '10px' }}>Tekstur Renyah</th>
                            </tr>
                          </thead>
                          <tbody>
                            {(sayuranData as any[]).map((item, idx) => (
                              <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                                <td className="px-2 py-2 border border-gray-200 text-gray-800 whitespace-nowrap" style={{ fontWeight: 600, minWidth: '150px' }}>
                                  {item.name}
                                </td>
                                <td className="px-1 py-2 border border-gray-200 text-center" style={{ color: item.texture_padat === 1 ? '#059669' : '#d1d5db', fontWeight: item.texture_padat === 1 ? 600 : 400 }}>
                                  {item.texture_padat ? '1' : '0'}
                                </td>
                                <td className="px-1 py-2 border border-gray-200 text-center" style={{ color: item.texture_lembut === 1 ? '#059669' : '#d1d5db', fontWeight: item.texture_lembut === 1 ? 600 : 400 }}>
                                  {item.texture_lembut ? '1' : '0'}
                                </td>
                                <td className="px-1 py-2 border border-gray-200 text-center" style={{ color: item.texture_renyah === 1 ? '#059669' : '#d1d5db', fontWeight: item.texture_renyah === 1 ? 600 : 400 }}>
                                  {item.texture_renyah ? '1' : '0'}
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="flex justify-between">
                  <button
                    onClick={() => setCurrentStep(1)}
                    className="px-4 py-2 bg-white border border-gray-200 text-gray-600 text-sm rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    Min-Max Scaling
                  </button>
                  <button
                    onClick={() => setCurrentStep(3)}
                    className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                  >
                    Selanjutnya: Hasil Rekomendasi
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}

            {/* Step 3: Recommendations */}
            {currentStep === 3 && (
              <div>
                {/* Detected Ingredient */}
                <div className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
                  <p className="text-xs text-gray-400 mb-2">Nutrisi bahan target</p>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b border-gray-100">
                          <th className="text-left text-xs text-gray-400 pb-2" style={{ fontWeight: 500 }}>Energi</th>
                          <th className="text-left text-xs text-gray-400 pb-2" style={{ fontWeight: 500 }}>Protein</th>
                          <th className="text-left text-xs text-gray-400 pb-2" style={{ fontWeight: 500 }}>Lemak</th>
                          <th className="text-left text-xs text-gray-400 pb-2" style={{ fontWeight: 500 }}>Karbo</th>
                          <th className="text-left text-xs text-gray-400 pb-2" style={{ fontWeight: 500 }}>Tekstur</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr>
                          <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.energy.toFixed(4)} (scaled)</td>
                          <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.protein.toFixed(4)} (scaled)</td>
                          <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.fat.toFixed(4)} (scaled)</td>
                          <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.carbs.toFixed(4)} (scaled)</td>
                          <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.texture}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Recommendations */}
                <div className="mb-4">
                  <h2 className="text-gray-900 mb-1" style={{ fontSize: '16px', fontWeight: 600 }}>Rekomendasi Pengganti</h2>
                  <p className="text-xs text-gray-400">Top 5 bahan diurutkan berdasarkan rata-rata (Avg) dari Euclidean, Manhattan, dan Cosine Similarity</p>
                </div>

                <div className="space-y-3 mb-6">
                  {recommendations.map((rec, index) => (
                    <div
                      key={rec.ingredient.id}
                      className="bg-white border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-baseline gap-2">
                          <span className="text-sm text-gray-400" style={{ fontWeight: 600 }}>{index + 1}.</span>
                          <div>
                            <span className="text-gray-900" style={{ fontSize: '15px', fontWeight: 600 }}>{rec.ingredient.name}</span>
                            <span className="text-xs text-gray-400 ml-2">{rec.ingredient.category}</span>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 text-xs tabular-nums">
                          <span className="text-gray-400">Euc <span className="text-gray-700" style={{ fontWeight: 600 }}>{rec.euc.toFixed(4)}</span></span>
                          <span className="text-gray-400">Man <span className="text-gray-700" style={{ fontWeight: 600 }}>{rec.man.toFixed(4)}</span></span>
                          <span className="text-gray-400">Cos <span className="text-gray-700" style={{ fontWeight: 600 }}>{rec.cos.toFixed(4)}</span></span>
                          <span className="text-gray-400">Avg <span className="text-blue-700" style={{ fontWeight: 600 }}>{rec.avg.toFixed(4)}</span></span>
                        </div>
                      </div>

                      <div className="overflow-x-auto">
                        <table className="w-full text-xs">
                          <thead>
                            <tr className="border-b border-gray-100">
                              <th className="text-left text-gray-400 pb-1.5 pr-4" style={{ fontWeight: 500 }}>Energi</th>
                              <th className="text-left text-gray-400 pb-1.5 pr-4" style={{ fontWeight: 500 }}>Protein</th>
                              <th className="text-left text-gray-400 pb-1.5 pr-4" style={{ fontWeight: 500 }}>Lemak</th>
                              <th className="text-left text-gray-400 pb-1.5 pr-4" style={{ fontWeight: 500 }}>Karbo</th>
                              <th className="text-left text-gray-400 pb-1.5" style={{ fontWeight: 500 }}>Tekstur</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.energy.toFixed(4)} KKal</td>
                              <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.protein.toFixed(4)}g</td>
                              <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.fat.toFixed(4)}g</td>
                              <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.carbs.toFixed(4)}g</td>
                              <td className="pt-1.5 text-gray-700">{rec.ingredient.texture}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex justify-start">
                  <button
                    onClick={() => setCurrentStep(2)}
                    className="px-4 py-2 bg-white border border-gray-200 text-gray-600 text-sm rounded-lg hover:bg-gray-50 transition-colors flex items-center gap-2"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    One-Hot Encoding
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}