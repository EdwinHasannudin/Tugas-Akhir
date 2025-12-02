import pandas as pd
import re
from collections import defaultdict

def classify_food_item(name):
    """
    Klasifikasi makanan berdasarkan nama untuk menentukan texture dan kategori
    """
    name_lower = re.sub(r'[-_/]', ' ', name.lower())  # Normalisasi
    
    # --- Prioritas kategori & texture (spesifik dulu baru umum)
    CATEGORY_PRIORITY = [
        'telur', 'susu', 'minyak/lemak', 'konfeksioneri',
        'bumbu_dan_rempah', 'daging', 'kacang_kacangan',
        'sayuran', 'buah', 'serelia', 'umbi_berpati', 'lainnya'
    ]

    TEXTURE_PRIORITY = ['cair', 'kental', 'lembut', 'padat', 'renyah', 'bubuk', 'netral']

    # Dictionary untuk mapping texture berdasarkan keywords
    texture_keywords = {
        'padat': ['daging', 'ikan', 'ayam', 'sapi', 'kambing', 'dendeng', 'anggur', 'arrowroot', 'kandis',
                  'asam payak', 'bagea', 'beef', 'biji', 'brem', 'baligo', 'batang', 'rotan', 'rukam', 
                  'bungkil', 'cakalang', 'cantel', 'cue', 'hangop', 'jahe', 'jampang', 'jawawut', 'lobak',
                  'karawila', 'kemiri', 'kenari', 'ketapang', 'kluwek', 'geplak', 'lapis', 'sente', 'uwi', 
                  'beras', 'bit', 'oncom', 'gadung', 'jagung', 'jantung', 'kaburan', 'kentang', 'keribang', 
                  'rebung', 'kunyit', 'lepok/ubi', 'terasi', 'ubi', 'wortel', 'babat', 'batatas', 'bebek', 
                  'komba', 'boros', 'buah merah', 'ruruhi', 'gatot', 'permen', 'geblek', 'gembili', 'gula', 
                  'kapurung', 'kelapa hutan', 'ketela', 'ketumbar', 'kranji', 'kundur', 'labu', 'cengkeh', 
                  'cumi', 'kabuto', 'kawista', 'kerbau', 'lokan', 'melinjo', 'takwa', 'talas', 'udang'],
        'lembut': ['haruwan', 'bubur', 'kukus', 'rebus', 'nasi', 'alpukat', 'arbei', 'ares', 'arwan', 'es',
                   'bawang', 'betok', 'botok', 'bakpia', 'bakung', 'bantal', 'barongko', 'atung', 'negri', 
                   'nona', 'cammetutu', 'cempedak', 'fillet', 'kelewih', 'kesemek', 'kwaci', 'selat',
                   'rajungan', 'sawo', 'tempoya', 'tempuyak', 'mentega', 'ampas', 'daun', 'daun ubi',
                   'getuk', 'gudeg', 'mie', 'kangkung', 'kakap', 'keju', 'ketoprak', 'krim', 'kepiting', 
                   'mi', 'brongkos', 'nanas', 'roti', 'sagu', 'sukun', 'bayam', 'tahu', 'batar', 'bihun', 
                   'bika', 'naga', 'tuppa', 'kelor', 'bunga', 'buntil', 'tape', 'carica', 'duku', 'durian', 
                   'duwet', 'embacang', 'gambas', 'gurandil', 'jali', 'jamur', 'kambose', 'kaparende', 
                   'kapusa', 'kelepon', 'kemang', 'kerang', 'ketan', 'kokosan', 'kulit melinjo', 'kwark', 
                   'turi', 'lamtoro', 'lantar', 'lema', 'lontar', 'makaroni', 'mangga', 'manggis', 
                   'margarin', 'masekat', 'matoa', 'melon', 'menteng', 'misoa', 'nangka', 'oyek', 'papeda', 
                   'pepaya', 'pisang', 'terong', 'terung', 'pulut', 'putu', 'rambutan', 'sardines', 
                   'tapai', 'serimping', 'sirsak', 'spaghetti', 'srikaya', 'suweg', 'tiwul', 'tomat', 
                   'waluh', 'yangko'],
        'cair': ['sop', 'santan', 'sayur ', 'cuka', 'air', 'gulai', 'jeruk', 'lemon', 'lemonade', 'telur',
                 'leunca buah', 'rujak', 'semangka', 'susu', 'seduh', 'teh', 'tebu'],
        'kental': ['kental', 'kecap', 'madu', 'rusip', 'taoco', 'yoghurt', 'sirup', 'selai', 'melase', 
                   'petis', 'saos', 'tauco', 'bekasang', 'minyak', 'tauji'],
        'renyah': ['akar tonjong', 'anyang', 'kerupuk', 'keripik', 'rempeyek', 'apel', 'emping', 'biskuit', 
                   'aletoge', 'andewi', 'bengkuang', 'biwah', 'bakwan', 'beberuk', 'belimbing', 'kom', 
                   'cabai', 'kelenting', 'eceng', 'enting', 'gatep', 'jengkol', 'jotang', 'kabau', 'komak',
                   'kacang', 'koro','kalakai', 'kadada', 'kapri', 'kecombrang', 'keremes', 'kerokot',  
                   'gemblong', 'genjer', 'krokot', 'nopia', 'paria', 'pete', 'peterseli', 'rimbang', 
                   'tekokak', 'toge', 'wijen', 'widaran', 'buncis', 'caisin', 'encung', 'gandaria', 'paku',
                   'ganyong', 'jambu', 'jambu air', 'selada air', 'selada', 'karedok', 'kecipir', 
                   'ketimun', 'markisa', 'mostarda', 'pastel', 'salak', 'sawi', 'seledri', 'taoge', 'tempe', 
                   'teri balado', 'kedondong', 'bunga pepaya', 'cap cai', 'erbis', 'japilus', 'kool', 
                   'kucai', 'laksa', 'rebon'],
        'bubuk':  ['tepung ', 'bubuk', 'serbuk', 'kopi', 'coklat bubuk', 'koya', 'maizena', 'merica']
    }
    
    # Dictionary untuk mapping kategori berdasarkan keywords
    category_keywords = {
        'serelia': ['beras', 'cantel', 'jagung', 'jali', 'jawawut', 'jampang', 'nasi', 'tapai', 'tepung',
                    'bihun', 'ketupat', 'ketan', 'maizena', 'mi', 'makaroni', 'misoa', 'roti', 'apem', 
                    'biskuit', 'bakpia', 'bakwan', 'bantal', 'batar daan', 'bika', 'brem', 'bubur', 
                    'cake tape', 'dodol', 'gemblong', 'gendar', 'intip', 'japilus', 'kambose', 'kapusa',
                    'kelepon', 'kue', 'ketoprak', 'koya', 'laksa', 'lapis legit', 'putu mayang', 'lupis',
                    'martabak', 'masekat', 'mie', 'nopia', 'onde-onde', 'pastel', 'pulut', 'pundut',
                    'putri selat', 'renggi', 'sarimuka', 'spaghetti', 'suwir-suwir', 'tipa-tipa', 'wajit',
                    'widaran', 'wingko', 'yangko'],
        'umbi_berpati': ['arrowroot', 'batatas', 'belitung', 'bengkuang', 'bentul', 'gadeng/gadung', 
                         'gadung', 'ganyong', 'gembili', 'hofa/ubi', 'kentang', 'keribang', 'ketela', 
                         'lepok/ubi', 'sagu', 'sente', 'talas', 'umbi uwi', 'uwi', 'ubi', 'suweg', 
                         'bagea', 'biji', 'Cassavastick', 'ceriping', 'gatot', 'getuk', 'geblek', 
                         'gurandil', 'kabuto', 'kapurung', 'kecimpring', 'keremes', 'keripik', 'kerupuk', 
                         'oyek', 'papeda', 'rasbi', 'rasi', 'serimping', 'tiwul'],
        'kacang_kacangan': ['kacang', 'kenari', 'komak', 'koro', 'lamtoro', 'wijen', 'ampas', 'pepea',
                            'bungkil', 'emping', 'enting-enting', 'geplak', 'kembang', 'kwaci', 'oncom', 
                            'tempe', 'melinjo', 'tahu', 'lebui', 'kedelai', 'takwa', 'tauco', 'taoco',
                            'tauji'],
        'sayuran': ['bayam', 'kangkung', 'wortel', 'brokoli', 'kubis', 'sawi', 'selada', 'daun', 'sayur', 
                    'tomat', 'akar tonjong', 'aletoge', 'andaliman', 'andewi', 'bakung', 'buah kelor', 
                    'buah merah', 'bit', 'baligo', 'batang tading', 'gembili', 'buncis', 'bunga', 'cabai',                    
                    'caisin', 'daun pepaya', 'eceng gondok', 'gambas', 'jamur', 'jengkol', 'jotang',
                    'kalakai', 'kapri', 'karawila', 'karedok', 'kelewih', 'turi', 'kerokot', 'polong', 
                    'kool', 'kool kembang','genjer', 'kabau', 'kucai', 'krokot', 'kundur', 'botok', 'lobak', 
                    'lumai/leunca', 'kecipir', 'paria', 'pe-cay', 'pepare', 'pete', 'purundawa', 
                    'putri malu', 'rimbang', 'seledri', 'taoge', 'tekokak', 'terong', 'terung', 'toge', 
                    'umbut', 'singkah', 'jantung pisang', 'kacang mekah', 'kacang panjang', 
                    'kacang ranti polong', 'kecombrang', 'kembang turi', 'ketimun', 'labu', 'lantar', 
                    'peterseli', 'tebu', 'arwan sirsir', 'beberuk', 'buntil', 'cammetutu', 'gado-gado', 
                    'gudeg', 'gulai pakis', 'gulai pliek', 'kadada', 'kotiu', 'rebung', 'lilin', 
                    'olah-olah', 'paku', 'rujak', 'shabu-shabu', 'tinira', 'waluh', 'woku'],
        'buah': ['apel', 'jeruk', 'pisang', 'mangga', 'anggur', 'pepaya', 'semangka', 'durian', 'nanas', 
                 'duku', 'alpukat', 'belimbing', 'buah', 'arbei', 'asam masak', 'biwah', 
                 'cempedak', 'duwet', 'gandaria', 'gatep', 'kawista', 'kelapa', 'kedondong', 'kemang', 
                 'kesemek', 'ketapang', 'kokosan', 'jambu', 'kranji', 'langsat', 'leci', 'lemon', 'limau', 
                 'longan', 'matoa', 'mengkudu', 'murbei', 'lontar', 'manggis', 'markisa', 'melon', 
                 'menteng', 'nangka', 'rambutan', 'salak', 'sawo', 'sirsak', 'sukun', 'srikaya', 
                 'abon haruwan', 'carica', 'embacang', 'encung', 'erbis', 'pala', 'purut', 'barongko'],
        'daging': ['daging', 'sapi', 'ayam', 'kambing', 'babi', 'domba', 'bebek', 'burung', 'ikan', 
                   'udang', 'cumi', 'kerang', 'hati', 'angsa', 'babat', 'beef', 'belut', 'cakalang', 
                   'kuda', 'cue', 'empal', 'fillet', 'kakap', 'katak', 'keong', 'kepiting', 'kodok', 
                   'kura-kura', 'kerbau', 'lokan', 'otak', 'rajungan', 'sotong', 'tiram', 'anjing', 
                   'ulat sagu', 'ham', 'brongkos', 'bulgogi', 'chicken', 'chikiniku', 'djibokum',
                   'jangang', 'kalio', 'lawar', 'lawara', 'nasu likku', 'oramu', 'paniki', 'pelepah',
                   'rawon', 'sate', 'sie reuboh', 'buntut', 'konro', 'sop saudara', 'soto', 'sukiyaki', 
                   'tedong', 'tinoransak', 'rebon', 'rusip', 'rebung laut', 'sardines', 'teripang',
                   'betok', 'gete', 'gulai asam keueung', 'gulau keumamah', 'jambal', 'jukku', 'kaholeo',
                   'parede', 'pempek', 'lele', 'pinda', 'pindang', 'sepi', 'bandeng', 'tekwan', 'teri'],
        'telur': ['telur'],
        'susu': ['susu', 'es krim', 'keju', 'kwark', 'hangop', 'yoghurt', ' kerbau', ' sapi'],
        'minyak/lemak': ['lemak', 'minyak', 'mentega', 'margarin', 'santan'],
        'konfeksioneri': ['coklat', 'permen', 'gula', 'jam selai', 'kopi', 'teh', 'madu', 'melase', 
                          'sirup'],
        'bumbu_dan_rempah': ['bawang', 'merica', 'ketumbar', 'jahe', 'kunyit', 'laos', 'sereh', 'cabe',
                             'lada', 'asam kandis', 'asam payak', 'bekasang', 'cengkeh', 'cuka', 'kemiri', 
                             'kluwek', 'asan', 'boros', 'daun salam', 'kecap', 'petis', 'saos tomat',
                             'tempoya', 'tempuyak', 'terasi'],
    }
    
    # --- Hitung skor keyword untuk kategori ---
    cat_scores = defaultdict(int)
    for cat, keywords in category_keywords.items():
        for kw in keywords:
            pattern = r'(?<!\w)' + re.escape(kw) + r'(?!\w)'
            if re.search(pattern, name_lower):
                cat_scores[cat] += 1

    # --- Hitung skor keyword untuk texture ---
    tex_scores = defaultdict(int)
    for tex, keywords in texture_keywords.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw.strip()) + r'(?:\s+\w+)?'
            if re.search(pattern, name_lower):
                tex_scores[tex] += 1

    # --- Tentukan kategori berdasarkan skor & prioritas ---
    if cat_scores:
        best_category = sorted(
            cat_scores.items(),
            key=lambda x: (-x[1], CATEGORY_PRIORITY.index(x[0]) if x[0] in CATEGORY_PRIORITY else 999)
        )[0][0]
    else:
        best_category = 'lainnya'

    # --- Tentukan texture berdasarkan skor & prioritas ---
    if tex_scores:
        best_texture = sorted(
            tex_scores.items(),
            key=lambda x: (-x[1], TEXTURE_PRIORITY.index(x[0]) if x[0] in TEXTURE_PRIORITY else 999)
        )[0][0]
    else:
        best_texture = 'netral'

    # --- Logika khusus untuk konflik umum ---
    if 'susu' in name_lower:
        if 'kental' in name_lower:
            best_texture = 'kental'
        else:
            best_texture = 'cair'
        best_category = 'susu'

    if 'kuah' in name_lower or 'sop' in name_lower or 'jus' in name_lower:
        best_texture = 'cair'

    if 'goreng' in name_lower or 'keripik' in name_lower:
        best_texture = 'renyah'

    if 'bubuk' in name_lower or 'tepung' in name_lower:
        best_texture = 'bubuk'

    if 'kacang' in name_lower and 'telur' in name_lower:
        best_texture = 'renyah'
        best_category = 'kacang_kacangan'

    return best_texture, best_category

def process_nutrition_data(file_path):
    """
    Memproses data nutrisi dan menambahkan kolom texture dan kategori
    """
    # Baca file Excel
    df = pd.read_excel(file_path)
    
    # Tambahkan kolom baru
    df[['texture', 'kategori']] = df['name'].apply(
        lambda x: pd.Series(classify_food_item(x))
    )
    
    # Simpan file dengan kolom baru
    output_file = file_path.replace('.xlsx', '_with_categories_texture.xlsx')
    df.to_excel(output_file, index=False)
    
    print(f"File berhasil diproses dan disimpan sebagai: {output_file}")
    print(f"\nStatistik Kategori:")
    print(df['kategori'].value_counts())
    print(f"\nStatistik Texture:")
    print(df['texture'].value_counts())
    
    return df

# penggunaan
if __name__ == "__main__":
    
    file_path = "nutrition_data.xlsx"
    
    try:
        processed_df = process_nutrition_data(file_path)
        
        # Tampilkan beberapa contoh hasil
        print("\nContoh 5 data pertama dengan kategori dan texture:")
        print(processed_df[['name', 'kategori', 'texture']].head(10))
        
    except FileNotFoundError:
        print("File tidak ditemukan. Pastikan path file benar.")
    except Exception as e:
        print(f"Terjadi error: {e}")