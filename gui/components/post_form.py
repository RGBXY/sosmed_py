import tkinter as tk
from tkinter import ttk
from constrants import *
from logic import Comunity_Logic

def PostForm(parent, current_user):    
    # Main Card Container (Kotak Putih)
    user_data = current_user
    comunities = Comunity_Logic()

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
    
    initial_letter = user_data.username[0].upper()
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
        text=user_data.username.capitalize(), 
        font=("Poppins", 10, "bold"), 
        bg=bg_white, 
        fg=text_dark
    ).pack()
    
    # Role Badge
    role_color = bg_secondary if user_data.role.lower() == "admin" else text_muted
    lbl_role = tk.Label(
        meta_frame, 
        text=user_data.role.upper(), 
        font=("Poppins", 7, "bold"), 
        bg=border_col, 
        fg=role_color,
        padx=6,
        pady=1
    )
    lbl_role.pack(padx=8)
    
    # ----------------------------------------------------
    # 2. BODY AREA (Konten Postingan)
    # ----------------------------------------------------
    body_frame = tk.Frame(card, bg=bg_white, pady=12)
    body_frame.pack(fill="x")
    
    # Label Post Content (PENTING: wraplength di-set agar teks otomatis turun ke bawah)
    ent_contents = tk.Text(body_frame, height=4)
    ent_contents.pack(fill="x")
    
    # Pembatas Garis Tipis sebelum masuk footer
    tk.Frame(card, height=1, bg=border_col).pack(fill="x", pady=(5, 10))
    
    # ----------------------------------------------------
    # 3. FOOTER AREA (Tombol Aksi)
    # ----------------------------------------------------
    footer_frame = tk.Frame(card, bg=bg_white)
    footer_frame.pack(fill="x")

    comunity_id = None

    def submit_post():
        user_id = current_user.id
        comunity_id = comunity_id
        content = ent_contents.get()   
        
             
    
    # Tombol Like (Dummy)
    btn_post = tk.Button(
        footer_frame, 
        text="Post Konten", 
        font=("Poppins", 9), 
        bg=bg_primary, 
        fg=bg_white,
        relief="flat",
        cursor="hand2",
        activebackground=bg_white
    )
    btn_post.pack(side="left", padx=(0, 15))

    data_comunity = comunities.get_comunity_logic()
    
    comunity_map = {row.name: row.id for row in data_comunity}

    data_comunity_name = list(comunity_map.keys())
    combo_comunity = ttk.Combobox(footer_frame, state="readonly", values=data_comunity_name)
    combo_comunity.pack(side="left", padx=(0, 15))

    def get_comunity_id():
        data = combo_comunity.get()
        return comunity_map["data"]
    
    comunity_id = get_comunity_id()
        
    return card