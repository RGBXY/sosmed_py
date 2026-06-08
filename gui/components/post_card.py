import tkinter as tk
from tkinter import messagebox
from constrants import *
from logic import Like_Logic

def CreatePostCard(parent, post_data, current_user, on_delete_callback, edit_callback, on_liked):   
    likes = Like_Logic()
    
    print(post_data.total_likes)
    
    initial_count = post_data.total_likes
    already_liked = post_data.is_liked_by_me 
    
    if already_liked:
        text_awal = f"❤️ {initial_count} Suka"
        warna_awal = "#FF4D4D"
    else:
        text_awal = f"🤍 {initial_count} Suka"
        warna_awal = text_muted

    def likes_logic():
        user_id = current_user.id
        post_id = post_data.id
        
        res = likes.like_logic(user_id, post_id)
        
        if res["status"] == "like":
            btn_like.config(text=f"❤️ {initial_count} Suka", fg="#FF4D4D") 
            on_liked()

        elif res["status"] == "unlike":
            btn_like.config(text=f"🤍 {initial_count} Suka", fg=text_muted)
            on_liked()
        
        print(res)
    
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
    
    # Header
    header_frame = tk.Frame(card, bg=bg_white)
    header_frame.pack(fill="x")
    
    # Mini Avatar
    avatar_frame = tk.Frame(header_frame, bg=bg_primary, width=40, height=40)
    avatar_frame.pack(side="left")  #
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
    
    # User Info Container
    info_frame = tk.Frame(header_frame, bg=bg_white, padx=10)
    info_frame.pack(side="left", fill="y")
    
    # Username & Comunity Badge
    meta_frame = tk.Frame(info_frame, bg=bg_white)
    meta_frame.pack(anchor="w")
    
    tk.Label(
        meta_frame, 
        text=post_data.username, 
        font=("Poppins", 10, "bold"), 
        bg=bg_white, 
        fg=text_dark
    ).pack(side="left")
    
    # Comunity Badge
    lbl_role = tk.Label(
        meta_frame, 
        text=post_data.comunity_name.upper(), 
        font=("Poppins", 7, "bold"), 
        bg=border_col, 
        fg=bg_secondary,
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
    
    # Body (Konten Postingan)
    body_frame = tk.Frame(card, bg=bg_white, pady=12)
    body_frame.pack(fill="x")
    
    # Label Post Content 
    lbl_content = tk.Label(
        body_frame, 
        text=post_data.content, 
        font=("Poppins", 10), 
        bg=bg_white, 
        fg=text_dark,
        justify="left",
        anchor="w",
        wraplength=600 #
    )
    lbl_content.pack(fill="x", anchor="w")
    
    # Pembatas Garis Tipis sebelum masuk footer
    tk.Frame(card, height=1, bg=border_col).pack(fill="x", pady=(5, 10))
    
    # Footer
    footer_frame = tk.Frame(card, bg=bg_white)
    footer_frame.pack(fill="x")
    
    # Tombol Like (Sekarang dinamis menggunakan text_awal dan warna_awal)
    btn_like = tk.Button(
        footer_frame, 
        text=text_awal, 
        font=("Poppins", 9), 
        bg=bg_white, 
        fg=warna_awal,
        relief="flat",
        cursor="hand2",
        activebackground=bg_white,
        command=likes_logic
    )
    btn_like.pack(side="left", padx=(0, 15))
    
    # Tombol Comment
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
    
    # Tombol Hapus
    if current_user.username == post_data.username or current_user.role.lower() == "admin" or current_user.role.lower() == "moderator":
        btn_delete = tk.Button(
            footer_frame, 
            text="🗑️ Hapus", 
            font=("Poppins", 9), 
            bg=bg_white, 
            fg="#FF4D4D",
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
            fg="#4D65FF",
            relief="flat",
            cursor="hand2",
            activebackground=bg_white,
            command=lambda: edit_callback(post_data)
        )
        btn_edit.pack(side="right")
        
    return card