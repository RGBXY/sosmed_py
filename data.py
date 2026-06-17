import sqlite3
import csv
import os
import hashlib 

DB_PATH = "./database/database.db"

def get_db():
    """Membuka koneksi database dengan konfigurasi Row Factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn 

# ============================================================
# SECTION: DATABASE INITIALIZATION
# ============================================================
def init_db():
    """Menginisialisasi seluruh skema tabel database dan data awal (seeding)."""
    # Mengaktifkan fitur Foreign Key cascading di SQLite secara eksplisit
    with get_db() as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        
        # 1. Tabel Users
        conn.execute(""" 
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )""")

        # 2. Tabel Communities (Diperbaiki dari 'comunities')
        conn.execute(""" 
            CREATE TABLE IF NOT EXISTS communities(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )""")

        # 3. Tabel Community Members
        conn.execute(""" 
            CREATE TABLE IF NOT EXISTS community_members(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                community_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(community_id, user_id), 
                FOREIGN KEY (community_id) REFERENCES communities(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )""")

        # 4. Tabel Posts
        conn.execute(""" 
            CREATE TABLE IF NOT EXISTS posts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                community_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (community_id) REFERENCES communities(id) ON DELETE CASCADE     
            )""")

        # 5. Tabel Likes
        conn.execute("""
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, post_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
            )""")

        # 6. Tabel Comments
        conn.execute("""
           CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
            )""")
        
        # 7. Tabel Follows
        conn.execute("""
           CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id INTEGER NOT NULL,      
                following_id INTEGER NOT NULL,     
                status TEXT DEFAULT 'pending',     
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(follower_id, following_id),
                FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE
            )""")
        
        # 8. Tabel Notifications
        conn.execute("""
           CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,          
                sender_id INTEGER,                 
                type TEXT NOT NULL,                
                message TEXT NOT NULL,             
                related_id INTEGER,                
                is_read INTEGER DEFAULT 0,         
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )""")
        
        # 9. Tabel Saved Posts
        conn.execute("""
           CREATE TABLE IF NOT EXISTS saved_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                post_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, post_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
            )""")
        
        # 10. Tabel Badwords
        conn.execute("""
            CREATE TABLE IF NOT EXISTS badwords (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 word TEXT UNIQUE NOT NULL
            )""")
        
        # 11. Tabel User Violation Logs (user_id diubah ke INTEGER agar valid saat JOIN)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_violation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )""")
        
        # --- SEEDING DATA AWAL ---
        check_user = conn.execute("SELECT COUNT(*) FROM users").fetchone()
        if check_user[0] == 0:
            # Menggunakan hashing SHA256 sederhana untuk keamanan data user
            def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
            data_users = [
                ("admin", hash_pw("12345678"), "admin"),      
                ("moderator", hash_pw("12345678"), "moderator"),
                ("budi", hash_pw("12345678"), "user"),        
                ("ican", hash_pw("12345678"), "user"),        
            ]
            conn.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", data_users)
            conn.commit()

        # Pembuatan Komunitas Global Default
        check_global = conn.execute("SELECT id FROM communities WHERE name = 'Global Feed'").fetchone()
        if not check_global:
            cursor = conn.execute("""
                INSERT INTO communities (user_id, name, description) 
                VALUES (1, 'Global Feed', 'Tempat semua user Hubble berkumpul dan berbagi cerita secara umum.')
            """)
            global_id = cursor.lastrowid
            conn.commit()
        else:
            global_id = check_global[0]

        # Daftarkan otomatis user yang belum join komunitas global
        all_users = conn.execute("SELECT id FROM users").fetchall()
        for row in all_users:
            conn.execute("""
                INSERT OR IGNORE INTO community_members (community_id, user_id) 
                VALUES (?, ?)
            """, (global_id, row[0]))
        conn.commit()


# ============================================================
# SECTION: USER AUTHENTICATION & MANAGEMENT
# ============================================================
def hash_password(password):
    """Mengamankan teks password mentah menggunakan algoritma SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_if_user_exist(conn, username):
    """Mengecek eksistensi username di dalam database."""
    check = conn.execute("SELECT 1 FROM users WHERE username=?", (username.strip(),)).fetchone()
    return "username_exist" if check else False

def login_user_auth(username, password):
    """Melakukan verifikasi login berdasarkan kesamaan kombinasi username & hash password."""
    hashed = hash_password(password.strip())
    with get_db() as conn:
        return conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username.strip(), hashed)).fetchone()

def register_user_auth(username, password):
    """Mendaftarkan akun baru tingkat pengguna (user)."""
    hashed = hash_password(password.strip())
    with get_db() as conn:
        if check_if_user_exist(conn, username.strip()):
            return "username_exist"
        
        conn.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (username.strip(), hashed, "user"))
        conn.commit()
        return conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def register_admin(username, password, role):
    """Mendaftarkan akun baru khusus untuk kebutuhan otoritas struktural (admin/moderator)."""
    hashed = hash_password(password.strip())
    with get_db() as conn:
        if check_if_user_exist(conn, username.strip()):
            return "username_exist"
        conn.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (username.strip(), hashed, role))
        conn.commit()
        return True

def edit_user(user_id, username, password, role):
    """Memperbarui informasi profile dan kredensial akses user berdasarkan ID."""
    with get_db() as conn:
        duplicate = conn.execute("SELECT id FROM users WHERE username = ? AND id != ?", (username.strip(), user_id)).fetchone()
        if duplicate:
            return "username_exist"

        if password and password.strip():
            hashed = hash_password(password)
            conn.execute("UPDATE users SET username=?, password=?, role=? WHERE id=?", (username.strip(), hashed, role, user_id))
        else:
            conn.execute("UPDATE users SET username=?, role=? WHERE id=?", (username.strip(), role, user_id))
        conn.commit()
        return True

def change_username(current_username, new_username):
    """Mengubah string pengenal nama (username) unik milik pengguna."""
    with get_db() as conn:
        if check_if_user_exist(conn, new_username):
            return "username_exist"
        conn.execute("UPDATE users SET username=? WHERE username=?", (new_username, current_username))
        conn.commit()
        return conn.execute("SELECT * FROM users WHERE username = ?", (new_username,)).fetchone()

def change_password(user_id, current_password, new_password):
    """Mengubah kata sandi lama akun ke kata sandi baru pasca pengecekan verifikasi hash."""
    with get_db() as conn:
        user_data = conn.execute("SELECT password FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user_data:
            return "user_not_found"
            
        if user_data["password"] != hash_password(current_password):
            return "wrong_password"

        conn.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_password), user_id))
        conn.commit()
        return "success"

def delete_user(user_id):
    """Menghapus user secara permanen."""
    with get_db() as conn:
        conn.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        return True

def get_users_paginated(limit=10, offset=0):
    """Mengambil list data seluruh user menggunakan sistem paginasi kontrol (Best Practice)."""
    with get_db() as conn:
        return conn.execute("SELECT * FROM users LIMIT ? OFFSET ?", (limit, offset)).fetchall()

# ============================================================
# SECTION: COMMUNITY MANAGEMENT
# ============================================================
def create_community(user_id, name, description):
    """Membuat ruang komunitas baru sekaligus mendaftarkan sang pembuat sebagai member internal."""
    if not name or not description:
        return {"status": "Error", "message": ("Gagal", "Data tidak boleh kosong!")}
        
    with get_db() as conn:

        check = conn.execute("SELECT 1 FROM communities WHERE name=?", (name.strip(),)).fetchone()

        if check:
            return "name_exist"

        cursor = conn.execute("INSERT INTO communities (user_id, name, description) VALUES (?, ?, ?)", (user_id, name, description))
        new_id = cursor.lastrowid 
        conn.execute("INSERT INTO community_members (community_id, user_id) VALUES (?, ?)", (new_id, user_id))
        conn.commit()
        return True

def update_community(community_id, name, description):
    """Memperbarui informasi judul dan deskripsi ruang komunitas."""
    with get_db() as conn:
        check = conn.execute("SELECT id FROM communities WHERE name=?", (name, )).fetchone()
        if check and check["id"] != community_id:
            return "name_exist"

        conn.execute("UPDATE communities SET name = ?, description = ? WHERE id = ?", (name, description, community_id))
        conn.commit()
        return True

def delete_community(community_id):
    """Menghapus total data komunitas dari sistem."""
    with get_db() as conn:
        conn.execute("DELETE FROM communities WHERE id=?", (community_id,))
        conn.commit()
        return True

def get_comunities():
    """Mengambil list seluruh komunitas aktif."""
    with get_db() as conn:
        return conn.execute("SELECT * FROM communities").fetchall()

def get_comunity_detail(community_id):
    """Mendapatkan data manifest terperinci milik suatu komunitas berdasarkan ID."""
    with get_db() as conn:
        return conn.execute("SELECT * FROM communities WHERE id = ?", (community_id, )).fetchone()


# ============================================================
# SECTION: POSTS & FEED ENGAGEMENT LOGIC (ALGORITHMIC FEED)
# ============================================================
def create_post(user_id, community_id, content):
    """Membuat kiriman postingan baru di dalam ruang komunitas tertentu."""
    with get_db() as conn:
        conn.execute("INSERT INTO posts (user_id, community_id, content) VALUES (?,?,?)", (user_id, community_id, content))
        conn.commit()
        return True

def get_community_post(community_id, current_user_id, limit=10):
    """Mengambil postingan berdasar ID Komunitas tertentu dengan kalkulasi bobot interaksi (Score Feed)."""
    query = """
        SELECT 
            posts.id, posts.user_id, posts.content, posts.created_at, 
            users.username AS username, users.role AS user_role,
            communities.name AS comunity_name,
            COUNT(DISTINCT likes.id) AS total_likes,
            MAX(CASE WHEN likes.user_id = ? THEN 1 ELSE 0 END) AS is_liked_by_me,
            (SELECT COUNT(*) FROM saved_posts WHERE saved_posts.post_id = posts.id AND saved_posts.user_id = ?) AS is_saved_by_me,
            (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS total_comments,
            (SELECT status FROM follows WHERE follower_id = ? AND following_id = posts.user_id) AS follow_status,
            (COUNT(DISTINCT likes.id) * 2 + 
             (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) * 3 + 
             (1.0 / (1.0 + (JULIANDAY('now') - JULIANDAY(posts.created_at)) * 24))) AS feed_score
        FROM posts
        INNER JOIN users ON posts.user_id = users.id
        INNER JOIN communities ON posts.community_id = communities.id
        LEFT JOIN likes ON posts.id = likes.post_id
        WHERE posts.community_id = ?
        GROUP BY posts.id
        ORDER BY feed_score DESC LIMIT ?;
    """
    with get_db() as conn:
        return conn.execute(query, (current_user_id, current_user_id, current_user_id, community_id, limit)).fetchall()

def get_global_feed(current_user_id, limit=10):
    """Mengambil seluruh data postingan lintas komunitas (Global Beranda Feed) terpopuler."""
    query = """
        SELECT 
            posts.id, posts.user_id, posts.content, posts.created_at, 
            users.username AS username, users.role AS user_role,
            communities.name AS comunity_name,
            COUNT(DISTINCT likes.id) AS total_likes,
            MAX(CASE WHEN likes.user_id = ? THEN 1 ELSE 0 END) AS is_liked_by_me,
            (SELECT COUNT(*) FROM saved_posts WHERE saved_posts.post_id = posts.id AND saved_posts.user_id = ?) AS is_saved_by_me,
            (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS total_comments,
            (SELECT status FROM follows WHERE follower_id = ? AND following_id = posts.user_id) AS follow_status,
            (COUNT(DISTINCT likes.id) * 2 + 
             (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) * 3 + 
             (1.0 / (1.0 + (JULIANDAY('now') - JULIANDAY(posts.created_at)) * 24))) AS feed_score
        FROM posts
        INNER JOIN users ON posts.user_id = users.id
        INNER JOIN communities ON posts.community_id = communities.id
        LEFT JOIN likes ON posts.id = likes.post_id
        GROUP BY posts.id
        ORDER BY feed_score DESC LIMIT ?;
    """
    with get_db() as conn:
        return conn.execute(query, (current_user_id, current_user_id, current_user_id, limit)).fetchall()

def update_post(post_id, content, community_id):
    """Mengubah isi konten atau pemindahan kategori wadah komunitas postingan."""
    with get_db() as conn:
        conn.execute("UPDATE posts SET content = ?, community_id = ? WHERE id = ?;", (content, community_id, post_id))
        conn.commit()
        return True

def delete_post(post_id):
    """Menghapus data postingan dari sistem secara permanen."""
    with get_db() as conn:
        conn.execute("DELETE FROM posts WHERE id=?", (post_id,))
        conn.commit()
        return True

# ============================================================
# SECTION: MEMBERSHIP MANAGEMENT
# ============================================================
def join_community(community_id, user_id):
    """Mendaftarkan ikatan keanggotaan user baru ke suatu komunitas."""
    with get_db() as conn:
        try:
            conn.execute("INSERT INTO community_members (community_id, user_id) VALUES (?, ?)", (community_id, user_id))
            conn.commit()
            return True
        except Exception:
            return False

def leave_community(community_id, user_id):
    """Membatalkan keikutsertaan anggota dari ruang komunitas."""
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM community_members WHERE community_id = ? AND user_id = ?", (community_id, user_id))
        conn.commit()
        return cursor.rowcount > 0

def check_membership_status(community_id, user_id):
    """Memvalidasi status kepemilikan hak akses keanggotaan user."""
    with get_db() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM community_members WHERE community_id = ? AND user_id = ?", (community_id, user_id))
        return cursor.fetchone()[0] > 0

def get_community_members(community_id):
    """Mengambil daftar list seluruh akun anggota suatu komunitas."""
    query = """
        SELECT users.id, users.username, users.role, community_members.joined_at
        FROM community_members
        JOIN users ON community_members.user_id = users.id
        WHERE community_members.community_id = ?
        ORDER BY community_members.joined_at DESC
    """
    with get_db() as conn:
        return conn.execute(query, (community_id,)).fetchall()


# ============================================================
# SECTION: SOCIAL INTERACTIONS (LIKE, COMMENT, FOLLOW, NOTIF)
# ============================================================
def like(user_id, post_id):
    """Menangani fungsi saklar interaksi suka/batal suka (Like/Unlike) postingan."""
    with get_db() as conn:
        res = conn.execute("SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id)).fetchone()
        if res:
            conn.execute("DELETE FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id))
            conn.commit()
            return "unlike"
        else:
            conn.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
            conn.commit()
            return "like"
    
def comment(user_id, post_id, content):
    """Menambahkan baris komentar opini baru pada postingan."""
    with get_db() as conn:
        conn.execute("INSERT INTO comments (user_id, post_id, content) VALUES (?,?,?)", (user_id, post_id, content))
        conn.commit()
        return True

def get_comments(post_id):
    """Mengambil list runtutan seluruh komentar postingan terlampir."""
    query = """
        SELECT comments.id, comments.user_id, comments.post_id, comments.content, comments.created_at, users.username AS username
        FROM comments
        INNER JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY comments.id ASC;
    """
    with get_db() as conn:
        return conn.execute(query, (post_id,)).fetchall()

def delete_comment(comment_id):
    """Menghapus komentar tertunjuk."""
    with get_db() as conn:
        conn.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
        return True

def update_comment(comment_id, content):
    """Memperbarui teks isi dari komentar."""
    with get_db() as conn:
        conn.execute("UPDATE comments SET content = ? WHERE id = ?", (content, comment_id))
        conn.commit()
        return True

def saved_post(user_id, post_id):
    """Menangani fungsi penanda arsip simpan/batal simpan (Bookmark) kiriman."""
    with get_db() as conn:
        res = conn.execute("SELECT 1 FROM saved_posts WHERE user_id = ? AND post_id = ?", (user_id, post_id)).fetchone()
        if res:
            conn.execute("DELETE FROM saved_posts WHERE user_id = ? AND post_id = ?", (user_id, post_id))
            conn.commit()
            return "unsave"
        else:
            conn.execute("INSERT INTO saved_posts (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
            conn.commit()
            return "save"
    
def get_saved_posts(user_id):
    """Menampilkan kompilasi seluruh postingan yang diarsipkan oleh user."""
    query = """
        SELECT posts.id, posts.user_id, posts.content, posts.created_at, 
               users.username AS username, users.role AS user_role, communities.name AS comunity_name,
               (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) AS total_likes,
               (SELECT status FROM follows WHERE follower_id = ? AND following_id = posts.user_id) AS follow_status,
               (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id AND likes.user_id = ?) AS is_liked_by_me,
               1 AS is_saved_by_me
        FROM saved_posts
        INNER JOIN posts ON saved_posts.post_id = posts.id
        INNER JOIN users ON posts.user_id = users.id
        INNER JOIN communities ON posts.community_id = communities.id
        WHERE saved_posts.user_id = ?
        ORDER BY saved_posts.created_at DESC;
    """
    with get_db() as conn:
        return conn.execute(query, (user_id, user_id, user_id)).fetchall()

def follow_user(follower_id, following_id):
    """Mengelola relasi permintaan ikuti akun sosial media beserta otomasi alur notifikasi."""
    with get_db() as conn:
        existing = conn.execute("SELECT id, status FROM follows WHERE follower_id = ? AND following_id = ?", (follower_id, following_id)).fetchone()
        if existing:
            follows_id = existing["id"]
            conn.execute("DELETE FROM follows WHERE follower_id = ? AND following_id = ?", (follower_id, following_id))
            conn.execute("DELETE FROM notifications WHERE type = 'follow_request' AND related_id = ?", (follows_id,))
            conn.commit()
            return "deleted"
        else:
            sender = conn.execute("SELECT username FROM users WHERE id = ?", (follower_id,)).fetchone()
            sender_username = sender["username"] if sender else "Seseorang"
            
            cursor = conn.execute("INSERT INTO follows (follower_id, following_id, status) VALUES (?, ?, 'pending')", (follower_id, following_id))
            new_follows_id = cursor.lastrowid
            
            msg = f"{sender_username} mengirimkan permintaan ikuti kepada Anda."
            conn.execute("INSERT INTO notifications (user_id, sender_id, type, message, related_id, is_read) VALUES (?, ?, 'follow_request', ?, ?, 0)",
                         (following_id, follower_id, msg, new_follows_id))
            conn.commit()
            return "inserted"

def get_notifications(user_id):
    """Mengambil seluruh data kotak masuk pemberitahuan/notifikasi milik pengguna."""
    query = """
        SELECT n.*, u.username AS sender_username 
        FROM notifications n
        LEFT JOIN users u ON n.sender_id = u.id
        WHERE n.user_id = ?
        ORDER BY n.created_at DESC
    """
    with get_db() as conn:
        return conn.execute(query, (user_id,)).fetchall()

def process_follow_action(notification_id, follows_id, action):
    """Memproses keputusan aksi konfirmasi persetujuan (Terima/Tolak) relasi pertemanan."""
    with get_db() as conn:
        if action == "accept":
            conn.execute("UPDATE follows SET status = 'accepted' WHERE id = ?", (follows_id,))
            conn.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
            conn.commit()
            return "accept"
        else:
            conn.execute("DELETE FROM follows WHERE id = ?", (follows_id,))
            conn.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
            conn.commit()
            return "decline"

def get_follower_count(user_id):
    """Menghitung total kuantitas angka akun pengikut (follower) terverifikasi."""
    with get_db() as conn:
        res = conn.execute("SELECT COUNT(*) FROM follows WHERE following_id = ? AND status = 'accepted'", (user_id,)).fetchone()
        return res[0] if res else 0

def get_following_count(user_id):
    """Menghitung total kuantitas angka akun entitas yang diikuti (following)."""
    with get_db() as conn:
        res = conn.execute("SELECT COUNT(*) FROM follows WHERE follower_id = ? AND status = 'accepted'", (user_id,)).fetchone()
        return res[0] if res else 0


# ============================================================
# SECTION: MODERATION & METRICS DASHBOARD
# ============================================================
def get_badwords():
    """Mengambil list kumpulan kata kasar."""
    with get_db() as conn:
        return conn.execute("SELECT * FROM badwords").fetchall()
    
def get_badwords_paginated(limit=10, offset=0):
    with get_db() as conn:
        return conn.execute("""
            SELECT *
            FROM badwords
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """, (limit, offset)).fetchall()

def create_badwords(word):
    """Mendaftarkan database blacklist kosakata kasar baru."""
    with get_db() as conn:
        check = conn.execute("SELECT 1 FROM badwords WHERE word=?", (word,)).fetchone()
        if check:
            return "word_exist"
        conn.execute("INSERT INTO badwords (word) VALUES (?)", (word,))
        conn.commit()
        return True

def update_badwords(badword_id, word):
    """Mengubah susunan ejaan kata terlarang terdaftar."""
    with get_db() as conn:
        duplicate = conn.execute("SELECT id FROM badwords WHERE word = ? AND id != ?", (word, badword_id)).fetchone()
        if duplicate:
            return "word_exist"
        conn.execute("UPDATE badwords SET word = ? WHERE id = ?", (word, badword_id))
        conn.commit()
        return True

def delete_badword(badword_id):
    """Menghapus aturan filter kata terlarang dari daftar."""
    with get_db() as conn:
        conn.execute("DELETE FROM badwords WHERE id = ?", (badword_id,))
        conn.commit()
        return True

def create_logs_user(user_id):
    """Mencatat berkas log rekam jejak pelanggaran ucapan tidak senonoh oleh user."""
    with get_db() as conn:
        conn.execute("INSERT INTO user_violation_logs (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return True

def get_dashboard_metrics():
    """Mengekstrak rangkuman seluruh indikator metrik statistik statistik utama aplikasi."""
    metrics = {"total_users": 0, "total_communities": 0, "total_posts": 0, "total_violations": 0}
    with get_db() as conn:
        try:
            metrics["total_users"] = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            metrics["total_communities"] = conn.execute("SELECT COUNT(*) FROM communities").fetchone()[0]
            metrics["total_posts"] = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
            metrics["total_violations"] = conn.execute("SELECT COUNT(*) FROM user_violation_logs").fetchone()[0]
        except Exception as e:
            print(f"Error fetching dashboard metrics: {e}")
        return metrics

def get_recent_violations(limit=5):
    """Menampilkan antrean histori catatan log kasus pelanggaran terbaru."""
    query = """
        SELECT v.id, u.username, v.created_at, u.id 
        FROM user_violation_logs v
        JOIN users u ON v.user_id = u.id
        ORDER BY v.created_at DESC LIMIT ?
    """
    with get_db() as conn:
        return conn.execute(query, (limit,)).fetchall()

def clear_all_violation_logs():
    """Mengosongkan riwayat rekaman seluruh data pelaporan log kejahatan/pelanggaran."""
    with get_db() as conn:
        try:
            conn.execute("DELETE FROM user_violation_logs")
            conn.commit()
            return True
        except Exception:
            return False

def get_user_activity_summary():
    """Menyusun matriks data ringkasan akumulasi performa perilaku keaktifan pengguna."""
    query = """
        SELECT u.id AS user_id, u.username, u.role,
            (SELECT COUNT(*) FROM posts WHERE posts.user_id = u.id) AS total_posts,
            (SELECT COUNT(*) FROM likes WHERE likes.user_id = u.id) AS total_likes_given,
            (SELECT COUNT(*) FROM comments WHERE comments.user_id = u.id) AS total_comments_written,
            (SELECT COUNT(*) FROM user_violation_logs WHERE user_violation_logs.user_id = u.id) AS total_violations
        FROM users u ORDER BY total_posts DESC
    """
    with get_db() as conn:
        return conn.execute(query).fetchall()

def export_metrics_to_csv(metric_type, filename):
    """Mengekspor struktur berkas pelaporan metrik ke format standar file lembar kerja CSV."""
    try:
        dir_name = os.path.dirname(filename)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        # Contoh implementasi penulisan CSV (bisa dikembangkan sesuai kebutuhan)
        if metric_type == 'activity':
            data = get_user_activity_summary()
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['User ID', 'Username', 'Role', 'Posts', 'Likes Given', 'Comments', 'Violations'])
                for row in data:
                    writer.writerow(list(row))
            return True
    except Exception as e:
        print(f"Failed to export CSV: {e}")
        return False


# ============================================================
# SECTION: MAIN EXECUTION TEST
# ============================================================
if __name__ == "__main__":
    # Menjalankan fungsi setup database saat modul dipanggil langsung
    init_db()
    print("Database Berhasil Dikonfigurasi dengan Aman (Best Practice).")