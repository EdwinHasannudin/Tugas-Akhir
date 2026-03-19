import { useState } from 'react';
import { SearchPage } from './components/SearchPage';
import { RecommendationPage } from './components/RecommendationPage';
import { DemoSystemPage } from './components/DemoSystemPage';
import { AboutMethodPage } from './components/AboutMethodPage';

export interface Ingredient {
  id: string;
  name: string;
  category: string;
  energy: number; // KKal
  protein: number;
  carbs: number;
  fat: number;
  texture: string;
}

export interface Recipe {
  id: string;
  name: string;
  image: string;
  ingredients: {
    ingredient: Ingredient;
    amount: string;
  }[];
  category: string;
}

type ViewMode = 'home' | 'demo' | 'recipe' | 'about';

export default function App() {
  const [viewMode, setViewMode] = useState<ViewMode>('home');
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);

  const handleSelectRecipe = (recipe: Recipe) => {
    setSelectedRecipe(recipe);
    setViewMode('recipe');
  };

  const handleBackToHome = () => {
    setViewMode('home');
    setSelectedRecipe(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50">
      {viewMode === 'home' && (
        <SearchPage 
          onSelectRecipe={handleSelectRecipe}
          onDemoSystem={() => setViewMode('demo')}
          onAboutMethod={() => setViewMode('about')}
        />
      )}
      
      {viewMode === 'demo' && (
        <DemoSystemPage 
          onBack={handleBackToHome}
          onAboutMethod={() => setViewMode('about')}
        />
      )}
      
      {viewMode === 'about' && (
        <AboutMethodPage 
          onBack={handleBackToHome}
          onTryDemo={() => setViewMode('demo')}
        />
      )}
      
      {viewMode === 'recipe' && selectedRecipe && (
        <RecommendationPage 
          recipe={selectedRecipe} 
          onBack={handleBackToHome} 
        />
      )}
    </div>
  );
}