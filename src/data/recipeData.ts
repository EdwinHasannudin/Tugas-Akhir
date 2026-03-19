import { Recipe, Ingredient } from '../App';
import { ingredientsDatabase } from './ingredientsData';

const getValidIngredients = (ingredientsReq: {id: string, amount: string}[]) => {
  const result: {ingredient: Ingredient, amount: string}[] = [];
  for (const req of ingredientsReq) {
    // Mapping ID lama ke ID baru jika diperlukan
    let searchId = req.id;
    if (searchId === 'telur') searchId = 'telur-ayam';
    if (searchId === 'tempe') searchId = 'tempe-pasar';
    
    const ingredient = ingredientsDatabase.find(ing => ing.id === searchId);
    if (ingredient) {
      result.push({ ingredient, amount: req.amount });
    } else {
      console.warn(`Ingredient ${searchId} tidak ditemukan di database, melewatkan bahan ini. Hubungi admin jika ini adalah kesalahan.`);
    }
  }
  return result;
};

export const recipeData: Recipe[] = [
  {
    id: 'nasi-goreng',
    name: 'Nasi Goreng',
    image: 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400',
    category: 'Makanan Utama',
    ingredients: getValidIngredients([
      { id: 'nasi', amount: '2 piring' },
      { id: 'ayam', amount: '200 gram' },
      { id: 'telur', amount: '2 butir' },
      { id: 'bawang-merah', amount: '5 siung' },
      { id: 'bawang-putih', amount: '3 siung' },
      { id: 'sawi', amount: '100 gram' }
    ])
  },
  {
    id: 'rendang',
    name: 'Rendang',
    image: 'https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?w=400',
    category: 'Makanan Utama',
    ingredients: getValidIngredients([
      { id: 'daging-sapi', amount: '500 gram' },
      { id: 'santan', amount: '500 ml' },
      { id: 'bawang-merah', amount: '10 siung' },
      { id: 'bawang-putih', amount: '6 siung' },
      { id: 'jahe', amount: '2 cm' },
      { id: 'lengkuas', amount: '3 cm' },
      { id: 'kunyit', amount: '2 cm' }
    ])
  },
  {
    id: 'gado-gado',
    name: 'Gado-gado',
    image: 'https://images.unsplash.com/photo-1591241841680-45646d28e34d?w=400',
    category: 'Salad',
    ingredients: getValidIngredients([
      { id: 'kangkung', amount: '1 ikat' },
      { id: 'bayam', amount: '1 ikat' },
      { id: 'kol', amount: '1/4 buah' },
      { id: 'kentang', amount: '2 buah' },
      { id: 'tahu', amount: '3 potong' },
      { id: 'tempe', amount: '2 potong' },
      { id: 'kacang-tanah', amount: '200 gram' },
      { id: 'telur', amount: '2 butir' }
    ])
  },
  {
    id: 'soto-ayam',
    name: 'Soto Ayam',
    image: 'https://images.unsplash.com/photo-1588029288028-e075801b2c5c?w=400',
    category: 'Sup',
    ingredients: getValidIngredients([
      { id: 'ayam', amount: '500 gram' },
      { id: 'mie', amount: '200 gram' },
      { id: 'kentang', amount: '2 buah' },
      { id: 'bawang-merah', amount: '8 siung' },
      { id: 'bawang-putih', amount: '4 siung' },
      { id: 'jahe', amount: '2 cm' },
      { id: 'kunyit', amount: '2 cm' }
    ])
  },
  {
    id: 'ayam-goreng',
    name: 'Ayam Goreng',
    image: 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400',
    category: 'Makanan Utama',
    ingredients: getValidIngredients([
      { id: 'ayam', amount: '1 ekor' },
      { id: 'bawang-merah', amount: '6 siung' },
      { id: 'bawang-putih', amount: '4 siung' },
      { id: 'kunyit', amount: '2 cm' },
      { id: 'jahe', amount: '1 cm' },
      { id: 'minyak-sayur', amount: '500 ml' }
    ])
  },
  {
    id: 'tempe-goreng',
    name: 'Tempe Goreng',
    image: 'https://images.unsplash.com/photo-1623653387945-2fd25214f8fc?w=400',
    category: 'Lauk',
    ingredients: getValidIngredients([
      { id: 'tempe', amount: '300 gram' },
      { id: 'bawang-putih', amount: '3 siung' },
      { id: 'kunyit', amount: '1 cm' },
      { id: 'minyak-sayur', amount: '300 ml' }
    ])
  },
  {
    id: 'tumis-kangkung',
    name: 'Tumis Kangkung',
    image: 'https://images.unsplash.com/photo-1604909052743-94e838986d24?w=400',
    category: 'Sayuran',
    ingredients: getValidIngredients([
      { id: 'kangkung', amount: '2 ikat' },
      { id: 'bawang-merah', amount: '5 siung' },
      { id: 'bawang-putih', amount: '3 siung' },
      { id: 'minyak-sayur', amount: '2 sdm' }
    ])
  },
  {
    id: 'cap-cay',
    name: 'Cap Cay',
    image: 'https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400',
    category: 'Sayuran',
    ingredients: getValidIngredients([
      { id: 'sawi', amount: '200 gram' },
      { id: 'wortel', amount: '1 buah' },
      { id: 'kol', amount: '1/4 buah' },
      { id: 'buncis', amount: '100 gram' },
      { id: 'jamur', amount: '100 gram' },
      { id: 'udang', amount: '150 gram' },
      { id: 'bawang-putih', amount: '4 siung' }
    ])
  }
].filter(recipe => recipe.ingredients.length > 0);
