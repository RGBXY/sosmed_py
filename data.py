import sqlite3

def get_db():
    conn = sqlite3.connect("./database/database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    conn.commit()
    
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

def login_user_auth(username):
    conn = get_db()
    res = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return res
