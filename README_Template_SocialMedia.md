# 🌸 Hubble — Simple Social Media Platform
> Proyek UAS Prinsip Pemrograman | Sistem Informasi – Universitas Atma Jaya Yogyakarta
> T.A. 2025/2026

---

## 👥 Tim Pengembang

| Nama | NIM | Kelas |
|------|-----|-------|
| Derren Amadeo Hermawan | 251713382 | SI-B |

---

## 📋 Deskripsi Aplikasi

Hubble adalah platform media sosial sederhana berbasis desktop yang dibangun menggunakan Python dan Tkinter. Aplikasi ini memungkinkan pengguna untuk berinteraksi secara sosial melalui fitur posting, komentar, like, follow, dan komunitas, dengan sistem peran (role) yang membedakan hak akses antara User biasa, Moderator, dan Admin.

---

## 🚀 Cara Menjalankan Program

### Prasyarat
- Python **3.10** ke atas
- Tidak memerlukan instalasi library eksternal (semua menggunakan library bawaan Python)

### Langkah-langkah

```
1. Pastikan Python sudah terinstall di komputer Anda
   Cek dengan: python --version

2. Clone atau unduh folder proyek ini

3. Masuk ke folder proyek:
   cd NamaAplikasi

4. Jalankan program:
   python main.py
```

### Akun Default untuk Testing

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | Admin123 |
| Moderator | moderator | Mod12345 |
| User | user1 | User1234 |

> ⚠️ Password wajib minimal 8 karakter dan mengandung kombinasi huruf + angka.

---

## 📁 Struktur File Proyek

```
NamaAplikasi/
│
├── main.py          # Entry point — inisialisasi aplikasi dan load data
├── gui.py           # Semua tampilan antarmuka (Tkinter) — View layer
├── logic.py         # Logika bisnis dan algoritma — Controller/Logic layer
├── data.py          # Manajemen penyimpanan data JSON — Data/Model layer
│
├── app_data.json    # File penyimpanan data utama (dibuat otomatis)
├── applogo.png      # Aset gambar logo aplikasi
│
└── README.md        # Dokumentasi ini
```

### Penjelasan Singkat Tiap File

- **`main.py`** — Titik masuk program. Menginisialisasi jendela utama Tkinter, memanggil `load()` saat program dibuka, dan `save()` saat program ditutup.
- **`gui.py`** — Seluruh komponen antarmuka: halaman login, feed, profil, dashboard, dll. Memanggil fungsi dari `logic.py` untuk memproses data.
- **`logic.py`** — Semua logika pemrosesan: autentikasi, algoritma feed ranking, karma system, pencarian, parsing hashtag, validasi input.
- **`data.py`** — Mendefinisikan struktur data (class User, Post, Comment, Community) dan menangani baca/tulis file JSON.

---

## 🔄 Alur Program Utama

### 1. Alur Login & Navigasi

```
Program Dibuka
     │
     ▼
 Load Data (app_data.json)
     │
     ▼
 Halaman Login
     │
  ┌──┴──────────────────┐
  │  Input username &   │
  │  password           │
  └──┬──────────────────┘
     │
  Validasi Autentikasi
     │
  ┌──┴──────────────────────────────┐
  │         Role Terdeteksi?        │
  └──┬──────────────┬───────────────┘
     │              │               │
  User           Moderator       Admin
     │              │               │
  Menu User    Menu Moderator   Menu Admin
  (6 menu)       (7 menu)        (9 menu)
     │
  Pilih Menu
     │
  Tampilkan Halaman Sesuai Pilihan
     │
  Logout → Hapus Session → Kembali ke Login
```

### 2. Alur CRUD Postingan

```
User login sebagai User
     │
     ▼
Halaman Feed/Home
     │
  [Tombol Buat Post]
     │
     ▼
Form Input Post
  - Isi konten teks
  - Sistem otomatis ekstrak #hashtag dari teks
     │
  Validasi (konten tidak boleh kosong)
     │
     ▼
Post Tersimpan
  - Timestamp otomatis
  - Hashtag diindeks ke database
  - Feed di-refresh & diurutkan ulang (Feed Ranking)
     │
     ▼
Post Muncul di Feed (terurut berdasarkan skor)

[Edit Post]          [Hapus Post]
     │                    │
Hanya pemilik       Konfirmasi dialog
post yang bisa      → Hapus permanen
mengedit            → Update feed
```

### 3. Alur Interaksi Sosial

```
User melihat Post di Feed
     │
  ┌──┴──────────────────────────────────┐
  │           Pilih Interaksi           │
  └──┬──────────┬──────────┬────────────┘
     │          │          │
  [Like]    [Simpan]   [Komentar]
     │          │          │
  Toggle     Toggle     Tambah teks
  +/- like   +/- save   komentar
     │          │          │
  Update     Update     Update
  counter    list       counter
     │          │          │
  Karma pemilik   Karma pemilik
  post +2 poin    post +3 poin
```

### 4. Alur Follow & Friend Request

```
User A membuka Profil User B
     │
  ┌──┴─────────────────────────┐
  │       Pilih Aksi           │
  └──┬──────────────┬──────────┘
     │              │
  [Follow]    [Kirim Friend Request]
     │              │
  Langsung       Status: "Pending"
  follow         User B menerima notifikasi
     │              │
  Tombol         User B: Terima / Tolak
  berubah            │
  "Unfollow"     Terima → Status "Teman"
                 Tolak  → Status dihapus
```

### 5. Alur Dashboard & Export

```
Login sebagai Admin/Moderator
     │
     ▼
Menu Dashboard Analitik
     │
  ┌──┴────────────────────────────────────┐
  │         Data Ditampilkan:             │
  │  - Engagement Score tiap post         │
  │    (likes×2 + comments×3 + saves×1)   │
  │  - Top 5 Hashtag Trending             │
  │  - Ringkasan Aktivitas User           │
  └──┬────────────────────────────────────┘
     │
  [Tombol Export]
     │
  ┌──┴────────────────┐
  │  Pilih format:    │
  │  .TXT atau .CSV   │
  └──┬────────────────┘
     │
  File tersimpan otomatis
  dengan nama + timestamp
```

---

## ⚙️ Fitur Opsional Wajib yang Diimplementasikan

### 1. Feed Ranking Algorithm

Feed tidak diurutkan berdasarkan waktu saja, melainkan menggunakan formula skor:

```
skor = (jumlah_like × 2) + (jumlah_komentar × 3) + (jumlah_simpan × 1) + (recency_weight)
```

- Post yang banyak dikomentari diprioritaskan lebih tinggi dari sekadar banyak like
- `recency_weight` memberi bobot waktu: post baru mendapat nilai lebih tinggi
- Feed diurutkan ulang setiap kali ada interaksi baru

### 2. Reputation / Karma System

Setiap interaksi positif menambah poin karma ke pemilik konten:

| Interaksi | Poin Karma |
|-----------|-----------|
| Post di-like | +2 poin |
| Post di-komentar | +3 poin |
| Post di-simpan | +1 poin |

Poin karma menentukan badge profil secara otomatis:

| Badge | Syarat |
|-------|--------|
| 🌱 Beginner | 0 – 49 poin |
| ⚡ Active | 50 – 149 poin |
| 🌟 Expert | 150 – 499 poin |
| 👑 Legend | 500+ poin |

---

## 🎯 9 Modul Prinsip Pemrograman

| No | Modul | Digunakan di | Contoh Penggunaan |
|----|-------|--------------|-------------------|
| 1 | Tipe Data Dasar | `data.py`, `logic.py` | String (username, konten), Integer (like count, karma), Boolean (is_saved, is_followed) |
| 2 | String | `logic.py` | Validasi password, ekstrak hashtag dengan split(), upper()/lower() untuk pencarian |
| 3 | Operator & Boolean | `logic.py` | Operator aritmatika pada formula feed ranking, operator logika pada validasi input |
| 4 | Tipe Data Majemuk | `data.py`, `logic.py` | List (daftar post, komentar), Dictionary (data user), Set (hashtag unik) |
| 5 | Conditional | `logic.py`, `gui.py` | if-elif-else untuk role check, validasi input, penentuan badge karma |
| 6 | Perulangan | `logic.py`, `gui.py` | for loop untuk render feed, hitung frekuensi hashtag, iterasi daftar user |
| 7 | Fungsi | `logic.py` | Fungsi modular: autentikasi(), hitung_skor_feed(), get_trending_hashtags() |
| 8 | Class & OOP | `data.py`, `logic.py` | Class User, Post, Comment, Community dengan atribut dan method masing-masing |
| 9 | GUI Tkinter + CRUD | `gui.py` | Frame, Label, Button, Entry, Listbox, ttk.Treeview untuk semua halaman |

---

## 💾 Struktur Data (app_data.json)

Data disimpan dalam satu file JSON dengan struktur berikut:

```json
{
  "users": [
    {
      "user_id": "u001",
      "username": "contoh_user",
      "password": "Pass1234",
      "role": "user",
      "bio": "Halo!",
      "karma": 45,
      "badge": "Beginner",
      "followers": [],
      "following": [],
      "friends": [],
      "friend_requests": [],
      "saved_posts": []
    }
  ],
  "posts": [
    {
      "post_id": "p001",
      "author_id": "u001",
      "content": "Halo dunia! #belajar #python",
      "hashtags": ["belajar", "python"],
      "likes": [],
      "comments": [],
      "saves": [],
      "timestamp": "2026-06-13 10:00:00"
    }
  ],
  "communities": [],
  "reports": []
}
```

---

## ⚠️ Hal yang Perlu Diperhatikan

- **Program tidak bisa crash** saat input kosong — semua form sudah divalidasi
- **Data tersimpan otomatis** saat program ditutup dengan tombol X
- **Konfirmasi sebelum hapus** selalu muncul untuk mencegah penghapusan tidak sengaja
- Jika file `app_data.json` dihapus, program akan membuat data baru secara otomatis

---

## 📌 Catatan Pengembangan

Proyek ini dibuat sebagai bagian dari UAS Prinsip Pemrograman dan mengimplementasikan seluruh 9 modul yang dipelajari selama semester. Pendekatan MVC ringan digunakan untuk memisahkan tanggung jawab antara tampilan (gui.py), logika (logic.py), dan data (data.py).

---

*Dibuat oleh: [Nama Tim] — Program Studi Sistem Informasi, Universitas Atma Jaya Yogyakarta*
