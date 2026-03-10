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

⚙️ Cara Instalasi & Penggunaan
Pastikan Docker dan Docker Compose sudah terpasang di Debian.

Masuk ke direktori proyek:

Bash
cd /home/debian/uts-asj-edi
Jalankan seluruh layanan:

Bash
docker-compose up -d
Akses melalui browser:

Aplikasi: http://192.168.1.11

Dashboard MinIO: http://192.168.1.11:9001

👤 Identitas
Nama: Herdi

Repository: Sahhyyyx1310/uts-asj-herdi

Tugas: Ujian Tengah Semester - Administrasi Sistem Jaringan
