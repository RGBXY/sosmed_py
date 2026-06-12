import sqlite3

def get_db():
    conn = sqlite3.connect("./database/database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()

    # Create table users
    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )""")
    conn.commit()

    # Create table comunities
    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS comunities(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
                 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )""")
    conn.commit()

    # Create table posts
    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            comunity_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (comunity_id) REFERENCES comunities(id) ON DELETE CASCADE     
        )""")
    conn.commit()

    # Create table likes
    conn.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            
            UNIQUE(user_id, post_id)
        )""")

    # Create table comments
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
    
    # Create table follow
    conn.execute("""
       CREATE TABLE IF NOT EXISTS follows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            follower_id INTEGER NOT NULL,      -- User yang menekan tombol Follow
            following_id INTEGER NOT NULL,     -- User yang mau di-follow
            status TEXT DEFAULT 'pending',     -- Status: 'pending', 'accepted', 'rejected'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (follower_id) REFERENCES users(id),
            FOREIGN KEY (following_id) REFERENCES users(id),
            UNIQUE(follower_id, following_id)
        )""")
    
    # Create table notif
    conn.execute("""
       CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,          -- Penerima notifikasi
            sender_id INTEGER,                 -- Pengirim (bisa NULL jika sistem/admin)
            type TEXT NOT NULL,                -- 'follow_request' atau 'system_info'
            message TEXT NOT NULL,             -- Isi teks pemberitahuan
            related_id INTEGER,                -- ID tambahan (misal: ID dari tabel 'follows')
            is_read INTEGER DEFAULT 0,         -- 0 = belum dibaca, 1 = sudah
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""")
    
    # Create table saved post
    conn.execute("""
       CREATE TABLE IF NOT EXISTS saved_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
        )""")
    
    check_user = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    if check_user[0] == 0:
        data_users = [
            ("admin", "haha1234", "admin"),
            ("budi", "hoho1234", "moderator"),
            ("dodi", "hehe1234", "user"),
        ]
        
        conn.executemany("""
            INSERT INTO users (username, password, role)    
            VALUES (?, ?, ?)
        """, data_users)
        conn.commit()
        
    conn.close()

# User
def cheack_if_user_exist(conn, username):
    check = conn.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone()
    
    if check:
        return "username_exist"
    
    return False

def login_user_auth(username):
    conn = get_db()
    res = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return res

def register_user_auth(username, password):
    conn = get_db()

    try:
        check = cheack_if_user_exist(conn, username) 

        if check == "username_exist":
            conn.close()
            return check
    
        conn.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (username, password, "user"))
        conn.commit()
        
        user_baru = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return user_baru
    except Exception:
        print(f"Error: {Exception}")
    finally:
        conn.close()

def register_admin(username, password, role):
    conn = get_db()

    try:
        check = cheack_if_user_exist(conn, username) 

        if check == "username_exist":
            conn.close()
            return check
    
        conn.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", (username, password, role))
        conn.commit()
    except Exception:
        print(f"Error: {Exception}")
    finally:
        conn.close()

def edit_user(id, username, password, role):
    conn = get_db()

    # Pengecekan duplikasi: Cari tahu apakah ada USER LAIN yang memakai username ini
    # Jika ada user lain (ID berbeda) yang memakai username ini, maka block!
    check_duplicate = conn.execute(
        "SELECT id FROM users WHERE username = ? AND id != ?", 
        (username, id)
    ).fetchone()
    
    if check_duplicate:
        conn.close()
        return "username_exist"  # Ubah jadi username_exist agar sinkron dengan logic kamu

    # Jika admin mengetikkan password baru (password tidak kosong)
    if password and len(password.strip()) > 0:
        conn.execute(
            "UPDATE users SET username=?, password=?, role=? WHERE id=?", 
            (username, password, role, id)
        )
    else:
        # Jika password kosong, UPDATE TANPA mengubah password lama user di DB
        conn.execute(
            "UPDATE users SET username=?, role=? WHERE id=?", 
            (username, role, id)
        )
        
    conn.commit()
    conn.close()
    return True

def change_username(curent_username, new_userame):
    conn = get_db()

    check = cheack_if_user_exist(conn, new_userame) 

    if check == "username_exist":
        conn.close()
        return check

    conn.execute("UPDATE users SET username=? WHERE username=?", (new_userame, curent_username))
    conn.commit()

    data_user = conn.execute("SELECT * FROM users WHERE username = ?", (new_userame,)).fetchone()

    conn.close()
    return data_user

def delete_user(id):
    conn = get_db()

    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()

    conn.close()
    return True

def get_user():
    conn = get_db()

    data_users = conn.execute("SELECT * FROM users").fetchmany(10)

    conn.close()
    return data_users

# Comunity
def create_comunity(user_id, name, description):
    conn = get_db()

    check = conn.execute("SELECT 1 FROM comunities WHERE name=?", (name, )).fetchone()

    if check:
        return "name_exist"
    
    conn.execute("INSERT INTO comunities (user_id, name, description) VALUES (?,?,?)", (user_id, name, description))
    conn.commit()

    new_comunity = conn.execute("SELECT * FROM comunities WHERE name = ?", (name,)).fetchone()

    conn.close()
    return new_comunity

def update_comunity(comunity_id, name, description):
    conn = get_db()

    check = conn.execute("SELECT * FROM comunities WHERE name=?", (name, )).fetchone()

    if check and not check[0] == comunity_id:
        return "name_exist"

    conn.execute(
        "UPDATE comunities SET name = ?, description = ? WHERE id = ?", 
        (name, description, comunity_id)
    )
    conn.commit()
    conn.close()

    return True

def delete_comunity(id):
    conn = get_db()

    conn.execute("DELETE FROM comunities WHERE id=?", (id,))
    conn.commit()

    return True

def get_comunity():
    conn = get_db()
    
    data_comunity = conn.execute("SELECT * FROM comunities").fetchmany(10)
    

    conn.close()
    return data_comunity

def get_comunity_post(id, current_user_id):
    conn = get_db()

    # Gabungkan logika filter komunitas langsung ke query yang lengkap
    data_posts = conn.execute("""
        SELECT 
            posts.id, 
            posts.user_id,
            posts.content, 
            posts.created_at, 
            users.username AS username, 
            users.role AS user_role,
            comunities.name AS comunity_name,
            
            COUNT(likes.post_id) AS total_likes,
            MAX(CASE WHEN likes.user_id = ? THEN 1 ELSE 0 END) AS is_liked_by_me,
            
            (SELECT COUNT(*) FROM saved_posts WHERE saved_posts.post_id = posts.id AND saved_posts.user_id = ?) AS is_saved_by_me,

            (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS total_comments,
                                          
            (SELECT status FROM follows WHERE follower_id = ? AND following_id = posts.user_id) AS follow_status,

            (1.0 / (1.0 + (JULIANDAY('now') - JULIANDAY(posts.created_at)) * 24)) AS recency_weight,
            
            (
                COUNT(likes.post_id) * 2 +
                (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) * 3 +
                (1.0 / (1.0 + (JULIANDAY('now') - JULIANDAY(posts.created_at)) * 24))
            ) AS feed_score
                                
        FROM posts
        INNER JOIN users ON posts.user_id = users.id
        INNER JOIN comunities ON posts.comunity_id = comunities.id
        LEFT JOIN likes ON posts.id = likes.post_id
        
        -- DI SINI KUNCI PERUBAHANNYA: Filter berdasarkan parameter id komunitas
        WHERE posts.comunity_id = ?
        
        GROUP BY posts.id
        
        ORDER BY feed_score DESC;
    """, (current_user_id, current_user_id, current_user_id, id)).fetchmany(10) # PENTING: Tambahkan 'id' di tuple parameter paling belakang

    conn.close()
    
    # Kembalikan data_posts yang sudah difilter dan di-sorting berdasarkan score
    return data_posts

# Post
def create_post(user_id, comunity_id, content):
    conn = get_db()

    conn.execute("INSERT INTO posts (user_id, comunity_id, content) VALUES (?,?,?)", (user_id, comunity_id, content))
    conn.commit()

    conn.close()
    return True

def get_post(current_user_id):
    conn = get_db()
    
    data_posts = conn.execute("""
        SELECT 
            posts.id, 
            posts.user_id, -- Tambahkan ini agar tahu ID pemilik postingan
            posts.content, 
            posts.created_at, 
            users.username AS username, 
            users.role AS user_role,
            comunities.name AS comunity_name,
            
            COUNT(likes.post_id) AS total_likes,
            MAX(CASE WHEN likes.user_id = ? THEN 1 ELSE 0 END) AS is_liked_by_me,
            
            (SELECT COUNT(*) FROM saved_posts WHERE saved_posts.post_id = posts.id AND saved_posts.user_id = ?) AS is_saved_by_me,

            (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) AS total_comments,
            
            -- Tambahkan ini untuk mengambil status follow saat ini
            (SELECT status FROM follows WHERE follower_id = ? AND following_id = posts.user_id) AS follow_status,
            
            (1.0 / (1.0 + (JULIANDAY('now') - JULIANDAY(posts.created_at)) * 24)) AS recency_weight,
            
            (
                COUNT(likes.post_id) * 2 +
                (SELECT COUNT(*) FROM comments WHERE comments.post_id = posts.id) * 3 +
                (1.0 / (1.0 + (JULIANDAY('now') - JULIANDAY(posts.created_at)) * 24))
            ) AS feed_score
                                
        FROM posts
        INNER JOIN users ON posts.user_id = users.id
        INNER JOIN comunities ON posts.comunity_id = comunities.id
        LEFT JOIN likes ON posts.id = likes.post_id
        
        GROUP BY posts.id
        
        ORDER BY feed_score DESC;
    """, (current_user_id, current_user_id, current_user_id)).fetchmany(10) # Parameter ditambah 1 untuk subquery follows

    conn.close()
    return data_posts

def update_post(id, content, comunity_id):
    conn = get_db()

    conn.execute("""
        UPDATE posts SET 
            content = ?, 
            comunity_id = ?
        WHERE id = ?;
    """, (content, comunity_id, id))
    conn.commit()
    conn.close()

    return True

def delete_post(id):
    conn = get_db()

    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()

    conn.close
    return True

# Like
def like(user_id, post_id):
    conn = get_db()
    
    res = conn.execute("SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id)).fetchone()
    
    if res:
        conn.execute("DELETE FROM likes WHERE user_id = ? and post_id = ?", (user_id, post_id))
        conn.commit()
        
        conn.close()
        return "unlike"
    else:
        conn.execute("INSERT INTO likes (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
        conn.commit()
        
        conn.close()
        return "like"
    
# Comment
def comment(user_id, post_id, content):
    conn = get_db()

    conn.execute("INSERT INTO comments (user_id, post_id, content) VALUES (?,?,?)", (user_id, post_id, content))
    conn.commit()

    conn.close()
    return True

def get_comment(post_id):
    conn = get_db()

    query = """
        SELECT 
            comments.id,
            comments.user_id,
            comments.post_id,
            comments.content,
            comments.created_at,
            users.username AS username
        FROM comments
        INNER JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY comments.id ASC;
    """
    
    res = conn.execute(query, (post_id,)).fetchall()

    conn.close()
    return res

def delete_comment(id):
    conn = get_db()

    conn.execute("DELETE FROM comments WHERE id = ?", (id,))
    conn.commit()

    conn.close()
    return True

def update_comment(id, content):
    conn = get_db()

    conn.execute("""
        UPDATE comments SET 
            content = ?
        WHERE id = ?
    """, (content, id))
    conn.commit()
    conn.close()

    return True

# Saved Post
def saved_post(user_id, post_id):
    conn = get_db()
    
    res = conn.execute("SELECT 1 FROM saved_posts WHERE user_id = ? AND post_id = ?", (user_id, post_id)).fetchone()
    
    if res:
        conn.execute("DELETE FROM saved_posts WHERE user_id = ? and post_id = ?", (user_id, post_id))
        conn.commit()
        
        conn.close()
        return "unsave"
    else:
        conn.execute("INSERT INTO saved_posts (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
        conn.commit()
        
        conn.close()
        return "save"
    
def get_saved_posts(user_id):
    conn = get_db()

    query = """
        SELECT 
            posts.id, 
            posts.user_id,
            posts.content, 
            posts.created_at, 
            users.username AS username, 
            users.role AS user_role,
            comunities.name AS comunity_name,
            
            (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id) AS total_likes,
            (SELECT status FROM follows WHERE follower_id = ? AND following_id = posts.user_id) AS follow_status,
            (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.id AND likes.user_id = ?) AS is_liked_by_me,
            1 AS is_saved_by_me
                               
        FROM saved_posts
        INNER JOIN posts ON saved_posts.post_id = posts.id
        INNER JOIN users ON posts.user_id = users.id
        INNER JOIN comunities ON posts.comunity_id = comunities.id
        
        WHERE saved_posts.user_id = ?
        ORDER BY saved_posts.created_at DESC;
    """
    
    res = conn.execute(query, (user_id, user_id, user_id)).fetchall()
    conn.close()
    return res

# Follow
def follow_user(follower_id, following_id):
    conn = get_db()
    try:
        # 1. Cek apakah data follow sudah ada sebelumnya
        existing = conn.execute("""
            SELECT id, status FROM follows 
            WHERE follower_id = ? AND following_id = ?
        """, (follower_id, following_id)).fetchone()
        
        if existing:
            # Ambil ID follows yang mau dihapus
            follows_id = existing["id"]
            
            # 2. Jika SUDAH ADA, lakukan UNFOLLOW (Hapus relasi)
            conn.execute("""
                DELETE FROM follows 
                WHERE follower_id = ? AND following_id = ?
            """, (follower_id, following_id))
            
            # SEKALIGUS hapus notifikasi lamanya agar tidak menumpuk di database
            conn.execute("""
                DELETE FROM notifications 
                WHERE type = 'follow_request' AND related_id = ?
            """, (follows_id,))
            
            conn.commit()
            return "deleted"
            
        else:
            # 3. Jika BELUM ADA, dapatkan data username si pengirim dulu untuk isi pesan
            sender = conn.execute("SELECT username FROM users WHERE id = ?", (follower_id,)).fetchone()
            sender_username = sender["username"] if sender else "Seseorang"
            
            # 4. Jalankan INSERT ke tabel follows
            cursor = conn.execute("""
                INSERT INTO follows (follower_id, following_id, status) 
                VALUES (?, ?, 'pending')
            """, (follower_id, following_id))
            
            # Ambil ID baris yang baru saja dimasukkan (Last Insert ID)
            new_follows_id = cursor.lastrowid
            
            # 5. KUNCI PERUBAHAN: Otomatis buat notifikasi buat si target (following_id)
            pesan_notif = f"{sender_username} mengirimkan permintaan ikuti kepada Anda."
            
            conn.execute("""
                INSERT INTO notifications (user_id, sender_id, type, message, related_id, is_read)
                VALUES (?, ?, 'follow_request', ?, ?, 0)
            """, (following_id, follower_id, pesan_notif, new_follows_id))
            
            conn.commit()
            return "inserted"
            
    except Exception as e:
        print(f"Error pada database: {e}")
        return "error"
    finally:
        conn.close()

# Notification
def get_notifications(user_id):
    conn = get_db()
    
    notif_data = conn.execute("""
        SELECT n.*, 
        u.username AS sender_username 
        FROM notifications n
        LEFT JOIN users u ON n.sender_id = u.id
        WHERE n.user_id = ?
        ORDER BY n.created_at DESC
    """, (user_id,)).fetchall()

    conn.close()
    return notif_data

def process_follow_action(notification_id, follows_id, action):
    conn = get_db()

    try:
        if action == "accept":
            # 1. Update status pertemanan di tabel follows
            conn.execute("UPDATE follows SET status = 'accepted' WHERE id = ?", (follows_id,))
            # 2. Hapus notifikasi request ini karena sudah diproses
            conn.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
            conn.commit()

            return "accept"
        else:
            # Jika ditolak, hapus relasi dari tabel follows dan notifications
            conn.execute("DELETE FROM follows WHERE id = ?", (follows_id,))
            conn.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
            conn.commit()

            return "decline"
        
    except Exception as e:
        return {"status": "Error", "message": f"Gagal: {e}"}
    finally:
        conn.close()

def get_follower_count(user_id):
    conn = get_db()
    try:
        # Menghitung berapa banyak orang yang mem-follow user_id ini
        res = conn.execute("""
            SELECT COUNT(*) FROM follows 
            WHERE following_id = ? AND status = 'accepted'
        """, (user_id,)).fetchone()
        
        return res[0] if res else 0
    except Exception as e:
        print(f"Error count follower: {e}")
        return 0
    finally:
        conn.close()

def get_following_count(user_id):
    conn = get_db()
    try:
        # Menghitung berapa banyak orang yang di-follow oleh user_id ini
        res = conn.execute("""
            SELECT COUNT(*) FROM follows 
            WHERE follower_id = ? AND status = 'accepted'
        """, (user_id,)).fetchone()
        
        return res[0] if res else 0
    except Exception as e:
        print(f"Error count following: {e}")
        return 0
    finally:
        conn.close()
