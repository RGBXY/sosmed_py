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

```
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
├── image/                     # Folder tempat menyimpan gambar
├── .gitignore                 # Memastikan file atau folder tertentu tidak masuk repository github
└── README.md
```

### Penjelasan Singkat Tiap Berkas Utama

- **`main.py`** — Mengatur siklus hidup aplikasi. Menginisialisasi `tk.Tk`, memicu pembuatan database lewat `init_db()`, memuat modul sensor ke memori RAM, dan mengelola perpindahan halaman via fungsi `switch_frame` guna mencegah kebocoran memori (*memory leak*).
- **`model.py`** — Menyediakan standarisasi objek data (Class `User`, `Community_Member`, `Post`, `Comment`, `NotificationData`, `Badwords`) dilengkapi dengan fungsi aman `@staticmethod convert()` untuk mengubah data mentah database menjadi objek siap pakai di UI.
- **`logic.py`** — Otak dari seluruh fitur aplikasi. Memproses validasi berlapis form login, logika pendaftaran/keluar anggota komunitas, hingga penapisan kata kotor (*bad words caching mechanism*).
- **`data.py`** — Menangani seluruh komunikasi tingkat rendah dengan sistem manajemen database (klausa `SELECT`, `INSERT`, `UPDATE`, `DELETE`) menggunakan arsitektur *context manager* (`with get_db()`).
- **`gui/`** — Menyimpan semua kebutuhan GUI seperti (`Component`, `Frame`, `Utils`) agar dapat lebih memudahkan dalam pembuatan gui dan membuat kode menjadi lebih rapih dan mudah dibaca.

---

## 🔄 Alur Program Utama

### 1. Alur Login & Navigasi Dinamis (Role-Based)
```
                 Program Dibuka (main.py)
                             │
                             ▼
            Inisialisasi DB & Load Badwords Cache
                             │
                             ▼
                Render Halaman Login Frame
                             │
                   ┌─────────┴─────────┐
                   │  Input username   │
                   │    & password     │
                   └─────────┬─────────┘
                             │
          Verifikasi SQL Hash Kredensial (data.py)
                             │
                             ▼
   Sukses? → Inject Objek User ke State (self.current_user)
                             │
                             ▼
    ┌─────────────────────────────────────────────────┐
    │ Callback auth_success() Memicu Router Hak Akses │
    └────────┬───────────────┬────────────────┬───────┘
             │               │                │
          [ User ]     [ Moderator ]      [ Admin ]
             │               │                │
             ▼               ▼                ▼
       Render HomeFrame   Render DashMod   Render DashAdmin
       + Sidebar User     + Sidebar Mod    + Sidebar Admin
             │               │                │
             └───────────────┼────────────────┘
                             │
                             ▼
             [ EKSEKUSI LOGOUT / KELUAR ]
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │ 1. Kosongkan State Session User       │
         │ 2. Hancurkan Instance Frame Aktif     │
         │ 3. Alihkan Kembali ke LoginFrame      │
         └───────────────────────────────────────┘
```

### 2. Alur CRUD Post (Community Hub)
```
                 [ USER INPUT KONTEN POSTINGAN ]
                                │
                                ▼
         ┌──────────────────────────────────────────────┐
         │        Proses Validasi Input Teks            │
         └──────────────────────┬───────────────────────┘
                                │
                      (Apakah Teks Kosong?)
                        ├── Ya  ──> Tampilkan Error Messagebox
                        └── Tidak
                                │
                                ▼
         ┌──────────────────────────────────────────────┐
         │     Pengecekan Kamus Sensor Kata Kasar       │
         │      (Mencocokkan dengan RAM Cache Set)      │
         └──────────────────────┬───────────────────────┘
                                │
                     (Ditemukan Kata Kotor?)
                        ├── Ya  ──> Ganti kata kotor dengan Asterisk (****)
                        └── Tidak ─> Biarkan teks asli
                                │
                                ▼
         ┌──────────────────────────────────────────────┐
         │    Identifikasi Lokasi Ruang Publikasi       │
         └──────────────────────┬───────────────────────┘
                                │
                 (Pilihan Komunitas Tujuan?)
                   ├── Global Feed  ──> Simpan dengan 'community_id' Global
                   └── Grup Tertentu ─> Simpan dengan 'community_id' Internal
                                │
                                ▼
         ┌──────────────────────────────────────────────┐
         │     Eksekusi SQL: INSERT INTO posts ...      │
         └──────────────────────┬───────────────────────┘
                                │
                                ▼
      ┌────────────────────────────────────────────────────┐
      │  Memicu Fungsi handle_form_success() pada parent   │
      └────────────────────────────────────────────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        │                                               │
        ▼                                               ▼
   [ AKSI EDIT POST ]                              [ AKSI HAPUS POST ]
        │                                               │
Pengecekan Otoritas Akses                       Pengecekan Otoritas Akses
(ID Pemilik == ID User?)                        (ID Pemilik == ID User / Role Staff?)
        │                                               │
  ├── Tidak ──> Tombol Sembunyi                   ├── Tidak ──> Tombol Sembunyi
  └── Ya                                          └── Ya
        │                                               │
        ▼                                               ▼
Buka Jendela Modal Edit                         Tampilkan `messagebox.askyesno`
        │                                               │
Kirim SQL UPDATE ke DB                          Kirim SQL DELETE ke DB
        │                                               │
        └───────────────────────┬───────────────────────┘
                                ▼
                    handle_form_success() paent
```

### 3. Alur Manajemen & Navigasi Komunitas (Community Hub)
```
User Membuka Menu Komunitas (comunity.py)
                                   │
                                   ▼
             Tarik Seluruh Record Komunitas dari DB 
          (Kecuali "Global Feed" yang disaring otomatis)
                                   │
                                   ▼
      ┌────────────────────────────────────────────────────────┐
      │ Render Komponen Secara Efisien ke dalam Scrollable Canvas│
      └────────────────────────────┬───────────────────────────┘
                                   │
                                   ▼
         Identifikasi Status Hubungan Pengguna dengan Komunitas
                                   │
                                   ▼
      ┌────────────────────────────────────────────────────────┐
      │                Pengecekan Akses Tombol                 │
      └──────────────┬───────────────────────────┬─────────────┘
                     │                           │
             [ Apakah Anggota? ]     [ Apakah Creator / Admin / Mod? ]
                     │                           │
          ├── Ya  ──> Tombol "Leave"  ├── Ya  ──> Tombol "Edit" & "Hapus"
          └── Tidak ─> Tombol "Join"  └── Tidak ─> Tombol Manajemen Hidden
                     │                           │
                     ▼                           ▼
             Eksekusi Aksi via            Buka Modal Windows
              Community_Logic            (CommunityFormWindow)
                     │                           │
                     └───────────────────────────┼────────────────┘
                                                 │
                                                 ▼
                                     refresh_page_data() GUI
```

### 4. Alur Sensor Kata Kasar (*Real-time Badwords Filter*)
```
                   Aplikasi Hubble Pertama Kali Dijalankan
                                     │
                                     ▼
                     Kelas Sensor_Logic() Diinisialisasi
                                     │
                                     ▼
                  Query Seluruh Kata Terlarang dari Tabel 
                        'badwords' via get_badwords()
                                     │
                                     ▼
                K   onversi Data Menjadi Tipe 'Set' di RAM 
                                     │
                                     ▼
        ┌────────────────────────────────────────────────────────┐
        │       User Membuat Postingan Baru / Menulis Komentar   │
        └────────────────────────────┬───────────────────────────┘
                                     │
                                     ▼
                Sistem Membaca String Konten & Melakukan 
                           Scanning Komparasi
                                     │
                                     ▼
                 [ Ditemukan Kata Kasar Cocok dengan RAM? ]
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
                 [  Ya ]                           [ Tidak ]
                    │                                 │
                    ▼                                 ▼
         Sensor Otomatis Mengubah                Konten Lolos
         Kata Menjadi Asterisk (****)            Tanpa Sensor
                    │                                 │
                    ▼                                 │
         Simpan Konten Bersih ke DB                   │
                    │                                 │
                    ▼                                 ▼
         Tambahkan ke Log Pelanggaran        [ SELESAI / OKE ]
                    │
                    ▼
               [ SELESAI ]

```

---

## 8. ⚙️ Fitur Opsional Wajib yang Diimplementasikan

### 1. Memori Cache Set untuk Sensor Kata Kasar 
Untuk menghindari penurunan performa akibat melakukan query database berulang-ulang setiap kali user mengirim pesan, Hubble menerapkan teknik **RAM Caching**. 
Saat aplikasi dibuka, 120+ data kata kasar ditarik sekali saja dan disimpan ke dalam struktur data **Set Python**. Pencarian kata kotor pada postingan menggunakan struktur data Set berjalan dalam kompleksitas waktu **$O(1)$ (Konstan)**, membuat aplikasi tetap responsif dan anti-lag.

### 2. Algoritma Feed Ranking Berbasis Recency Score
Untuk menyajikan linimasa yang dinamis, Hubble menerapkan sistem pemeringkatan postingan (*feed ranking*) berbasis waktu (*recency*). Peringkat dihitung secara matematis dengan membagi total interaksi (*likes*) terhadap selisih waktu pembuatan konten menggunakan fungsi peluruhan (*time-decay*). Pendekatan ini memastikan postingan baru yang hangat langsung didorong ke baris paling atas linimasa, sementara postingan lama akan turun peringkatnya secara otomatis meskipun memiliki jumlah *likes* yang tinggi.

 ---

## 9. 🎯 Modul Prinsip Pemrograman yang Diterapkan

| No | Modul | Digunakan di | Contoh Penggunaan Nyata pada Hubble |
|----|-------|--------------|-------------------------------------|
| 1 | Tipe Data Dasar | `model.py`, `data.py` | String untuk `username` & `content`, Integer untuk `id` & total likes, Boolean untuk status `is_liked_by_me` & `is_saved_by_me`. |
| 2 | String | `logic.py` | Penggunaan `.strip().lower()` untuk standarisasi pencarian nama komunitas, serta tokenisasi teks postingan saat proses pemindaian sensor. |
| 3 | Operator & Boolean | `logic.py`, `gui/` | Operator aritmatika & eksponen (`**`) pada rumus peluruhan waktu *feed ranking*, serta operator logika `if not res` untuk deteksi kegagalan login. |
| 4 | Tipe Data Majemuk | `logic.py`, `model.py` | List untuk menampung kumpulan objek baris data dari database, dan **Set** untuk menampung *cache* memori data kata terlarang (`bad_words_cache`). |
| 5 | Conditional | `main.py`, `gui/` | Percabangan `if-elif-else` berbasis role pengguna (`admin`/`moderator`/`user`) dinamis pada fungsi callback penentu halaman `auth_success`. |
| 6 | Perulangan | `gui/frames/` | `for row in data:` untuk merender susunan kartu box komunitas secara otomatis, dan perulangan `for item in tree.get_children()` untuk membersihkan tabel. |
| 7 | Fungsi | `data.py`, `logic.py` | Fungsi terisolasi yang modular dan *reusable* seperti `login_user_auth(u, p)`, `hitung_recency_score()`, dan `check_membership_logic(c_id, u_id)`. |
| 8 | Class & OOP | Seluruh Berkas | Pewarisan sifat objek (*Inheritance*) dari objek Tkinter (`class Main(tk.Tk)` & `class ComunityFrame(tk.Frame)`), serta enkapsulasi cetak biru data pengguna lewat Class `User`. |
| 9 | GUI Tkinter + CRUD | Paket folder `gui/` | Pemanfaatan komponen `tk.Canvas` untuk area *scroll*, `tk.Toplevel` untuk sub-jendela form modal baru, dan `ttk.Treeview` untuk menyusun baris tabel data badwords. |

---

## 10. 💾 Struktur Data & Skema Database (SQLite)

Aplikasi Hubble menggunakan sistem manajemen basis data relasional **SQLite** untuk menjamin konsistensi, performa pencarian, dan integritas data. Berikut adalah detail struktur dari masing-masing tabel yang digunakan:

### 1. Tabel `users`
Tempat menyimpan data akun kredensial, autentikasi, dan tingkatan hak akses pengguna.

| No | Nama Kolom | Tipe Data | Atribut Kolom | Keterangan |
|:--:|:---|:---|:---|:---|
| 1 | **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID unik otomatis untuk setiap pengguna |
| 2 | **username** | TEXT | UNIQUE, NOT NULL | Nama pengguna unik yang digunakan untuk login |
| 3 | **password** | TEXT | NOT NULL | Kata sandi yang sudah diamankan lewat enkripsi *hash* |
| 4 | **role** | TEXT | NOT NULL | Hak akses tingkat pengguna (`user`, `moderator`, `admin`) |

---

### 2. Tabel `communities`
Tempat menyimpan data entitas kelompok atau wadah diskusi forum yang dibuat di dalam aplikasi.

| No | Nama Kolom | Tipe Data | Atribut Kolom | Keterangan |
|:--:|:---|:---|:---|:---|
| 1 | **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID unik otomatis untuk setiap komunitas |
| 2 | **user_id** | INTEGER | FOREIGN KEY ➔ `users.id` | ID pengguna yang bertindak sebagai pembuat (*creator*) |
| 3 | **name** | TEXT | NOT NULL | Nama dari ruang komunitas (contoh: "Python Developer") |
| 4 | **description**| TEXT | NOT NULL | Penjelasan singkat mengenai topik bahasan komunitas |

---

### 3. Tabel `posts`
Tempat menyimpan data konten kiriman teks yang dipublikasikan oleh pengguna pada lini masa tertentu.

| No | Nama Kolom | Tipe Data | Atribut Kolom | Keterangan |
|:--:|:---|:---|:---|:---|
| 1 | **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID unik otomatis untuk setiap postingan |
| 2 | **user_id** | INTEGER | FOREIGN KEY ➔ `users.id` | ID pengguna yang menulis dan mengunggah postingan |
| 3 | **community_id**| INTEGER | FOREIGN KEY ➔ `communities.id`| Target ruang diskusi komunitas tempat post berada |
| 4 | **content** | TEXT | NOT NULL | Isi teks kiriman (yang lolos dari pemindaian sensor) |
| 5 | **created_at** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Waktu publikasi post (untuk kalkulasi *recency score*) |

---

### 4. Tabel `comments`
Tempat menyimpan data interaksi timbal balik berupa tanggapan komentar di bawah suatu postingan.

| No | Nama Kolom | Tipe Data | Atribut Kolom | Keterangan |
|:--:|:---|:---|:---|:---|
| 1 | **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT | ID unik otomatis untuk setiap baris komentar |
| 2 | **user_id** | INTEGER | FOREIGN KEY ➔ `users.id` | ID pengguna yang menulis tanggapan komentar |
| 3 | **post_id** | INTEGER | FOREIGN KEY ➔ `posts.id` | ID postingan target tempat komentar disematkan |
| 4 | **content** | TEXT | NOT NULL | Isi teks komentar (yang telah melalui sensor kata kasar) |
| 5 | **created_at** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Catatan waktu saat komentar tersebut dikirimkan |

---

### 5. Relasi Database
```
users
 │
 ├── communities
 │
 ├── posts
 │     ├── likes
 │     └── comments
 │
 ├── follows
 │
 ├── notifications
 │
 └── user_violation_logs

communities
 │
 ├── community_members
 │
 └── posts

posts
 │
 ├── likes
 ├── comments
 └── saved_posts
```

---

## ⚠️ Hal yang Perlu Diperhatikan

- **Program tidak bisa crash** saat input kosong — semua form sudah divalidasi
- **Konfirmasi sebelum hapus** selalu muncul untuk mencegah penghapusan tidak sengaja
- Jika file `database.db` dihapus, program akan membuat data baru secara otomatis

---

## 📌 Catatan Pengembangan

Proyek ini dibuat sebagai bagian dari UAS Prinsip Pemrograman dan mengimplementasikan seluruh 9 modul yang dipelajari selama semester. Pendekatan MVC ringan digunakan untuk memisahkan tanggung jawab antara tampilan (gui/), logika (logic.py), dan data (data.py).

---

*Dibuat oleh: Derren Amadeo Hermwan — Program Studi Sistem Informasi, Universitas Atma Jaya Yogyakarta*
