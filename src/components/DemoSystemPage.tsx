import { useState } from 'react';
import { Search, ArrowLeft, Sparkles } from 'lucide-react';
import { Ingredient } from '../App';
import { ingredientsDatabase } from '../data/ingredientsData';
import { calculateSimilarity } from '../utils/contentBasedFiltering';
<<<<<<< Updated upstream
import { Logo } from './Logo';
=======
import { getClosestIngredient } from '../utils/ingredientSearch';
import { HeaderLogo } from './HeaderLogo';
>>>>>>> Stashed changes

interface DemoSystemPageProps {
  onBack: () => void;
  onAboutMethod: () => void;
}

export function DemoSystemPage({ onBack, onAboutMethod }: DemoSystemPageProps) {
  const [dishInput, setDishInput] = useState('');
  const [detectedIngredient, setDetectedIngredient] = useState<Ingredient | null>(null);
  const [recommendations, setRecommendations] = useState<Array<{
    ingredient: Ingredient;
    similarity: number;
    reasons: string[];
  }>>([]);
  const [showResults, setShowResults] = useState(false);

<<<<<<< Updated upstream
  // Function to detect ingredient from dish name
  const detectIngredientFromDish = (dish: string): Ingredient | null => {
    const dishLower = dish.toLowerCase();
    
    // Try to find ingredient mentioned in the dish name
    for (const ingredient of ingredientsDatabase) {
      if (dishLower.includes(ingredient.name.toLowerCase())) {
        return ingredient;
      }
    }
    
    return null;
  };

  const handleSearch = () => {
    if (!dishInput.trim()) return;

    const detected = detectIngredientFromDish(dishInput);
    
=======
  const handleSearch = () => {
    if (!dishInput.trim()) return;

    // Cari bahan yang sesuai di ingredientsData.ts
    const detected = getClosestIngredient(dishInput);

>>>>>>> Stashed changes
    if (!detected) {
      alert('Maaf, bahan tidak terdeteksi. Coba masukkan nama bahan seperti "Ayam", "Bayam", "Ikan Mas", "Daging Sapi", dll.');
      return;
    }

    setDetectedIngredient(detected);

<<<<<<< Updated upstream
    // Calculate recommendations
=======
    // Hitung rekomendasi bahan pengganti
>>>>>>> Stashed changes
    const recs = ingredientsDatabase
      .filter(item => item.id !== detected.id)
      .map(item => ({
        ingredient: item,
        similarity: calculateSimilarity(detected, item),
        reasons: generateReasons(detected, item)
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, 5);
    
    setRecommendations(recs);
    setShowResults(true);
  };

  const handleReset = () => {
    setDishInput('');
    setDetectedIngredient(null);
    setRecommendations([]);
    setShowResults(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const generateReasons = (original: Ingredient, substitute: Ingredient): string[] => {
    const reasons: string[] = [];
    
    if (original.category === substitute.category) {
      reasons.push(`Kategori sama: ${substitute.category}`);
    }
    
    if (original.texture === substitute.texture) {
      reasons.push(`Tekstur serupa: ${substitute.texture}`);
    }
    
    const energyDiff = Math.abs(original.energy - substitute.energy);
    if (energyDiff < 50) {
      reasons.push('Kandungan energi mirip');
    }
    
    const proteinDiff = Math.abs(original.protein - substitute.protein);
    if (proteinDiff < 5) {
      reasons.push('Kandungan protein mirip');
    }
    
    const carbsDiff = Math.abs(original.carbs - substitute.carbs);
    if (carbsDiff < 5) {
      reasons.push('Kandungan karbohidrat serupa');
    }

    const fatDiff = Math.abs(original.fat - substitute.fat);
    if (fatDiff < 5) {
      reasons.push('Kandungan lemak serupa');
    }
    
    return reasons;
  };

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.8) return 'text-green-600 bg-green-50';
    if (similarity >= 0.6) return 'text-blue-600 bg-blue-50';
    return 'text-orange-600 bg-orange-50';
  };

  const getSimilarityLabel = (similarity: number) => {
    if (similarity >= 0.8) return 'Sangat Cocok';
    if (similarity >= 0.6) return 'Cocok';
    return 'Cukup Cocok';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50">
      {/* Header */}
      <header className="bg-transparent">
        <div className="container mx-auto px-6 py-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={onBack} className="flex items-center gap-3 hover:opacity-80 transition-opacity text-left">
              <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center p-2">
                <Logo />
              </div>
              <div>
                <div className="font-bold text-gray-900 text-lg">Recipe</div>
                <div className="text-sm text-gray-600">Sistem Rekomendasi</div>
              </div>
            </button>
          </div>
          <nav className="flex gap-8">
            <button className="text-blue-600 font-semibold">Demo Sistem</button>
            <button onClick={onAboutMethod} className="text-gray-700 hover:text-blue-600 font-medium">Tentang Metode</button>
          </nav>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12 max-w-5xl">
        {!showResults ? (
          <>
            {/* Title Section */}
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                Demo Sistem Rekomendasi
              </h1>
              <p className="text-gray-600 text-lg max-w-3xl mx-auto">
                Sistem akan menganalisis bahan utama dari masakan Anda dan memberikan rekomendasi
                pengganti berdasarkan <span className="text-blue-600 font-semibold">Energi, Protein, Lemak, Karbohidrat, Tekstur,</span> dan <span className="text-blue-600 font-semibold">Kategori</span> menggunakan algoritma Content Based Filtering.
              </p>
            </div>

            {/* Input Section */}
            <div className="bg-white rounded-3xl shadow-xl p-10">
              <div className="flex items-center justify-center mb-6">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                  <Sparkles className="w-8 h-8 text-blue-600" />
                </div>
              </div>

              <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
                Mau masak apa?
              </h2>

              <div className="max-w-2xl mx-auto mb-6">
                <input
                  type="text"
                  value={dishInput}
                  onChange={(e) => setDishInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Contoh: Kare Ayam, Rendang Sapi, Soto Ayam, Gulai Kambing..."
                  className="w-full px-6 py-5 border-2 border-gray-200 rounded-2xl focus:outline-none focus:border-blue-400 text-lg"
                />
              </div>

              <div className="text-center mb-8">
                <button
                  onClick={handleSearch}
                  disabled={!dishInput.trim()}
                  className="px-10 py-4 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all font-semibold shadow-lg hover:shadow-xl inline-flex items-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Search className="w-5 h-5" />
                  Cari Bahan Pengganti
                </button>
              </div>

<<<<<<< Updated upstream
              {/* Popular Suggestions */}
              <div className="max-w-2xl mx-auto">
                <p className="text-sm text-gray-500 mb-3 text-center">Contoh masakan populer:</p>
                <div className="flex flex-wrap justify-center gap-2">
                  {['Kare Ayam', 'Rendang Sapi', 'Gulai Kambing', 'Soto Ayam', 'Pepes Ikan'].map((suggestion) => (
=======
              {/* Suggestions */}
              <div>
                <p className="text-xs text-gray-400 mb-2">Coba salah satu:</p>
                <div className="flex flex-wrap gap-1.5">
                  {['Kare Ayam', 'Rendang Sapi', 'Gulai Kambing', 'Soto Ayam', 'Pepes Ikan'].map((s) => (
>>>>>>> Stashed changes
                    <button
                      key={suggestion}
                      onClick={() => setDishInput(suggestion)}
                      className="px-4 py-2 bg-blue-50 text-blue-600 rounded-full text-sm hover:bg-blue-100 transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </>
        ) : (
<<<<<<< Updated upstream
          /* Results Section */
          <div className="space-y-6">
            {/* Header Info */}
            <div className="bg-white rounded-3xl shadow-lg p-8">
              <div className="flex items-center justify-between mb-4">
                <div className="flex-1">
                  <div className="text-sm text-gray-500 mb-2">Masakan yang ingin dibuat:</div>
                  <h2 className="text-3xl font-bold text-gray-900">{dishInput}</h2>
=======
          /* Results */
          <div>
            {/* Back + Title */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <p className="text-xs text-gray-400 mb-1">Bahan yang Dicari</p>
                <h1 className="text-xl text-gray-900" style={{ fontWeight: 700 }}>{dishInput}</h1>
              </div>
              <button
                onClick={handleReset}
                className="text-sm text-gray-500 hover:text-blue-600 flex items-center gap-1.5"
              >
                <ArrowLeft className="w-4 h-4" />
                Cari lagi
              </button>
            </div>

            {/* Detected Ingredient */}
            <div className="bg-white border border-gray-200 rounded-lg p-5 mb-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-8 h-8 bg-blue-100 rounded flex items-center justify-center">
                  <Utensils className="w-4 h-4 text-blue-600" />
                </div>
                <div>
                  <p className="text-xs text-gray-400">Bahan utama terdeteksi</p>
                  <p className="text-gray-900" style={{ fontSize: '15px', fontWeight: 600 }}>{detectedIngredient?.name} <span className="text-gray-400" style={{ fontWeight: 400, fontSize: '13px' }}>— {detectedIngredient?.category}</span></p>
>>>>>>> Stashed changes
                </div>
                <button
                  onClick={handleReset}
                  className="text-blue-600 hover:text-blue-700 font-medium flex items-center gap-2"
                >
                  <ArrowLeft className="w-5 h-5" />
                  Cari Lagi
                </button>
              </div>

              <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-2xl p-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600 mb-1">Bahan utama yang terdeteksi:</div>
                    <div className="font-bold text-gray-900 text-2xl">{detectedIngredient?.name}</div>
                    <div className="text-sm text-gray-500">{detectedIngredient?.category}</div>
                  </div>
                </div>

                {/* Nutrisi Bahan Asli */}
                <div className="mt-4 pt-4 border-t border-blue-200">
                  <p className="text-sm font-semibold text-gray-700 mb-3">Karakteristik nutrisi:</p>
                  <div className="grid grid-cols-5 gap-3">
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-500">Energi</div>
                      <div className="font-semibold text-gray-900">{detectedIngredient?.energy} KKal</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-500">Protein</div>
                      <div className="font-semibold text-gray-900">{detectedIngredient?.protein}g</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-500">Lemak</div>
                      <div className="font-semibold text-gray-900">{detectedIngredient?.fat}g</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-500">Karbo</div>
                      <div className="font-semibold text-gray-900">{detectedIngredient?.carbs}g</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-xs text-gray-500">Tekstur</div>
                      <div className="font-semibold text-gray-900 text-sm">{detectedIngredient?.texture}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Recommendations */}
            <div className="bg-white rounded-3xl shadow-lg p-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">
                Rekomendasi Bahan Pengganti
              </h3>

              <div className="space-y-4">
                {recommendations.map((rec, index) => (
                  <div
                    key={rec.ingredient.id}
                    className="border-2 border-gray-200 rounded-2xl p-6 hover:border-blue-300 transition-all"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-2xl font-bold text-blue-600">
                            #{index + 1}
                          </span>
                          <div>
                            <div className="font-bold text-gray-900 text-2xl">
                              {rec.ingredient.name}
                            </div>
                            <span className="text-sm text-gray-500">{rec.ingredient.category}</span>
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`text-sm font-bold px-4 py-2 rounded-full ${getSimilarityColor(rec.similarity)}`}>
                          {getSimilarityLabel(rec.similarity)}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {(rec.similarity * 100).toFixed(1)}% cocok
                        </div>
                      </div>
                    </div>

                    {/* Nutrisi Comparison */}
                    <div className="bg-gray-50 rounded-xl p-4 mb-4">
                      <p className="text-sm font-semibold text-gray-700 mb-3">Perbandingan Nutrisi:</p>
                      <div className="grid grid-cols-5 gap-3">
                        <div className="text-center">
                          <div className="text-xs text-gray-500 mb-1">Energi</div>
                          <div className="font-semibold text-gray-900">{rec.ingredient.energy}</div>
                          <div className="text-xs text-gray-400">KKal</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xs text-gray-500 mb-1">Protein</div>
                          <div className="font-semibold text-gray-900">{rec.ingredient.protein}</div>
                          <div className="text-xs text-gray-400">gram</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xs text-gray-500 mb-1">Lemak</div>
                          <div className="font-semibold text-gray-900">{rec.ingredient.fat}</div>
                          <div className="text-xs text-gray-400">gram</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xs text-gray-500 mb-1">Karbo</div>
                          <div className="font-semibold text-gray-900">{rec.ingredient.carbs}</div>
                          <div className="text-xs text-gray-400">gram</div>
                        </div>
                        <div className="text-center">
                          <div className="text-xs text-gray-500 mb-1">Tekstur</div>
                          <div className="font-semibold text-gray-900 text-sm">{rec.ingredient.texture}</div>
                        </div>
                      </div>
                    </div>

                    {/* Reasons */}
                    <div className="bg-blue-50 rounded-xl p-4">
                      <p className="text-sm font-semibold text-blue-900 mb-2">Alasan Rekomendasi:</p>
                      <ul className="space-y-1">
                        {rec.reasons.map((reason, idx) => (
                          <li key={idx} className="text-sm text-blue-800 flex items-start gap-2">
                            <span className="text-green-500 mt-0.5">✓</span>
                            <span>{reason}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
