import { Recipe } from '../App';
import { ingredientsDatabase } from './ingredientsData';

const findIngredient = (id: string) => {
  const ingredient = ingredientsDatabase.find(ing => ing.id === id);
  if (!ingredient) {
    // Fallback to a generic ingredient if not found
    return {
      id,
      name: id.replace(/-/g, ' '),
      category: 'lauk',
      energy: 0,
      protein: 0,
      carbs: 0,
      fat: 0,
      texture: 'unknown'
    };
  }
  return ingredient;
};

export const recipeData: Recipe[] = [
  {
    id: 'ayam-goreng',
    name: 'Ayam Goreng',
    image: 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('ayam'), amount: '1 ekor' },
      { ingredient: findIngredient('kangkung'), amount: '200 gram' },
      { ingredient: findIngredient('sawi'), amount: '150 gram' }
    ]
  },
  {
    id: 'ikan-goreng',
    name: 'Ikan Goreng',
    image: 'https://images.unsplash.com/photo-1580959375944-abd7e991f971?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('ikan-mas'), amount: '500 gram' },
      { ingredient: findIngredient('bayam-segar'), amount: '200 gram' },
      { ingredient: findIngredient('kangkung'), amount: '150 gram' }
    ]
  },
  {
    id: 'daging-goreng',
    name: 'Daging Goreng',
    image: 'https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('daging-sapi'), amount: '500 gram' },
      { ingredient: findIngredient('sawi'), amount: '200 gram' },
      { ingredient: findIngredient('kangkung'), amount: '150 gram' }
    ]
  },
  {
    id: 'tumis-kangkung',
    name: 'Tumis Kangkung',
    image: 'https://images.unsplash.com/photo-1604909052743-94e838986d24?w=400',
    category: 'Sayuran',
    ingredients: [
      { ingredient: findIngredient('kangkung'), amount: '500 gram' },
      { ingredient: findIngredient('bayam-segar'), amount: '200 gram' }
    ]
  },
  {
    id: 'tumis-sawi',
    name: 'Tumis Sawi',
    image: 'https://images.unsplash.com/photo-1609986980950-e71182cf4c42?w=400',
    category: 'Sayuran',
    ingredients: [
      { ingredient: findIngredient('sawi'), amount: '500 gram' },
      { ingredient: findIngredient('bayam-segar'), amount: '300 gram' }
    ]
  },
  {
    id: 'daging-sapi-tumis',
    name: 'Daging Sapi Tumis',
    image: 'https://images.unsplash.com/photo-1635048757821-8c9c2e3af76e?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('daging-sapi'), amount: '600 gram' },
      { ingredient: findIngredient('kangkung'), amount: '300 gram' },
      { ingredient: findIngredient('bayam-segar'), amount: '200 gram' }
    ]
  },
  {
    id: 'ikan-mas-pepes',
    name: 'Ikan Mas Pepes',
    image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('ikan-mas-pepes'), amount: '500 gram' },
      { ingredient: findIngredient('sawi'), amount: '200 gram' }
    ]
  },
  {
    id: 'ayam-rebus',
    name: 'Ayam Rebus',
    image: 'https://images.unsplash.com/photo-1598103442097-8b74394b95c6?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('ayam'), amount: '1 ekor' },
      { ingredient: findIngredient('bayam-segar'), amount: '200 gram' },
      { ingredient: findIngredient('kangkung'), amount: '150 gram' }
    ]
  },
  {
    id: 'sayur-tumis',
    name: 'Sayur Tumis',
    image: 'https://images.unsplash.com/photo-1609986980950-e71182cf4c42?w=400',
    category: 'Sayuran',
    ingredients: [
      { ingredient: findIngredient('kangkung'), amount: '300 gram' },
      { ingredient: findIngredient('sawi'), amount: '300 gram' },
      { ingredient: findIngredient('bayam-segar'), amount: '200 gram' }
    ]
  }
];
