# 🐳 Panduan Menjalankan dengan Docker

## Prasyarat
- Docker Desktop terinstall di komputer Anda
- Docker Desktop dalam keadaan running

## Cara Menjalankan

### 1️⃣ Mode Development (dengan hot-reload)
Untuk development dengan fitur hot-reload (perubahan code langsung terlihat):

```bash
docker-compose up dev
```

Aplikasi akan berjalan di: **http://localhost:3000**

### 2️⃣ Mode Production
Untuk production build yang sudah dioptimasi:

```bash
docker-compose up prod
```

Aplikasi akan berjalan di: **http://localhost:3000**

## Perintah Docker Lainnya

### Menjalankan di background
```bash
docker-compose up -d dev
```

### Melihat logs
```bash
docker-compose logs -f dev
```

### Menghentikan container
```bash
docker-compose down
```

### Rebuild image (jika ada perubahan dependencies)
```bash
docker-compose build dev
docker-compose up dev
```

### Membersihkan semua container dan image
```bash
docker-compose down --rmi all
```

## Troubleshooting

### Port sudah digunakan
Jika port 3000 sudah digunakan, edit file `docker-compose.yml` dan ubah:
```yaml
ports:
  - "8080:3000"  # Ganti 8080 dengan port yang tersedia
```

### Perubahan code tidak terdeteksi (mode dev)
Pastikan volume mapping sudah benar di `docker-compose.yml` dan restart container:
```bash
docker-compose restart dev
```

### Build gagal
Hapus cache dan rebuild:
```bash
docker-compose build --no-cache dev
docker-compose up dev
```

## Perbedaan Mode Development vs Production

| Fitur | Development | Production |
|-------|-------------|------------|
| Hot-reload | ✅ Ya | ❌ Tidak |
| Ukuran image | Lebih besar | Lebih kecil (optimized) |
| Build time | Cepat | Lebih lama |
| Performance | Normal | Optimized |
| Use case | Coding & testing | Deploy ke server |
