import tkinter as tk
from tkinter import messagebox
from constrants import *

# ============================================================
# SECTION: LOGIC & DATA
# ============================================================
def go_profile(parent, current_user):
    """Pindah ke halaman profil user."""
    from gui.frames.user_profile import UserProfileFrame
    window_parent = parent.winfo_toplevel()
    window_parent.switch_frame(
        UserProfileFrame,
        current_user=current_user
    )

# ============================================================
# SECTION: GUI COMPONENTS
# ============================================================
def main_header(parent, current_user, screen_name):
    """Membuat komponen header untuk tampilan atas aplikasi."""
    
    # Main container buat ngebungkus seluruh elemen header
    main_frame = tk.Frame(parent, bg=bg_white)
    main_frame.pack(side="top", fill="x", anchor="n") 

    # Kontainer dalam biar ada jarak (padding) di sisi kiri dan kanan
    content_frame = tk.Frame(main_frame, bg=bg_white, padx=24)
    content_frame.pack(fill="x", side="top")

    # Judul halaman yang lagi aktif
    tk.Label(
        content_frame, 
        text=screen_name, 
        font=("Poppins", 14, "bold"), 
        bg=bg_white, 
        fg=text_dark,
        pady=16 
    ).pack(side="left")

    # Tombol buat navigasi ke profil user
    btn_profile = tk.Button(
        content_frame, 
        text=f"Profil Pengguna", 
        font=("Poppins", 10, "bold"), 
        bg=bg_main,
        fg=text_dark,
        activebackground=border_col,
        activeforeground=text_dark,
        padx=16,
        pady=6,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: go_profile(parent, current_user)
    )
    btn_profile.pack(side="right", pady=14) 

    # Efek hover biar tombol kerasa lebih hidup
    btn_profile.bind("<Enter>", lambda e: btn_profile.config(bg=border_col))
    btn_profile.bind("<Leave>", lambda e: btn_profile.config(bg=bg_main))

    # Garis pemisah tipis di bawah header
    tk.Frame(main_frame, height=1, bg=border_col).pack(fill="x", side="top")
 
    return main_frame
