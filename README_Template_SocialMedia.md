# 🌸 Hubble — Forum & Community-Based Social Media Platform
> Proyek UAS Prinsip Pemrograman | Sistem Informasi – Universitas Atma Jaya Yogyakarta
> T.A. 2025/2026

---

## 👥 Tim Pengembang

| Nama | NIM | Kelas |
|------|-----|-------|
| Derren Amadeo Hermawan | 251713382 | SI-B |

---

## 📋 Deskripsi Aplikasi

**Hubble** adalah platform media sosial berbasis komunitas (forum) desktop yang dibangun menggunakan Python dan Tkinter. Berbeda dengan media sosial konvensional, Hubble berfokus pada ruang diskusi terfragmentasi via ruang komunitas. Aplikasi ini menerapkan sistem manajemen basis data relasional, pengamanan session pengguna, serta sistem moderasi pintar melalui sensor kata kasar secara otomatis (*real-time*). 

Aplikasi ini mengimplementasikan *Role-Based Access Control* (RBAC) yang memisahkan hak akses secara dinamis untuk **User biasa**, **Moderator**, dan **Admin**.

---

## 🚀 Cara Menjalankan Program

### Prasyarat
- Python **3.10** ke atas
- Database Engine Sq
- Library eksternal penunjang (jika ada, cantumkan di sini)

### Langkah-langkah
1. Pastikan Python sudah terinstall di komputer Anda
   Cek dengan: python --version

2. Clone atau unduh folder proyek Hubble ini

3. Masuk ke folder root proyek:
   cd Hubble

4. Jalankan program utama:
   python main.py

### Akun Default untuk Testing

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | 12345678 |
| Moderator | moderator | 12345678 |
| User | budi | 12345678 |

---

## 📁 Struktur File Proyek

Aplikasi Hubble dikembangkan menggunakan pendekatan arsitektur **MVC (Model-View-Controller) yang Modular**, memisahkan komponen antarmuka ke dalam sub-paket khusus agar kode mudah dirawat

Hubble/
│
├── main.py                    # Entry point — Inisialisasi jendela utama & state router
├── data.py                    # Data Layer — Query SQL, koneksi database, & fungsi transaksi
├── logic.py                   # Logic Layer — Berisi fungsionalitas fitur & pengolahan data bisnis
├── model.py                   # Model Layer — Mapping & konversi record database menjadi objek Python
├── constrants.py              # Global Configuration — Palet warna, ukuran font, dan konstanta UI
│
├── gui/                       # View Layer — Seluruh komponen antarmuka (Tkinter)
│   ├── components/            # Komponen UI global (Header, reusable widget)
│   ├── utils/                 # Utility UI (Render sidebar berdasarkan hak akses)
│   └── frames/                # Halaman/Layar penuh aplikasi
│       ├── auth/              # Halaman Login & Registrasi
│       ├── admin/             # Dashboard manajemen milik Admin
│       ├── moderator/         # Dashboard moderasi milik Moderator
│       ├── home.py            # Linimasa utama (Feed) User
│       ├── comunity.py        # Eksplorasi Hub daftar Komunitas
│       └── comunity_post.py   # Linimasa postingan internal grup komunitas
│
└── README.md

### Penjelasan Singkat Tiap Berkas Utama

- **`main.py`** — Mengatur siklus hidup aplikasi. Menginisialisasi `tk.Tk`, memicu pembuatan database lewat `init_db()`, memuat modul sensor ke memori RAM, dan mengelola perpindahan halaman via fungsi `switch_frame` guna mencegah kebocoran memori (*memory leak*).
- **`model.py`** — Menyediakan standarisasi objek data (Class `User`, `Community_Member`, `Post`, `Comment`, `NotificationData`, `Badwords`) dilengkapi dengan fungsi aman `@staticmethod convert()` untuk mengubah data mentah database menjadi objek siap pakai di UI.
- **`logic.py`** — Otak dari seluruh fitur aplikasi. Memproses validasi berlapis form login, logika pendaftaran/keluar anggota komunitas, hingga penapisan kata kotor (*bad words caching mechanism*).
- **`data.py`** — Menangani seluruh komunikasi tingkat rendah dengan sistem manajemen database (klausa `SELECT`, `INSERT`, `UPDATE`, `DELETE`) menggunakan arsitektur *context manager* (`with get_db()`).

---

## 🔄 Alur Program Utama

### 1. Alur Login & Navigasi Dinamis (Role-Based)
Program Dibuka (main.py)
│
▼
Inisialisasi DB & Load Cache Badwords ke RAM
│
▼
Render Halaman Login Frame
│
┌──┴──────────────────┐
│  Input username &   │
│  password           │
└──┬──────────────────┘
│
Verifikasi SQL Hash Kredensial (data.py)
│
Sukses? → Inject Objek User ke Main State (self.current_user)
│
┌──┴────────────────────────────────────────────────┐
│  Callback auth_success() Memicu Router Hak Akses  │
└──┬──────────────────────┬─────────────────────────┘
│                      │                         │
User                   Moderator                 Admin
│                      │                         │
Render HomeFrame       Render DashboardMod       Render DashboardAdmin

Sidebar User         + Sidebar Moderator       + Sidebar Admin
│                      │                         │
└──────────────────────┼─────────────────────────┘
▼
Logout() → Kosongkan State Session User
→ Hancurkan Frame Aktif
→ Kembali ke LoginFrame

### 2. Alur Manajemen & Navigasi Komunitas (Community Hub)
User Membuka Menu Komunitas (comunity.py)
│
▼
Tarik Seluruh Record Komunitas dari DB (Kecuali "Global Feed" yang disaring otomatis)
│
┌──┴───────────────────────────────────────────────────────┐
│  Render Komponen Secara Efisien ke dalam Scrollable Canvas │
└──┬───────────────────────────────────────────────────────┘
│
Identifikasi Status Hubungan Pengguna dengan Komunitas
│
┌──┴───────────────────────────────────────────────────────┐
│               Pengecekan Akses Tombol                    │
└──┬──────────────────────┬────────────────────────────────┘
│                      │
[Apakah Anggota?]      [Apakah Pemilik / Admin / Moderator?]
│                      │
Ya  → Tombol "Leave"   Ya  → Tombol "Edit" & "Hapus" Muncul
Tidak → Tombol "Join"  Tidak → Tombol Manajemen Disembunyikan
│                      │
▼                      ▼
Eksekusi Aksi via     Buka Modal Windows (CommunityFormWindow)
Community_Logic       untuk Mutasi Data / CRUD ke Database
│                      │
└──────────────────────┴──→ Refresh Tampilan Halaman (refresh_page_data)

### 3. Alur Sistem Sensor Kata Kasar (*Real-time Badwords Filter*)
Aplikasi Hubble Pertama Kali Dijalankan
│
▼
Kelas Sensor_Logic() Diinisialisasi
│
Query Seluruh Kata Terlarang dari Tabel 'badwords' lewat get_badwords()
│
▼
Konversi Data Menjadi Tipe 'Set' di RAM (bad_words_cache) untuk Pencarian O(1)
│
┌──┴──────────────────────────────────────────────────────┐
│  User Membuat Postingan Baru / Menulis Komentar          │
└──┬──────────────────────────────────────────────────────┘
│
Sistem Membaca String Konten & Melakukan Scanning Komparasi
│
Ditemukan Kata Kasar yang Cocok dengan Cache RAM?
│
┌──┴──────────────────────┬───────────────────────────────┐
│                        Ya                              Tidak
▼                                                         ▼
Sensor Otomatis Mengubah Kata                          Konten Lolos
Tersebut Menjadi Asterisk (****)                       Tanpa Sensor
│                                                      │
└──────────────────────┬───────────────────────────────┘
▼
Simpan Konten Bersih ke DB

---

## ⚙️ Fitur Unggulan yang Diimplementasikan

### 1. Memori Cache Set untuk Sensor Kata Kasar (Performa Tinggi)
Untuk menghindari penurunan performa akibat melakukan query database berulang-ulang setiap kali user mengirim pesan, Hubble menerapkan teknik **RAM Caching**. 
Saat aplikasi dibuka, 120+ data kata kasar ditarik sekali saja dan disimpan ke dalam struktur data **Set Python**. Pencarian kata kotor pada postingan menggunakan struktur data Set berjalan dalam kompleksitas waktu **$O(1)$ (Konstan)**, membuat aplikasi tetap responsif dan anti-lag.

### 2. Pengamanan Memory Leak via Widget Destruction
Navigasi antar-halaman pada aplikasi desktop rawan memakan RAM yang besar jika frame lama hanya disembunyikan. Hubble mengimplementasikan metode pembersihan memori secara eksplisit pada fungsi `switch_frame()`:
```python
if self.current_frame:  
    self.current_frame.destroy()  # Menghapus instance lama secara permanen dari RAM

3. Skalabilitas Visual dengan ttk.Treeview + Scrollbar
Pada dashboard manajemen kata kasar admin, aplikasi mampu memuat ratusan baris data secara rapi tanpa merusak susunan tata letak grafis menggunakan komponen ttk.Treeview. Data dibungkus ke dalam tabel dengan tinggi statis berkecepatan render tinggi yang dilengkapi komponen interaksi Scrollbar vertikal.