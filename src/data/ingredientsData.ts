import { Ingredient } from '../App';

export const ingredientsDatabase: Ingredient[] = [
  // Protein Hewani
  {
    id: 'ayam',
    name: 'Ayam',
    category: 'Protein Hewani',
    energy: 239,
    protein: 27,
    carbs: 0,
    fat: 14,
    fiber: 0,
    texture: 'Lembut',
    flavor: 'Gurih'
  },
  {
    id: 'daging-sapi',
    name: 'Daging Sapi',
    category: 'Protein Hewani',
    energy: 250,
    protein: 26,
    carbs: 0,
    fat: 17,
    fiber: 0,
    texture: 'Kenyal',
    flavor: 'Gurih'
  },
  {
    id: 'bebek',
    name: 'Bebek',
    category: 'Protein Hewani',
    energy: 337,
    protein: 19,
    carbs: 0,
    fat: 28,
    fiber: 0,
    texture: 'Kenyal',
    flavor: 'Gurih'
  },
  {
    id: 'kelinci',
    name: 'Kelinci',
    category: 'Protein Hewani',
    energy: 173,
    protein: 33,
    carbs: 0,
    fat: 3,
    fiber: 0,
    texture: 'Lembut',
    flavor: 'Gurih'
  },
  {
    id: 'kambing',
    name: 'Kambing',
    category: 'Protein Hewani',
    energy: 143,
    protein: 27,
    carbs: 0,
    fat: 3,
    fiber: 0,
    texture: 'Kenyal',
    flavor: 'Gurih'
  },
  {
    id: 'ikan',
    name: 'Ikan',
    category: 'Protein Hewani',
    energy: 206,
    protein: 22,
    carbs: 0,
    fat: 5,
    fiber: 0,
    texture: 'Lembut',
    flavor: 'Gurih'
  },
  {
    id: 'udang',
    name: 'Udang',
    category: 'Protein Hewani',
    energy: 99,
    protein: 24,
    carbs: 1,
    fat: 1,
    fiber: 0,
    texture: 'Kenyal',
    flavor: 'Gurih'
  },
  {
    id: 'telur',
    name: 'Telur',
    category: 'Protein Hewani',
    energy: 155,
    protein: 13,
    carbs: 1,
    fat: 11,
    fiber: 0,
    texture: 'Lembut',
    flavor: 'Gurih'
  },

  // Protein Nabati
  {
    id: 'tahu',
    name: 'Tahu',
    category: 'Protein Nabati',
    energy: 76,
    protein: 8,
    carbs: 2,
    fat: 5,
    fiber: 1,
    texture: 'Lembut',
    flavor: 'Tawar'
  },
  {
    id: 'tempe',
    name: 'Tempe',
    category: 'Protein Nabati',
    energy: 193,
    protein: 19,
    carbs: 9,
    fat: 11,
    fiber: 7,
    texture: 'Padat',
    flavor: 'Gurih'
  },
  {
    id: 'kacang-merah',
    name: 'Kacang Merah',
    category: 'Protein Nabati',
    energy: 127,
    protein: 8,
    carbs: 22,
    fat: 1,
    fiber: 7,
    texture: 'Lembut',
    flavor: 'Tawar'
  },
  {
    id: 'jamur',
    name: 'Jamur',
    category: 'Protein Nabati',
    energy: 22,
    protein: 3,
    carbs: 3,
    fat: 0,
    fiber: 1,
    texture: 'Lembut',
    flavor: 'Umami'
  },

  // Karbohidrat
  {
    id: 'nasi',
    name: 'Nasi',
    category: 'Karbohidrat',
    energy: 130,
    protein: 2,
    carbs: 28,
    fat: 0,
    fiber: 0,
    texture: 'Pulen',
    flavor: 'Tawar'
  },
  {
    id: 'kentang',
    name: 'Kentang',
    category: 'Karbohidrat',
    energy: 77,
    protein: 2,
    carbs: 17,
    fat: 0,
    fiber: 2,
    texture: 'Lembut',
    flavor: 'Tawar'
  },
  {
    id: 'mie',
    name: 'Mie',
    category: 'Karbohidrat',
    energy: 138,
    protein: 5,
    carbs: 25,
    fat: 1,
    fiber: 1,
    texture: 'Kenyal',
    flavor: 'Tawar'
  },
  {
    id: 'ubi',
    name: 'Ubi',
    category: 'Karbohidrat',
    energy: 86,
    protein: 1,
    carbs: 20,
    fat: 0,
    fiber: 3,
    texture: 'Lembut',
    flavor: 'Manis'
  },

  // Sayuran
  {
    id: 'kangkung',
    name: 'Kangkung',
    category: 'Sayuran',
    energy: 19,
    protein: 3,
    carbs: 4,
    fat: 0,
    fiber: 2,
    texture: 'Renyah',
    flavor: 'Tawar'
  },
  {
    id: 'bayam',
    name: 'Bayam',
    category: 'Sayuran',
    energy: 23,
    protein: 3,
    carbs: 4,
    fat: 0,
    fiber: 2,
    texture: 'Lembut',
    flavor: 'Tawar'
  },
  {
    id: 'sawi',
    name: 'Sawi',
    category: 'Sayuran',
    energy: 13,
    protein: 2,
    carbs: 3,
    fat: 0,
    fiber: 2,
    texture: 'Renyah',
    flavor: 'Tawar'
  },
  {
    id: 'kol',
    name: 'Kol',
    category: 'Sayuran',
    energy: 25,
    protein: 1,
    carbs: 6,
    fat: 0,
    fiber: 2,
    texture: 'Renyah',
    flavor: 'Tawar'
  },
  {
    id: 'wortel',
    name: 'Wortel',
    category: 'Sayuran',
    energy: 41,
    protein: 1,
    carbs: 10,
    fat: 0,
    fiber: 3,
    texture: 'Renyah',
    flavor: 'Manis'
  },
  {
    id: 'buncis',
    name: 'Buncis',
    category: 'Sayuran',
    energy: 31,
    protein: 2,
    carbs: 7,
    fat: 0,
    fiber: 3,
    texture: 'Renyah',
    flavor: 'Tawar'
  },

  // Bumbu & Rempah
  {
    id: 'bawang-merah',
    name: 'Bawang Merah',
    category: 'Bumbu & Rempah',
    energy: 40,
    protein: 1,
    carbs: 9,
    fat: 0,
    fiber: 1,
    texture: 'Renyah',
    flavor: 'Pedas'
  },
  {
    id: 'bawang-putih',
    name: 'Bawang Putih',
    category: 'Bumbu & Rempah',
    energy: 33,
    protein: 1,
    carbs: 8,
    fat: 0,
    fiber: 1,
    texture: 'Renyah',
    flavor: 'Pedas'
  },
  {
    id: 'jahe',
    name: 'Jahe',
    category: 'Bumbu & Rempah',
    energy: 80,
    protein: 2,
    carbs: 18,
    fat: 1,
    fiber: 2,
    texture: 'Keras',
    flavor: 'Pedas'
  },
  {
    id: 'kunyit',
    name: 'Kunyit',
    category: 'Bumbu & Rempah',
    energy: 312,
    protein: 1,
    carbs: 3,
    fat: 0,
    fiber: 1,
    texture: 'Keras',
    flavor: 'Pahit'
  },
  {
    id: 'lengkuas',
    name: 'Lengkuas',
    category: 'Bumbu & Rempah',
    energy: 71,
    protein: 1,
    carbs: 15,
    fat: 1,
    fiber: 2,
    texture: 'Keras',
    flavor: 'Pedas'
  },
  {
    id: 'kemiri',
    name: 'Kemiri',
    category: 'Bumbu & Rempah',
    energy: 718,
    protein: 8,
    carbs: 13,
    fat: 40,
    fiber: 3,
    texture: 'Keras',
    flavor: 'Gurih'
  },
  {
    id: 'kacang-tanah',
    name: 'Kacang Tanah',
    category: 'Bumbu & Rempah',
    energy: 567,
    protein: 26,
    carbs: 16,
    fat: 49,
    fiber: 8,
    texture: 'Renyah',
    flavor: 'Gurih'
  },

  // Santan & Lemak
  {
    id: 'santan',
    name: 'Santan',
    category: 'Santan & Lemak',
    energy: 230,
    protein: 2,
    carbs: 6,
    fat: 24,
    fiber: 0,
    texture: 'Cair',
    flavor: 'Gurih'
  },
  {
    id: 'susu',
    name: 'Susu',
    category: 'Santan & Lemak',
    energy: 61,
    protein: 3,
    carbs: 5,
    fat: 3,
    fiber: 0,
    texture: 'Cair',
    flavor: 'Gurih'
  },
  {
    id: 'minyak-sayur',
    name: 'Minyak Sayur',
    category: 'Santan & Lemak',
    energy: 884,
    protein: 0,
    carbs: 0,
    fat: 100,
    fiber: 0,
    texture: 'Cair',
    flavor: 'Tawar'
  }
];