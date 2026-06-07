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
            role TEXT NOT NULL,
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

def change_username(curent_username, new_userame):
    conn = get_db()

    check = cheack_if_user_exist(conn, new_userame) 

    if check == "username_exist":
        conn.close()
        return check

    conn.execute("UPDATE users SET username=? WHERE username=?", (new_userame, curent_username))
    conn.commit()

    data_user = conn.execute("SELECT * FROM users WHERE username = ?", (new_userame,)).fetchone()

    return data_user

def delete_user(id):
    conn = get_db()

    conn.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()

    return True

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

# Post
def create_post(user_id, comunity_id, content):
    pass    

