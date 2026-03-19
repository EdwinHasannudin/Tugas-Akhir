import { useState } from 'react';
import { Search, ArrowLeft, Utensils } from 'lucide-react';
import { Ingredient } from '../App';
import { ingredientsDatabase } from '../data/ingredientsData';
import { calculateSimilarity } from '../utils/contentBasedFiltering';
import { detectIngredientFromDish } from '../utils/ingredientSearch';
import { HeaderLogo } from './HeaderLogo';

interface DemoSystemPageProps {
  onBack: () => void;
}

export function DemoSystemPage({ onBack }: DemoSystemPageProps) {
  const [dishInput, setDishInput] = useState('');
  const [detectedIngredient, setDetectedIngredient] = useState<Ingredient | null>(null);
  const [recommendations, setRecommendations] = useState<Array<{
    ingredient: Ingredient;
    similarity: number;
  }>>([]);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = () => {
    if (!dishInput.trim()) return;

    const detected = detectIngredientFromDish(dishInput);

    if (!detected) {
      alert('Maaf, bahan tidak terdeteksi. Coba masukkan nama masakan yang lebih spesifik seperti "Kare Ayam", "Rendang Sapi", "Soto Ayam", dll.');
      return;
    }

    setDetectedIngredient(detected);

    const recs = ingredientsDatabase
      .filter(item => item.id !== detected.id)
      .map(item => ({
        ingredient: item,
        similarity: calculateSimilarity(detected, item)
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

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 0.8) return 'text-green-700 bg-green-50 border-green-200';
    if (similarity >= 0.6) return 'text-blue-700 bg-blue-50 border-blue-200';
    return 'text-orange-700 bg-orange-50 border-orange-200';
  };

  const getSimilarityLabel = (similarity: number) => {
    if (similarity >= 0.8) return 'Sangat Cocok';
    if (similarity >= 0.6) return 'Cocok';
    return 'Cukup Cocok';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <HeaderLogo onClick={onBack} />
          <nav className="flex gap-6">
            <span className="text-blue-600 text-sm" style={{ fontWeight: 600 }}>Demo Sistem</span>
            <button onClick={onBack} className="text-gray-500 hover:text-blue-600 text-sm">Beranda</button>
          </nav>
        </div>
      </header>

      <div className="max-w-3xl mx-auto px-6 py-10">
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
            <div className="bg-white border border-gray-200 rounded-lg p-6">
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
          /* Results */
          <div>
            {/* Back + Title */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <p className="text-xs text-gray-400 mb-1">Masakan</p>
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
                </div>
              </div>

              {/* Nutrisi table */}
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
                      <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.energy} KKal</td>
                      <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.protein}g</td>
                      <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.fat}g</td>
                      <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.carbs}g</td>
                      <td className="pt-2 text-gray-900" style={{ fontWeight: 500 }}>{detectedIngredient?.texture}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            {/* Recommendations */}
            <div className="mb-4">
              <h2 className="text-gray-900 mb-1" style={{ fontSize: '16px', fontWeight: 600 }}>Rekomendasi Pengganti</h2>
              <p className="text-xs text-gray-400">Top 5 bahan dengan similarity score tertinggi</p>
            </div>

            <div className="space-y-3">
              {recommendations.map((rec, index) => (
                <div
                  key={rec.ingredient.id}
                  className="bg-white border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
                >
                  {/* Top row: rank, name, score */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-baseline gap-2">
                      <span className="text-sm text-gray-400" style={{ fontWeight: 600 }}>{index + 1}.</span>
                      <div>
                        <span className="text-gray-900" style={{ fontSize: '15px', fontWeight: 600 }}>{rec.ingredient.name}</span>
                        <span className="text-xs text-gray-400 ml-2">{rec.ingredient.category}</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs px-2 py-0.5 rounded border ${getSimilarityColor(rec.similarity)}`} style={{ fontWeight: 500 }}>
                        {getSimilarityLabel(rec.similarity)}
                      </span>
                      <span className="text-sm text-gray-900 tabular-nums" style={{ fontWeight: 600 }}>
                        {(rec.similarity * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  {/* Nutrisi comparison */}
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
                          <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.energy} KKal</td>
                          <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.protein}g</td>
                          <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.fat}g</td>
                          <td className="pt-1.5 pr-4 text-gray-700">{rec.ingredient.carbs}g</td>
                          <td className="pt-1.5 text-gray-700">{rec.ingredient.texture}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
