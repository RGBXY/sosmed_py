import tkinter as tk
from tkinter import messagebox
from constrants import *

def main_header(parent, current_user, screen_name):
    # Main container untuk seluruh header
    main_frame = tk.Frame(parent, bg=bg_main)
    main_frame.pack(side="top", fill="x", anchor="n") # Diubah ke side="top" agar horizontal full di atas

    # 1. Buat kontainer khusus untuk konten (Screen Name & Profile) biar bisa justify-between
    content_frame = tk.Frame(main_frame, bg=bg_white)
    content_frame.pack(fill="x", side="top")

    def go_profile():
        from gui.frames.user_profile import UserProfileFrame

        parent.master.switch_frame(
        UserProfileFrame,
        current_user=current_user
    )

    # KIRI: Screen Name
    tk.Label(
        content_frame, 
        text=f"{screen_name}", 
        font=("Poppins", 14, "bold"), 
        bg=bg_white, 
        fg=text_dark, 
        height=4, 
        padx=20
    ).pack(side="left") # Tarik ke kiri mentok

    # KANAN: Profile
    tk.Button(
        content_frame, 
        text="Profile", 
        font=("Poppins", 11), 
        bg=bg_white, 
        fg=text_dark,
        padx=20,
        relief="flat",
        command=go_profile
    ).pack(side="right") # Tarik ke kanan mentok (Ini kunci "space-between"-nya!)

    # 2. Garis pembagi (Border bawah/Line) ditaruh di bawah content_frame
    tk.Frame(main_frame, height=2, bg=bg_primary).pack(fill="x", side="top")
 
    return main_frame