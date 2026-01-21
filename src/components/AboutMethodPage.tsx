import { Logo } from './Logo';
import { Calculator, Database, ChefHat, ArrowRight, Scale, Brain } from 'lucide-react';

interface AboutMethodPageProps {
  onBack: () => void;
  onTryDemo: () => void;
}

export function AboutMethodPage({ onBack, onTryDemo }: AboutMethodPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-green-50">
      {/* Header */}
      <header className="bg-transparent">
        <div className="container mx-auto px-6 py-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button onClick={onBack} className="flex items-center gap-3 hover:opacity-80 transition-opacity text-left">
              <div className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center p-2">
                <Logo />
              </div>
              <div>
                <div className="font-bold text-gray-900 text-lg">Recipe</div>
                <div className="text-sm text-gray-600">Sistem Rekomendasi</div>
              </div>
            </button>
          </div>
          <nav className="flex gap-8">
            <button onClick={onTryDemo} className="text-gray-700 hover:text-blue-600 font-medium transition-colors">Demo Sistem</button>
            <button className="text-blue-600 font-semibold">Tentang Metode</button>
          </nav>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12 max-w-5xl">
        {/* Title Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center p-3 bg-blue-50 rounded-full mb-6">
            <Brain className="w-6 h-6 text-blue-600 mr-2" />
            <span className="text-blue-700 font-semibold">Teknologi Dibalik Layar</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight">
            Bagaimana Sistem Kami<br />
            <span className="text-blue-600">Menemukan Pengganti Terbaik?</span>
          </h1>
          <p className="text-gray-600 text-lg max-w-3xl mx-auto">
            Kami menggunakan pendekatan ilmiah dengan metode <span className="font-semibold text-gray-900">Content-Based Filtering</span> dan algoritma <span className="font-semibold text-gray-900">Cosine Similarity</span> untuk memastikan bahan pengganti yang direkomendasikan benar-benar sesuai dengan kebutuhan masakan Anda.
          </p>
        </div>

        {/* Feature Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-shadow border border-gray-100">
            <div className="w-14 h-14 bg-orange-100 rounded-2xl flex items-center justify-center mb-6">
              <Database className="w-7 h-7 text-orange-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Database Komprehensif</h3>
            <p className="text-gray-600 leading-relaxed">
              Sistem kami memiliki database lengkap yang mencakup profil nutrisi mendetail: Energi, Protein, Lemak, Karbohidrat, serta karakteristik fisik seperti Tekstur.
            </p>
          </div>

          <div className="bg-white p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-shadow border border-gray-100">
            <div className="w-14 h-14 bg-blue-100 rounded-2xl flex items-center justify-center mb-6">
              <Scale className="w-7 h-7 text-blue-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Analisis Vektor Nutrisi</h3>
            <p className="text-gray-600 leading-relaxed">
              Setiap bahan direpresentasikan sebagai vektor multi-dimensi. Kami membandingkan jarak dan sudut antar vektor untuk menentukan tingkat kemiripan karakteristik.
            </p>
          </div>

          <div className="bg-white p-8 rounded-3xl shadow-xl hover:shadow-2xl transition-shadow border border-gray-100">
            <div className="w-14 h-14 bg-green-100 rounded-2xl flex items-center justify-center mb-6">
              <Calculator className="w-7 h-7 text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Algoritma Cosine Similarity</h3>
            <p className="text-gray-600 leading-relaxed">
              Perhitungan matematis presisi yang menghasilkan skor kemiripan 0-100%, memastikan rekomendasi yang objektif dan akurat secara ilmiah.
            </p>
          </div>
        </div>

        {/* Deep Dive Section */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden mb-16">
          <div className="p-10 md:p-12">
            <div className="flex flex-col md:flex-row gap-12 items-center">
              <div className="flex-1">
                <h2 className="text-3xl font-bold text-gray-900 mb-6">Parameter Analisis</h2>
                <div className="space-y-4">
                  {[
                    { label: 'Kandungan Energi (KKal)', desc: 'Memastikan asupan kalori yang setara' },
                    { label: 'Makronutrisi (Protein, Lemak, Karbo)', desc: 'Menjaga keseimbangan gizi resep' },
                    { label: 'Tekstur Bahan', desc: 'Penting untuk mouthfeel dan hasil masakan' },
                    { label: 'Kategori Bahan', desc: 'Menjaga kesesuaian jenis (Sayur, Daging, dll)' }
                  ].map((item, idx) => (
                    <div key={idx} className="flex items-start gap-4">
                      <div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center mt-1 flex-shrink-0">
                        <span className="text-blue-600 text-sm font-bold">{idx + 1}</span>
                      </div>
                      <div>
                        <h4 className="font-bold text-gray-900">{item.label}</h4>
                        <p className="text-sm text-gray-600">{item.desc}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="flex-1 bg-gray-50 rounded-2xl p-8 border border-gray-100">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <Calculator className="w-5 h-5 text-gray-500" />
                  Visualisasi Perhitungan
                </h3>
                <div className="space-y-3 font-mono text-sm">
                  <div className="bg-white p-3 rounded-lg border border-gray-200 shadow-sm">
                    <div className="text-xs text-gray-500 mb-1">Vector A (Bahan Asli)</div>
                    <div className="text-blue-600 font-bold">[120, 15, 5, 20]</div>
                  </div>
                  <div className="flex justify-center text-gray-400">vs</div>
                  <div className="bg-white p-3 rounded-lg border border-gray-200 shadow-sm">
                    <div className="text-xs text-gray-500 mb-1">Vector B (Kandidat)</div>
                    <div className="text-green-600 font-bold">[110, 14, 6, 18]</div>
                  </div>
                  <div className="border-t border-gray-200 my-2"></div>
                  <div className="bg-blue-50 p-3 rounded-lg flex justify-between items-center">
                    <span className="text-blue-900 font-semibold">Similarity Score:</span>
                    <span className="text-blue-600 font-bold text-lg">98.5%</span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-4 text-center">
                  *Contoh penyederhanaan perhitungan vektor
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Siap Mencoba Sistemnya?</h2>
          <button 
            onClick={onTryDemo}
            className="px-10 py-4 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all font-semibold shadow-lg hover:shadow-xl inline-flex items-center gap-3 text-lg"
          >
            <ChefHat className="w-6 h-6" />
            Coba Demo Sekarang
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
