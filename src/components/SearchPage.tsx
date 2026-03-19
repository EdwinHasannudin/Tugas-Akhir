import { useState, KeyboardEvent } from 'react';
import { Search, ChefHat, Utensils, Target, Clock } from 'lucide-react';
import { Recipe } from '../App';
import { recipeData } from '../data/recipeData';
<<<<<<< Updated upstream
import { Logo } from './Logo';
=======
import bgImage from '../assets/Background.png';
import { HeaderLogo } from './HeaderLogo';
>>>>>>> Stashed changes

interface SearchPageProps {
  onSelectRecipe: (recipe: Recipe) => void;
  onDemoSystem: () => void;
  onAboutMethod: () => void;
}

export function SearchPage({ onSelectRecipe, onDemoSystem, onAboutMethod }: SearchPageProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredRecipes, setFilteredRecipes] = useState<Recipe[]>([]);
  const [showSearch, setShowSearch] = useState(false);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      const results = recipeData.filter(recipe =>
        recipe.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setFilteredRecipes(results);
      setShowSearch(true);
    } else {
      setFilteredRecipes([]);
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  if (!showSearch) {
    return (
      <div className="min-h-screen relative">
        {/* Background Image with Overlay */}
        <div 
          className="absolute inset-0 bg-cover bg-center bg-gradient-to-br from-blue-50 to-blue-100"
        >
          <div className="absolute inset-0 bg-white/80 backdrop-blur-md"></div>
        </div>

        {/* Content */}
        <div className="relative z-10">
          {/* Header */}
          <header className="bg-transparent">
            <div className="container mx-auto px-6 py-6 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center p-2">
                  <Logo />
                </div>
                <div>
                  <div className="font-bold text-gray-900 text-lg">Recipe</div>
                  <div className="text-sm text-gray-600">Sistem Rekomendasi</div>
                </div>
              </div>
              <nav className="flex gap-8">
                <button onClick={onDemoSystem} className="text-gray-700 hover:text-blue-600 font-medium">Demo Sistem</button>
                <button onClick={onAboutMethod} className="text-gray-700 hover:text-blue-600 font-medium">Tentang Metode</button>
              </nav>
            </div>
          </header>

          {/* Hero Section */}
          <div className="container mx-auto px-4 py-16 max-w-5xl">
            <div className="text-center mb-12">
              <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
                Sistem Rekomendasi<br />
                <span className="text-blue-600">Bahan Pengganti</span>
              </h1>
              <p className="text-xl text-gray-700 max-w-3xl mx-auto">
                Temukan bahan pengganti terbaik untuk resep masakan Anda menggunakan<br />
                teknologi <span className="text-blue-600 font-semibold">Content Based Filtering</span>
              </p>
            </div>

            {/* Feature Cards */}
            <div className="grid md:grid-cols-2 gap-8 mb-12 max-w-4xl mx-auto">
              <div className="bg-white rounded-3xl shadow-xl p-10 text-center">
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center">
                    <Target className="w-8 h-8 text-white" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Akurat</h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Rekomendasi berdasarkan similarity score dengan tingkat akurasi tinggi
                </p>
              </div>

              <div className="bg-white rounded-3xl shadow-xl p-10 text-center">
                <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
                    <Clock className="w-8 h-8 text-white" />
                  </div>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Instan</h3>
                <p className="text-gray-600 text-lg leading-relaxed">
                  Hasil rekomendasi dalam hitungan detik dengan interface yang mudah
                </p>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-wrap items-center justify-center gap-6">
              <button
                onClick={() => {
                  setShowSearch(true);
                  onDemoSystem();
                }}
                className="px-10 py-4 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all font-semibold shadow-lg hover:shadow-xl flex items-center gap-3 text-lg"
              >
                <Search className="w-5 h-5" />
                Coba Demo Sekarang
              </button>
              <button 
                onClick={onAboutMethod}
                className="px-10 py-4 bg-white text-blue-600 rounded-full hover:bg-gray-50 transition-all font-semibold shadow-lg border-2 border-blue-600 text-lg"
              >
                Pelajari Metode
              </button>
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