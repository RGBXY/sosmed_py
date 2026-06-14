import tkinter as tk
from tkinter import messagebox
from constrants import *

def main_header(parent, current_user, screen_name):
    """Membuat dan mengembalikan komponen header universal untuk navigasi dan identitas halaman.

    Args:
        parent: Widget utama tempat header ini akan ditempatkan.
        current_user: Objek user yang sedang aktif login saat ini.
        screen_name (str): Nama halaman yang akan ditampilkan pada judul header.
    """
    def go_profile():
        """Mengarahkan pengguna ke halaman profil dengan mengakses root window secara dinamis."""
        # Melakukan import lokal untuk menghindari dependency bertipe circular/mutar
        from gui.frames.user_profile import UserProfileFrame

        # Mengambil instance root window (Main class) dari hierarki widget Tkinter teratas
        window_parent = parent.winfo_toplevel()
        
        # Memanggil fungsi routing global yang ada di Main class untuk menukar frame halaman
        window_parent.switch_frame(
            UserProfileFrame,
            current_user=current_user
        )

    # Main container untuk seluruh header (sebagai wrapper utama komponen)
    main_frame = tk.Frame(parent, bg=bg_main)
    main_frame.pack(side="top", fill="x", anchor="n") 

    # Kontainer dalam untuk menampung teks judul halaman dan tombol aksi profil
    content_frame = tk.Frame(main_frame, bg=bg_white)
    content_frame.pack(fill="x", side="top")

    # Label Header (Menampilkan identitas teks atau judul halaman saat ini)
    tk.Label(
        content_frame, 
        text=f"{screen_name}", 
        font=("Poppins", 14, "bold"), 
        bg=bg_white, 
        fg=text_dark, 
        height=4, 
        padx=20
    ).pack(side="left")

    # Profile Button (Tombol navigasi untuk masuk ke halaman pengaturan akun user)
    tk.Button(
        content_frame, 
        text="Profile", 
        font=("Poppins", 11), 
        bg=bg_white, 
        fg=text_dark,
        padx=20,
        relief="flat",
        command=go_profile
    ).pack(side="right") 

    # Garis Pembatas (Aksen visual berupa border tipis di bawah area konten header)
    tk.Frame(main_frame, height=2, bg=bg_primary).pack(fill="x", side="top")
 
    return main_frame