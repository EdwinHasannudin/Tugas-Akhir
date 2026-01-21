import { Recipe } from '../App';
import { ingredientsDatabase } from './ingredientsData';

const findIngredient = (id: string) => {
  const ingredient = ingredientsDatabase.find(ing => ing.id === id);
  if (!ingredient) throw new Error(`Ingredient ${id} not found`);
  return ingredient;
};

export const recipeData: Recipe[] = [
  {
    id: 'nasi-goreng',
    name: 'Nasi Goreng',
    image: 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('nasi'), amount: '2 piring' },
      { ingredient: findIngredient('ayam'), amount: '200 gram' },
      { ingredient: findIngredient('telur'), amount: '2 butir' },
      { ingredient: findIngredient('bawang-merah'), amount: '5 siung' },
      { ingredient: findIngredient('bawang-putih'), amount: '3 siung' },
      { ingredient: findIngredient('sawi'), amount: '100 gram' }
    ]
  },
  {
    id: 'rendang',
    name: 'Rendang',
    image: 'https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('daging-sapi'), amount: '500 gram' },
      { ingredient: findIngredient('santan'), amount: '500 ml' },
      { ingredient: findIngredient('bawang-merah'), amount: '10 siung' },
      { ingredient: findIngredient('bawang-putih'), amount: '6 siung' },
      { ingredient: findIngredient('jahe'), amount: '2 cm' },
      { ingredient: findIngredient('lengkuas'), amount: '3 cm' },
      { ingredient: findIngredient('kunyit'), amount: '2 cm' }
    ]
  },
  {
    id: 'gado-gado',
    name: 'Gado-gado',
    image: 'https://images.unsplash.com/photo-1591241841680-45646d28e34d?w=400',
    category: 'Salad',
    ingredients: [
      { ingredient: findIngredient('kangkung'), amount: '1 ikat' },
      { ingredient: findIngredient('bayam'), amount: '1 ikat' },
      { ingredient: findIngredient('kol'), amount: '1/4 buah' },
      { ingredient: findIngredient('kentang'), amount: '2 buah' },
      { ingredient: findIngredient('tahu'), amount: '3 potong' },
      { ingredient: findIngredient('tempe'), amount: '2 potong' },
      { ingredient: findIngredient('kacang-tanah'), amount: '200 gram' },
      { ingredient: findIngredient('telur'), amount: '2 butir' }
    ]
  },
  {
    id: 'soto-ayam',
    name: 'Soto Ayam',
    image: 'https://images.unsplash.com/photo-1588029288028-e075801b2c5c?w=400',
    category: 'Sup',
    ingredients: [
      { ingredient: findIngredient('ayam'), amount: '500 gram' },
      { ingredient: findIngredient('mie'), amount: '200 gram' },
      { ingredient: findIngredient('kentang'), amount: '2 buah' },
      { ingredient: findIngredient('bawang-merah'), amount: '8 siung' },
      { ingredient: findIngredient('bawang-putih'), amount: '4 siung' },
      { ingredient: findIngredient('jahe'), amount: '2 cm' },
      { ingredient: findIngredient('kunyit'), amount: '2 cm' }
    ]
  },
  {
    id: 'ayam-goreng',
    name: 'Ayam Goreng',
    image: 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400',
    category: 'Makanan Utama',
    ingredients: [
      { ingredient: findIngredient('ayam'), amount: '1 ekor' },
      { ingredient: findIngredient('bawang-merah'), amount: '6 siung' },
      { ingredient: findIngredient('bawang-putih'), amount: '4 siung' },
      { ingredient: findIngredient('kunyit'), amount: '2 cm' },
      { ingredient: findIngredient('jahe'), amount: '1 cm' },
      { ingredient: findIngredient('minyak-sayur'), amount: '500 ml' }
    ]
  },
  {
    id: 'tempe-goreng',
    name: 'Tempe Goreng',
    image: 'https://images.unsplash.com/photo-1623653387945-2fd25214f8fc?w=400',
    category: 'Lauk',
    ingredients: [
      { ingredient: findIngredient('tempe'), amount: '300 gram' },
      { ingredient: findIngredient('bawang-putih'), amount: '3 siung' },
      { ingredient: findIngredient('kunyit'), amount: '1 cm' },
      { ingredient: findIngredient('minyak-sayur'), amount: '300 ml' }
    ]
  },
  {
    id: 'tumis-kangkung',
    name: 'Tumis Kangkung',
    image: 'https://images.unsplash.com/photo-1604909052743-94e838986d24?w=400',
    category: 'Sayuran',
    ingredients: [
      { ingredient: findIngredient('kangkung'), amount: '2 ikat' },
      { ingredient: findIngredient('bawang-merah'), amount: '5 siung' },
      { ingredient: findIngredient('bawang-putih'), amount: '3 siung' },
      { ingredient: findIngredient('minyak-sayur'), amount: '2 sdm' }
    ]
  },
  {
    id: 'cap-cay',
    name: 'Cap Cay',
    image: 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400',
    category: 'Sayuran',
    ingredients: [
      { ingredient: findIngredient('sawi'), amount: '200 gram' },
      { ingredient: findIngredient('wortel'), amount: '1 buah' },
      { ingredient: findIngredient('kol'), amount: '1/4 buah' },
      { ingredient: findIngredient('buncis'), amount: '100 gram' },
      { ingredient: findIngredient('jamur'), amount: '100 gram' },
      { ingredient: findIngredient('udang'), amount: '150 gram' },
      { ingredient: findIngredient('bawang-putih'), amount: '4 siung' }
    ]
  }
];
