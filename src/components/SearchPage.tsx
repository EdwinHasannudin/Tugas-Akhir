import { useState } from 'react';
import { Search, ChefHat, Utensils, ArrowRight } from 'lucide-react';
import { Recipe } from '../App';
import { recipeData } from '../data/recipeData';
import bgImage from '../assets/Background.png';
import { HeaderLogo } from './HeaderLogo';

interface SearchPageProps {
  onSelectRecipe: (recipe: Recipe) => void;
  onDemoSystem: () => void;
}

export function SearchPage({ onSelectRecipe, onDemoSystem }: SearchPageProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredRecipes, setFilteredRecipes] = useState<Recipe[]>([]);
  const [showSearch, setShowSearch] = useState(false);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      const results = recipeData.filter(recipe =>
        recipe.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredRecipes(results);
    } else {
      setFilteredRecipes([]);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  if (!showSearch) {
    return (
      <div className="min-h-screen relative">
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: `url(${bgImage})` }}
        >
          <div className="absolute inset-0 bg-white/85"></div>
        </div>

        {/* Content */}
        <div className="relative z-10">
          {/* Header */}
          <header className="border-b border-gray-200 bg-white/60 backdrop-blur-sm">
            <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
              <HeaderLogo />
              <nav className="flex gap-6">
                <button 
                  onClick={onDemoSystem} 
                  className="text-gray-600 hover:text-blue-600 text-sm"
                >
                  Demo Sistem
                </button>
              </nav>
            </div>
          </header>

          {/* Hero */}
          <div className="max-w-3xl mx-auto px-6 pt-20 pb-16">
            <div className="mb-10">
              <p className="text-sm text-blue-600 mb-3 tracking-wide uppercase">Content Based Filtering</p>
              <h1 className="text-3xl text-gray-900 mb-4 leading-snug" style={{ fontWeight: 700 }}>
                Sistem Rekomendasi<br />Bahan Pengganti Masakan
              </h1>
              <p className="text-gray-500 max-w-lg leading-relaxed" style={{ fontSize: '15px' }}>
                Cari alternatif bahan masakan berdasarkan kesamaan nutrisi, tekstur, dan kategori. 
                Cukup masukkan nama masakan, sistem akan memberikan rekomendasi pengganti yang paling mirip.
              </p>
            </div>

            {/* CTA */}
            <div className="flex flex-wrap gap-3">
              <button
                onClick={onDemoSystem}
                className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center gap-2"
              >
                Coba Demo
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Info Cards */}
          <div className="max-w-3xl mx-auto px-6 pb-20">
            <div className="grid sm:grid-cols-3 gap-4">
              <div className="bg-white border border-gray-200 rounded-lg p-5">
                <div className="w-9 h-9 bg-blue-50 rounded-lg flex items-center justify-center mb-3">
                  <Search className="w-4 h-4 text-blue-600" />
                </div>
                <h3 className="text-gray-900 mb-1" style={{ fontSize: '14px', fontWeight: 600 }}>Deteksi Otomatis</h3>
                <p className="text-gray-500" style={{ fontSize: '13px', lineHeight: '1.5' }}>
                  Bahan utama terdeteksi langsung dari nama masakan yang Anda input
                </p>
              </div>

              <div className="bg-white border border-gray-200 rounded-lg p-5">
                <div className="w-9 h-9 bg-green-50 rounded-lg flex items-center justify-center mb-3">
                  <ChefHat className="w-4 h-4 text-green-600" />
                </div>
                <h3 className="text-gray-900 mb-1" style={{ fontSize: '14px', fontWeight: 600 }}>6 Kriteria</h3>
                <p className="text-gray-500" style={{ fontSize: '13px', lineHeight: '1.5' }}>
                  Energi, protein, lemak, karbohidrat, tekstur, dan kategori bahan
                </p>
              </div>

              <div className="bg-white border border-gray-200 rounded-lg p-5">
                <div className="w-9 h-9 bg-orange-50 rounded-lg flex items-center justify-center mb-3">
                  <Utensils className="w-4 h-4 text-orange-600" />
                </div>
                <h3 className="text-gray-900 mb-1" style={{ fontSize: '14px', fontWeight: 600 }}>Similarity Score</h3>
                <p className="text-gray-500" style={{ fontSize: '13px', lineHeight: '1.5' }}>
                  Weighted Sum untuk menghasilkan skor kemiripan yang akurat
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="flex items-center justify-center mb-4">
          <ChefHat className="w-12 h-12 text-orange-500" />
        </div>
        <h1 className="text-4xl font-bold text-gray-800 mb-3">
          Sistem Rekomendasi Bahan Pengganti
        </h1>
        <p className="text-gray-600 text-lg">
          Content-Based Filtering untuk menemukan alternatif bahan masakan
        </p>
      </div>

      {/* Search Section */}
      <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
        <label className="block text-2xl font-semibold text-gray-800 mb-4 text-center">
          Mau masak apa hari ini?
        </label>
        
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ketik nama masakan (contoh: Nasi Goreng, Rendang, Gado-gado)"
              className="w-full px-5 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-orange-400 text-lg"
            />
            <Search className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
          <button
            onClick={handleSearch}
            className="px-8 py-4 bg-orange-500 text-white rounded-xl hover:bg-orange-600 transition-colors font-semibold shadow-lg hover:shadow-xl"
          >
            Cari
          </button>
        </div>

        {/* Popular Suggestions */}
        <div className="mt-6">
          <p className="text-sm text-gray-500 mb-3">Populer:</p>
          <div className="flex flex-wrap gap-2">
            {['Nasi Goreng', 'Rendang', 'Gado-gado', 'Soto Ayam', 'Ayam Goreng'].map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => {
                  setSearchQuery(suggestion);
                  const results = recipeData.filter(recipe =>
                    recipe.name.toLowerCase().includes(suggestion.toLowerCase())
                  );
                  setFilteredRecipes(results);
                }}
                className="px-4 py-2 bg-orange-50 text-orange-600 rounded-full text-sm hover:bg-orange-100 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Results */}
      {filteredRecipes.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Hasil Pencarian ({filteredRecipes.length})
          </h2>
          
          <div className="grid gap-4">
            {filteredRecipes.map((recipe) => (
              <button
                key={recipe.id}
                onClick={() => onSelectRecipe(recipe)}
                className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all p-6 text-left group"
              >
                <div className="flex items-center gap-4">
                  <img
                    src={recipe.image}
                    alt={recipe.name}
                    className="w-24 h-24 rounded-lg object-cover"
                  />
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-800 mb-2 group-hover:text-orange-600 transition-colors">
                      {recipe.name}
                    </h3>
                    <div className="flex items-center gap-2 text-gray-600">
                      <Utensils className="w-4 h-4" />
                      <span className="text-sm">{recipe.ingredients.length} bahan utama</span>
                      <span className="mx-2">•</span>
                      <span className="text-sm bg-orange-100 text-orange-700 px-3 py-1 rounded-full">
                        {recipe.category}
                      </span>
                    </div>
                  </div>
                  <div className="text-orange-500 group-hover:translate-x-1 transition-transform">
                    <Search className="w-6 h-6" />
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {searchQuery && filteredRecipes.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <Utensils className="w-16 h-16 mx-auto" />
          </div>
          <p className="text-gray-600 text-lg">
            Masakan tidak ditemukan. Coba kata kunci lain!
          </p>
        </div>
      )}
    </div>
  );
}