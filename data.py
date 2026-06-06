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

    
    
    