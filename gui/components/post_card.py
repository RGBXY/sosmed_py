import tkinter as tk
from tkinter import messagebox
from constrants import *


def CreatePostCard(parent, post_data, current_user, on_delete_callback, edit_callback):   
    # Main Card Container (Kotak Putih)
    card = tk.Frame(
        parent, 
        bg=bg_white, 
        highlightbackground=border_col, 
        highlightthickness=1,
        padx=20,
        pady=20
    )
    card.pack(fill="x", pady=10, padx=20)
    
    # ----------------------------------------------------
    # 1. HEADER AREA (Avatar, Username, Role, Timestamp)
    # ----------------------------------------------------
    header_frame = tk.Frame(card, bg=bg_white)
    header_frame.pack(fill="x")
    
    # Mini Avatar
    avatar_frame = tk.Frame(header_frame, bg=bg_primary, width=40, height=40)
    avatar_frame.pack(side="left") # Ilustrasi margin
    avatar_frame.pack(side="left")
    avatar_frame.pack_propagate(False)
    
    initial_letter = post_data.username[0].upper() if post_data.username else "?"
    tk.Label(
        avatar_frame, 
        text=initial_letter, 
        fg=bg_white, 
        bg=bg_primary, 
        font=("Poppins", 12, "bold")
    ).pack(expand=True)
    
    # User Info Container (Samping Avatar)
    info_frame = tk.Frame(header_frame, bg=bg_white, padx=10)
    info_frame.pack(side="left", fill="y")
    
    # Username & Role Badge (Horizontal)
    meta_frame = tk.Frame(info_frame, bg=bg_white)
    meta_frame.pack(anchor="w")
    
    tk.Label(
        meta_frame, 
        text=post_data.username, 
        font=("Poppins", 10, "bold"), 
        bg=bg_white, 
        fg=text_dark
    ).pack(side="left")
    
    # Role Badge
    role_color = bg_secondary
    lbl_role = tk.Label(
        meta_frame, 
        text=post_data.comunity_name.upper(), 
        font=("Poppins", 7, "bold"), 
        bg=border_col, 
        fg=role_color,
        padx=6,
        pady=1
    )
    lbl_role.pack(side="left", padx=8)
    
    # Timestamp
    tk.Label(
        info_frame, 
        text=post_data.created_at, 
        font=("Poppins", 8), 
        bg=bg_white, 
        fg=text_muted
    ).pack(anchor="w")
    
    # ----------------------------------------------------
    # 2. BODY AREA (Konten Postingan)
    # ----------------------------------------------------
    body_frame = tk.Frame(card, bg=bg_white, pady=12)
    body_frame.pack(fill="x")
    
    # Label Post Content (PENTING: wraplength di-set agar teks otomatis turun ke bawah)
    lbl_content = tk.Label(
        body_frame, 
        text=post_data.content, 
        font=("Poppins", 10), 
        bg=bg_white, 
        fg=text_dark,
        justify="left",
        anchor="w",
        wraplength=600 # Sesuaikan dengan perkiraan lebar area content di aplikasi lu
    )
    lbl_content.pack(fill="x", anchor="w")
    
    # Pembatas Garis Tipis sebelum masuk footer
    tk.Frame(card, height=1, bg=border_col).pack(fill="x", pady=(5, 10))
    
    # ----------------------------------------------------
    # 3. FOOTER AREA (Tombol Aksi)
    # ----------------------------------------------------
    footer_frame = tk.Frame(card, bg=bg_white)
    footer_frame.pack(fill="x")
    
    # Tombol Like (Dummy)
    btn_like = tk.Button(
        footer_frame, 
        text="❤️ Suka", 
        font=("Poppins", 9), 
        bg=bg_white, 
        fg=text_muted,
        relief="flat",
        cursor="hand2",
        activebackground=bg_white
    )
    btn_like.pack(side="left", padx=(0, 15))
    
    # Tombol Comment (Dummy)
    btn_comment = tk.Button(
        footer_frame, 
        text="💬 Komentar", 
        font=("Poppins", 9), 
        bg=bg_white, 
        fg=text_muted,
        relief="flat",
        cursor="hand2",
        activebackground=bg_white
    )
    btn_comment.pack(side="left")
    
    # TOMBOL HAPUS: Hanya muncul jika user yang login adalah pemilik post, ATAU user adalah Admin
    if current_user.username == post_data.username or current_user.role.lower() == "admin" or current_user.role.lower() == "moderator":
        btn_delete = tk.Button(
            footer_frame, 
            text="🗑️ Hapus", 
            font=("Poppins", 9), 
            bg=bg_white, 
            fg="#FF4D4D", # Warna merah cerah untuk hapus
            relief="flat",
            cursor="hand2",
            activebackground=bg_white,
            command=lambda: on_delete_callback(post_data.id)
        )
        btn_delete.pack(side="right")

        btn_edit = tk.Button(
            footer_frame, 
            text="Edit", 
            font=("Poppins", 9), 
            bg=bg_white, 
            fg="#4D65FF", # Warna merah cerah untuk hapus
            relief="flat",
            cursor="hand2",
            activebackground=bg_white,
            command=lambda: edit_callback(post_data)
        )
        btn_edit.pack(side="right")
        
    return card