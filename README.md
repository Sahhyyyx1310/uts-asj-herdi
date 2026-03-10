# UTS Administrasi Sistem Jaringan (ASJ) - Microservices CRUD

Proyek ini merupakan implementasi arsitektur microservices menggunakan Docker untuk mengelola data pengguna. Sistem ini mengintegrasikan layanan Backend (API), Frontend, Database, dan Object Storage untuk menangani penyimpanan metadata serta file fisik (gambar).

## 🚀 Fitur Utama
- **CRUD Data Pengguna**: Input nama, email, dan alamat.
- **Upload File**: Mengunggah foto profil ke Object Storage.
- **Microservices**: Pemisahan tugas antara database, storage, dan logic aplikasi.
- **Containerization**: Seluruh layanan berjalan di atas Docker Container.

## 📁 Struktur Proyek
```text
uts-asj-edi/
├── app/
│   ├── main.py          # Backend logic (FastAPI)
│   ├── Dockerfile       # Build image untuk service API
│   └── requirements.txt # Library Python
├── frontend/
│   └── index.html       # Tampilan antarmuka pengguna
├── .env                 # Konfigurasi database & storage (Environment Variables)
└── docker-compose.yml   # Konfigurasi utama seluruh container

Service,Software,Deskripsi
Frontend,Nginx,Menampilkan UI web di port 80.
Backend,FastAPI,Menangani logic API di port 8080.
Database,PostgreSQL,Menyimpan metadata (DB: uts_asj_db).
Storage,MinIO,Menyimpan file foto (Bucket: tugas-herdi).
