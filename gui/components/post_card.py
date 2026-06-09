import tkinter as tk
from tkinter import messagebox, simpledialog
from constrants import *
from logic import Like_Logic, Comment_Logic, Saved_Post_Logic 

def CreatePostCard(parent, post_data, current_user, on_liked, on_delete_callback=None, edit_callback=None):   
    likes = Like_Logic()
    comment_backend = Comment_Logic() 
    saved_backend = Saved_Post_Logic() 
        
    initial_count = post_data.total_likes
    already_liked = post_data.is_liked_by_me 
    
    already_saved = getattr(post_data, 'is_saved_by_me', False) 
    
    comment_state = tk.BooleanVar(value=False)
    
    if already_liked:
        text_like_awal = f"❤️ {initial_count} Suka"
        warna_like_awal = "#FF4D4D"
    else:
        text_like_awal = f"🤍 {initial_count} Suka"
        warna_like_awal = text_muted

    # Konfigurasi Awal Tombol Saved Post
    if already_saved:
        text_save_awal = "🔖 Disimpan"
        warna_save_awal = "#4D65FF" 
    else:
        text_save_awal = "🔖 Simpan"
        warna_save_awal = text_muted

    # Fungsi Logika Klik Like
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

    # Fungsi Unsave Post
    def saved_logic():
        user_id = current_user.id
        post_id = post_data.id
        
        res = saved_backend.saved_post_logic(user_id, post_id)
        
        if res["status"] == "save":
            btn_save.config(text="🔖 Disimpan", fg="#4D65FF")
            messagebox.showinfo("Berhasil", "Postingan berhasil disimpan ke bookmark!")
        elif res["status"] == "unsave":
            btn_save.config(text="🗂️ Simpan", fg=text_muted)
            messagebox.showinfo("Berhasil", "Postingan dihapus dari bookmark.")

    def submit_comment(entry_widget):
        comment_text = entry_widget.get().strip()
        if not comment_text or comment_text == "Tulis komentar...":
            messagebox.showwarning("Peringatan", "Komentar tidak boleh kosong!")
            return
        
        res = comment_backend.comments_logic(current_user.id, post_data.id, comment_text)
        
        if res["status"] == "Success":
            entry_widget.delete(0, tk.END)
            if hasattr(card, 'list_container') and card.list_container.winfo_exists():
                render_comments(card.list_container)
        else:
            messagebox.showerror("Gagal", "Gagal mengirim komentar, silakan coba lagi.")

    def trigger_edit_comment(comment_id, old_content):
        new_content = simpledialog.askstring("Edit Komentar", "Ubah komentar Anda:", initialvalue=old_content)
        if new_content is not None: 
            if not new_content.strip():
                messagebox.showwarning("Peringatan", "Komentar tidak boleh kosong!")
                return
            
            try:
                res = comment_backend.upadate_comment_logic(comment_id, new_content)
            except AttributeError:
                print("error")
                return
                
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                render_comments(card.list_container)
            else:
                messagebox.showerror(res["message"][0], res["message"][1])

    def trigger_delete_comment(comment_id):
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus komentar ini?"):
            try:
                res = comment_backend.delete_comment_logic(comment_id)
            except AttributeError:
                print("error")
                return

            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                render_comments(card.list_container)
            else:
                messagebox.showerror(res["message"][0], res["message"][1])

    def render_comments(container):
        for widget in container.winfo_children():
            widget.destroy()
            
        try:
            comments_list = comment_backend.get_comments_logic(post_data.id)
        except Exception:
            try:
                comments_list = Comment_Logic.get_comments_logic(post_data.id)
            except Exception:
                comments_list = []

        if not comments_list:
            lbl_empty = tk.Label(container, text="Belum ada komentar.", font=("Poppins", 9, "italic"), bg=bg_white, fg=text_muted)
            lbl_empty.pack(anchor="w", pady=8, padx=5)
            return

        for c in comments_list:
            c_id = getattr(c, 'id', None)
            c_user_id = getattr(c, 'user_id', None)
            c_user = getattr(c, 'username', 'User')
            c_text = getattr(c, 'content', '')
            
            item_box = tk.Frame(container, bg="#F3F4F6", padx=10, pady=8)
            item_box.pack(fill="x", anchor="w", pady=4)
            
            item_header = tk.Frame(item_box, bg="#F3F4F6")
            item_header.pack(fill="x", side="top")
            
            lbl_user = tk.Label(item_header, text=c_user, font=("Poppins", 9, "bold"), bg="#F3F4F6", fg=bg_primary)
            lbl_user.pack(anchor="w", side="left")
            
            is_owner = (current_user.id == c_user_id)
            is_staff = (current_user.role.lower() in ["admin", "moderator"])
            
            if is_owner or is_staff:
                btn_del_c = tk.Button(
                    item_header, text="Delete", font=("Poppins", 8), bg="#F3F4F6", fg="#FF4D4D",
                    relief="flat", activebackground="#F3F4F6", cursor="hand2",
                    command=lambda cid=c_id: trigger_delete_comment(cid)
                )
                btn_del_c.pack(side="right", padx=2)
            
            if is_owner:
                btn_edit_c = tk.Button(
                    item_header, text="Edit", font=("Poppins", 8), bg="#F3F4F6", fg="#4D65FF",
                    relief="flat", activebackground="#F3F4F6", cursor="hand2",
                    command=lambda cid=c_id, txt=c_text: trigger_edit_comment(cid, txt)
                )
                btn_edit_c.pack(side="right", padx=2)
            
            lbl_msg = tk.Label(
                item_box, text=c_text, font=("Poppins", 9), bg="#F3F4F6", fg=text_dark, 
                justify="left", wraplength=550, anchor="w"
            )
            lbl_msg.pack(fill="x", anchor="w", pady=(2, 0), side="top")

    def coment_button():
        if not comment_state.get():
            comment_state.set(True)

            card.comment_ui = tk.Frame(card, bg=bg_white, pady=5)
            card.comment_ui.pack(fill="x", after=footer_frame)

            tk.Frame(card.comment_ui, height=1, bg=border_col).pack(fill="x", pady=(5, 10))

            input_frame = tk.Frame(card.comment_ui, bg=bg_white)
            input_frame.pack(fill="x", pady=(0, 12))

            ent_comment = tk.Entry(
                input_frame, font=("Poppins", 9), bg=bg_white, fg=text_dark,
                highlightbackground=border_col, highlightthickness=1, relief="flat"
            )
            ent_comment.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 8))
            ent_comment.insert(0, "Tulis komentar...")
            
            ent_comment.bind("<FocusIn>", lambda e: ent_comment.delete(0, tk.END) if ent_comment.get() == "Tulis komentar..." else None)
            ent_comment.bind("<FocusOut>", lambda e: ent_comment.insert(0, "Tulis komentar...") if ent_comment.get().strip() == "" else None)

            card.list_container = tk.Frame(card.comment_ui, bg=bg_white)
            
            btn_send_comment = tk.Button(
                input_frame, text="Kirim", font=("Poppins", 9, "bold"), bg=bg_primary, fg=bg_white,
                relief="flat", cursor="hand2", padx=15, pady=3,
                command=lambda: submit_comment(ent_comment)
            )
            btn_send_comment.pack(side="right")
            ent_comment.bind("<Return>", lambda e: submit_comment(ent_comment))

            card.list_container.pack(fill="x", expand=True, pady=(5, 0))
            render_comments(card.list_container)

        else:
            comment_state.set(False)
            if hasattr(card, 'comment_ui') and card.comment_ui.winfo_exists():
                card.comment_ui.destroy()

    # Main Card Container 
    card = tk.Frame(parent, bg=bg_white, highlightbackground=border_col, highlightthickness=1, padx=20, pady=20)
    card.pack(fill="x", pady=10, padx=20)
    
    # Header
    header_frame = tk.Frame(card, bg=bg_white)
    header_frame.pack(fill="x")
    
    # Mini Avatar
    avatar_frame = tk.Frame(header_frame, bg=bg_primary, width=40, height=40)
    avatar_frame.pack(side="left")  
    avatar_frame.pack_propagate(False)
    
    initial_letter = post_data.username[0].upper() if post_data.username else "?"
    tk.Label(avatar_frame, text=initial_letter, fg=bg_white, bg=bg_primary, font=("Poppins", 12, "bold")).pack(expand=True)
    
    # User Info Container
    info_frame = tk.Frame(header_frame, bg=bg_white, padx=10)
    info_frame.pack(side="left", fill="y")
    
    # Username & Comunity Badge
    meta_frame = tk.Frame(info_frame, bg=bg_white)
    meta_frame.pack(anchor="w")
    
    tk.Label(meta_frame, text=post_data.username, font=("Poppins", 10, "bold"), bg=bg_white, fg=text_dark).pack(side="left")
    
    # Comunity Badge
    lbl_role = tk.Label(meta_frame, text=post_data.comunity_name.upper(), font=("Poppins", 7, "bold"), bg=border_col, fg=bg_secondary, padx=6, pady=1)
    lbl_role.pack(side="left", padx=8)
    
    # Timestamp
    tk.Label(info_frame, text=post_data.created_at, font=("Poppins", 8), bg=bg_white, fg=text_muted).pack(anchor="w")
    
    # Body 
    body_frame = tk.Frame(card, bg=bg_white, pady=12)
    body_frame.pack(fill="x")
    
    lbl_content = tk.Label(body_frame, text=post_data.content, font=("Poppins", 10), bg=bg_white, fg=text_dark, justify="left", anchor="w", wraplength=600)
    lbl_content.pack(fill="x", anchor="w")
    
    # Line
    tk.Frame(card, height=1, bg=border_col).pack(fill="x", pady=(5, 10))
    
    # Footer
    footer_frame = tk.Frame(card, bg=bg_white)
    footer_frame.pack(fill="x")
    
    # Tombol Like
    btn_like = tk.Button(footer_frame, text=text_like_awal, font=("Poppins", 9), bg=bg_white, fg=warna_like_awal, relief="flat", cursor="hand2", activebackground=bg_white, command=likes_logic)
    btn_like.pack(side="left", padx=(0, 15))

    # Tombol Comment
    btn_comment = tk.Button(footer_frame, text="Komentar", font=("Poppins", 9), bg=bg_white, fg=text_muted, relief="flat", cursor="hand2", activebackground=bg_white, command=coment_button)
    btn_comment.pack(side="left", padx=(0, 15))

    # Btn Save
    btn_save = tk.Button(
        footer_frame, 
        text=text_save_awal, 
        font=("Poppins", 9), 
        bg=bg_white, 
        fg=warna_save_awal, 
        relief="flat", 
        cursor="hand2", 
        activebackground=bg_white, 
        command=saved_logic
    )
    btn_save.pack(side="left")
    
    # Btn Delete and Btn Edit
    if current_user.username == post_data.username or current_user.role.lower() == "admin" or current_user.role.lower() == "moderator":
        btn_delete = tk.Button(footer_frame, text="Hapus", font=("Poppins", 9), bg=bg_white, fg="#FF4D4D", relief="flat", cursor="hand2", activebackground=bg_white, command=lambda: on_delete_callback(post_data.id))
        btn_delete.pack(side="right")

        btn_edit = tk.Button(footer_frame, text="Edit", font=("Poppins", 9), bg=bg_white, fg="#4D65FF", relief="flat", cursor="hand2", activebackground=bg_white, command=lambda: edit_callback(post_data))
        btn_edit.pack(side="right")
        
    return card