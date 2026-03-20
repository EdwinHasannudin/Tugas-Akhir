import { useState } from 'react';
import { Info, Lightbulb, TrendingUp, CheckCircle2 } from 'lucide-react';
import { Recipe, Ingredient } from '../App';
import { ingredientsDatabase } from '../data/ingredientsData';
import { calculateSimilarity } from '../utils/contentBasedFiltering';
import { HeaderLogo } from './HeaderLogo';

interface RecommendationPageProps {
  recipe: Recipe;
  onBack: () => void;
}

export function RecommendationPage({ recipe, onBack }: RecommendationPageProps) {
  const [selectedIngredient, setSelectedIngredient] = useState<Ingredient | null>(null);
  const [recommendations, setRecommendations] = useState<Array<{
    ingredient: Ingredient;
    similarity: number;
    reasons: string[];
  }>>([]);

  const handleSelectIngredient = (ingredient: Ingredient) => {
    setSelectedIngredient(ingredient);
    
    // Calculate recommendations using content-based filtering
    const recs = ingredientsDatabase
      .filter(item => item.id !== ingredient.id)
      .map(item => ({
        ingredient: item,
        similarity: calculateSimilarity(ingredient, item),
        reasons: generateReasons(ingredient, item)
      }))
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, 5);
    
    setRecommendations(recs);
  };

  const generateReasons = (original: Ingredient, substitute: Ingredient): string[] => {
    const reasons: string[] = [];
    
    if (original.category === substitute.category) {
      reasons.push(`Kategori sama: ${substitute.category}`);
    }
    
    if (original.texture === substitute.texture) {
      reasons.push(`Tekstur serupa: ${substitute.texture}`);
    }
    

    const proteinDiff = Math.abs(original.protein - substitute.protein);
    if (proteinDiff < 5) {
      reasons.push('Kandungan protein mirip');
    }
    
    const carbsDiff = Math.abs(original.carbs - substitute.carbs);
    if (carbsDiff < 10) {
      reasons.push('Kandungan karbohidrat serupa');
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
      <header className="bg-white/80 backdrop-blur-md shadow-sm">
        <div className="container mx-auto px-6 py-6 flex items-center justify-between">
          <HeaderLogo onClick={onBack} />
          <nav className="flex gap-8">
            <button className="text-gray-700 hover:text-blue-600 font-medium">Demo Sistem</button>
          </nav>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Recipe Info */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <div className="flex items-start gap-6">
            <img
              src={recipe.image}
              alt={recipe.name}
              className="w-32 h-32 rounded-xl object-cover"
            />
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-800 mb-2">{recipe.name}</h1>
              <span className="inline-block bg-orange-100 text-orange-700 px-4 py-1 rounded-full text-sm font-medium">
                {recipe.category}
              </span>
              <p className="text-gray-600 mt-4">
                Pilih bahan yang ingin diganti untuk melihat rekomendasi pengganti
              </p>
            </div>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Ingredients List */}
          <div>
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Info className="w-6 h-6 text-orange-500" />
                Bahan-bahan Masakan
              </h2>
              
              <div className="space-y-3">
                {recipe.ingredients.map(({ ingredient, amount }) => (
                  <button
                    key={ingredient.id}
                    onClick={() => handleSelectIngredient(ingredient)}
                    className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                      selectedIngredient?.id === ingredient.id
                        ? 'border-orange-500 bg-orange-50 shadow-md'
                        : 'border-gray-200 hover:border-orange-300 hover:bg-orange-50/50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="font-semibold text-gray-800">{ingredient.name}</div>
                        <div className="text-sm text-gray-500 mt-1">{amount}</div>
                        <div className="flex gap-2 mt-2">
                          <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                            {ingredient.category}
                          </span>
                          <span className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                            {ingredient.texture}
                          </span>
                        </div>
                      </div>
                      {selectedIngredient?.id === ingredient.id && (
                        <CheckCircle2 className="w-6 h-6 text-orange-500" />
                      )}
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Recommendations */}
          <div>
            <div className="bg-white rounded-2xl shadow-lg p-6 sticky top-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Lightbulb className="w-6 h-6 text-orange-500" />
                Rekomendasi Pengganti
              </h2>

              {!selectedIngredient ? (
                <div className="text-center py-12">
                  <TrendingUp className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">
                    Pilih bahan dari daftar untuk melihat rekomendasi pengganti
                  </p>
                </div>
              ) : (
                <>
                  <div className="bg-gradient-to-r from-orange-50 to-green-50 rounded-lg p-4 mb-6">
                    <p className="text-sm text-gray-600 mb-1">Mencari pengganti untuk:</p>
                    <p className="font-bold text-gray-800 text-lg">{selectedIngredient.name}</p>
                  </div>

                  <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                    {recommendations.map((rec, index) => (
                      <div
                        key={rec.ingredient.id}
                        className="border-2 border-gray-200 rounded-xl p-4 hover:border-orange-300 transition-all"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1">
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-gray-800 text-lg">
                                {index + 1}. {rec.ingredient.name}
                              </span>
                            </div>
                            <span className="text-xs text-gray-500">{rec.ingredient.category}</span>
                          </div>
                          <div className="text-right">
                            <div className={`text-sm font-bold px-3 py-1 rounded-full ${getSimilarityColor(rec.similarity)}`}>
                              {getSimilarityLabel(rec.similarity)}
                            </div>
                            <div className="text-xs text-gray-500 mt-1">
                              {(rec.similarity * 100).toFixed(0)}% cocok
                            </div>
                          </div>
                        </div>

                        <div className="bg-gray-50 rounded-lg p-3 mb-3">
                          <p className="text-xs font-semibold text-gray-600 mb-2">Alasan Rekomendasi:</p>
                          <ul className="space-y-1">
                            {rec.reasons.map((reason, idx) => (
                              <li key={idx} className="text-xs text-gray-600 flex items-start gap-2">
                                <span className="text-green-500 mt-0.5">✓</span>
                                <span>{reason}</span>
                              </li>
                            ))}
                          </ul>
                        </div>

                        <div className="grid grid-cols-3 gap-2 text-xs">
                          <div className="bg-white rounded p-2 text-center">
                            <div className="text-gray-500">Protein</div>
                            <div className="font-semibold text-gray-800">{rec.ingredient.protein}g</div>
                          </div>
                          <div className="bg-white rounded p-2 text-center">
                            <div className="text-gray-500">Karbo</div>
                            <div className="font-semibold text-gray-800">{rec.ingredient.carbs}g</div>
                          </div>
                          <div className="bg-white rounded p-2 text-center">
                            <div className="text-gray-500">Lemak</div>
                            <div className="font-semibold text-gray-800">{rec.ingredient.fat}g</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}