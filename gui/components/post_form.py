import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from logic import Comunity_Logic, Post_Logic

def PostForm(parent, current_user, edit_post_data, on_submit):    
    # Main Card Container 
    user_data = current_user
    comunities = Comunity_Logic()
    posts = Post_Logic()
    edit_data = edit_post_data

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
    avatar_frame.pack(side="left") # 
    avatar_frame.pack_propagate(False)
    
    initial_letter = user_data.username[0].upper() if user_data.username else "?"
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
    
    # Username & Comunity
    meta_frame = tk.Frame(info_frame, bg=bg_white)
    meta_frame.pack(anchor="w")
    
    tk.Label(
        meta_frame, 
        text=user_data.username.capitalize(), 
        font=("Poppins", 10, "bold"), 
        bg=bg_white, 
        fg=text_dark
    ).pack(side="left")
    
    # Comunity
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
    lbl_role.pack(side="left", padx=8)
    
    # Body
    body_frame = tk.Frame(card, bg=bg_white, pady=12)
    body_frame.pack(fill="x")
    
    # Label Post Content
    ent_contents = tk.Text(body_frame, height=4, font=("Poppins", 10))
    ent_contents.pack(fill="x")
    
    tk.Frame(card, height=1, bg=border_col).pack(fill="x", pady=(5, 10))
    
    # Footer
    footer_frame = tk.Frame(card, bg=bg_white)
    footer_frame.pack(fill="x")

    def clear_post():
        ent_contents.delete("1.0", tk.END)
        combo_comunity.set("")
        on_submit()

    def submit_post():
        user_id = current_user.id
        comunity_id = get_comunity_id()
        content = ent_contents.get("1.0", tk.END).strip()   

        res = posts.create_posts_logic(user_id, comunity_id, content)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            clear_post()

    def edit_post():
        post_id = edit_data.id
        comunity_id = get_comunity_id()
        content = ent_contents.get("1.0", tk.END).strip()   

        res = posts.edit_post_logic(post_id, content, comunity_id)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            clear_post()
    
    data_comunity = comunities.get_comunity_logic()
    comunity_map = {row.name: row.id for row in data_comunity}
    data_comunity_name = list(comunity_map.keys())
    
    if edit_data:
        btn_edit = tk.Button(
            footer_frame, 
            text="Simpan Perubahan", 
            font=("Poppins", 9, "bold"), 
            bg="#4D65FF", 
            fg=bg_white,
            relief="flat",
            cursor="hand2",
            command=edit_post,
            activebackground=bg_white
        )
        btn_edit.pack(side="left", padx=(0, 15))

        btn_clear = tk.Button(
            footer_frame, 
            text="Cancel", 
            font=("Poppins", 9), 
            bg="#FF4D4D", 
            fg=bg_white,
            relief="flat",
            cursor="hand2",
            command=clear_post,
            activebackground=bg_white
        )
        btn_clear.pack(side="left", padx=(0, 15))
    else:
        btn_post = tk.Button(
            footer_frame, 
            text="Post Konten", 
            font=("Poppins", 9, "bold"), 
            bg=bg_primary, 
            fg=bg_white,
            relief="flat",
            cursor="hand2",
            command=submit_post,
            activebackground=bg_white
        )
        btn_post.pack(side="left", padx=(0, 15))

    combo_comunity = ttk.Combobox(footer_frame, state="readonly", values=data_comunity_name)
    combo_comunity.pack(side="left", padx=(0, 15))

    def get_comunity_id():
        data = combo_comunity.get()
        if not data:
            return None
        return comunity_map[data]
    
    if edit_post_data:
        ent_contents.insert("1.0", edit_post_data.content)
        combo_comunity.set(edit_post_data.comunity_name)
            
    return card