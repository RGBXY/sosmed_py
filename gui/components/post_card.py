import tkinter as tk
from tkinter import messagebox
from logic import Like_Logic, Comment_Logic, Saved_Post_Logic, Follow_Logic, Sensor_Logic
from constrants import *


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class CustomEditDialog(tk.Toplevel):
    """Kelas kustom dialog modal berbasis Toplevel Frame untuk mengubah konten komentar."""

    def __init__(self, parent, title, initial_value=""):
        """Menginisialisasi layout dialog modal kustom dengan gaya desain Hubble."""
        super().__init__(parent)
        self.title(title)
        self.configure(bg=bg_white)

        # Membuat Instance Sensor_Logic
        self.sensor = Sensor_Logic()
        
        # Membuat dialog menjadi modal
        self.transient(parent)
        self.grab_set()
        
        # Mengatur ukuran dan posisi di tengah window utama
        self.geometry("400x180")
        self.resizable(False, False)
        
        self.result = None
        
        tk.Label(
            self, text="Ubah komentar Anda:", font=("Poppins", 10, "bold"), 
            bg=bg_white, fg=text_dark
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        self.entry = tk.Entry(
            self, font=("Poppins", 10), bg=bg_main, fg=text_dark,
            highlightbackground=border_col, highlightthickness=1, relief="flat"
        )
        self.entry.pack(fill="x", padx=20, pady=5, ipady=6)
        self.entry.insert(0, initial_value)
        self.entry.focus_set()
        
        btn_frame = tk.Frame(self, bg=bg_white)
        btn_frame.pack(fill="x", side="bottom", pady=20, padx=20)
        
        tk.Button(
            btn_frame, text="Batal", font=("Poppins", 9), bg=border_col, fg=text_dark,
            relief="flat", cursor="hand2", padx=15, pady=4, command=self.on_cancel
        ).pack(side="right", padx=(10, 0))
        
        tk.Button(
            btn_frame, text="Simpan", font=("Poppins", 9, "bold"), bg=dark, fg=bg_white,
            relief="flat", cursor="hand2", padx=15, pady=4, command=self.on_save
        ).pack(side="right")
        
        self.entry.bind("<Return>", lambda e: self.on_save())
        
        # Menunggu sampai window dialog ini ditutup sebelum melanjutkan baris kode berikutnya
        self.wait_window(self)

    def on_save(self):
        """Menyimpan teks input ke dalam variabel result dan menutup dialog."""
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        """Menutup dialog tanpa menyimpan perubahan data."""
        self.destroy()


# ============================================================
# SECTION: GUI COMPONENTS & FACTORIES
# ============================================================
def CreatePostCard(parent, post_data, current_user, on_liked, on_delete_callback=None, edit_callback=None):   
    """Membuat komponen UI berupa kartu postingan (Post Card) lengkap dengan fitur interaksi sosial."""
    likes = Like_Logic()
    comment_backend = Comment_Logic() 
    saved_backend = Saved_Post_Logic() 
    follow_backend = Follow_Logic() 
    sensor = Sensor_Logic()
        
    initial_count = post_data.total_likes
    already_liked = post_data.is_liked_by_me 
    already_saved = getattr(post_data, 'is_saved_by_me', False) 
    initial_follow_status = getattr(post_data, 'follow_status', None)
    
    comment_state = tk.BooleanVar(value=False)
    
    # Konfigurasi State Warna & Teks Sejak Awal Render 
    if already_liked:
        text_like_awal = f"❤️ {initial_count} Suka"
        warna_like_awal = "#FF4D4D"
    else:
        text_like_awal = f"🖤 {initial_count} Suka"
        warna_like_awal = text_muted

    if already_saved:
        text_save_awal = "🔖 Tersimpan"
        warna_save_awal = "#4D65FF" 
    else:
        text_save_awal = "🔖 Simpan"
        warna_save_awal = text_muted

    if initial_follow_status == "accepted":
        text_follow_awal = "● Mengikuti"
        warna_follow_awal = "#2ECC71"
    elif initial_follow_status == "pending":
        text_follow_awal = "● Menunggu Konfirmasi"
        warna_follow_awal = "#F39C12"
    else:
        text_follow_awal = "● Ikuti Pengguna"
        warna_follow_awal = bg_primary

    # Fungsi Logika Internal
    def likes_logic():
        """Menangani logika klik tombol like dan update total text like."""
        user_id = current_user.id
        post_id = post_data.id
        res = likes.like_logic(user_id, post_id)
        if res["status"] == "like":
            btn_like.config(text=f"❤️ {initial_count + 1} Suka", fg="#FF4D4D") 
            on_liked()
        elif res["status"] == "unlike":
            btn_like.config(text=f"🖤 {initial_count} Suka", fg=text_muted)
            on_liked()

    def saved_logic():
        """Menangani bookmark postingan dan mengubah status tombol simpan."""
        user_id = current_user.id
        post_id = post_data.id
        res = saved_backend.saved_post_logic(user_id, post_id)
        if res["status"] == "save":
            btn_save.config(text="🔖 Tersimpan", fg="#4D65FF")
            messagebox.showinfo("Berhasil", "Postingan disimpan ke bookmark!")
            on_liked()
        elif res["status"] == "unsave":
            btn_save.config(text="🔖 Simpan", fg=text_muted)
            messagebox.showinfo("Berhasil", "Postingan dihapus dari bookmark.")
            on_liked()

    def follow_logic():
        """Mengurus permintaan follow atau unfollow antar pengguna."""
        follower_id = current_user.id
        following_id = post_data.user_id
        res = follow_backend.follow_user_logic(follower_id, following_id)
        if res["status"] == "Success":
            btn_follw.config(text="● Menunggu Konfirmasi", fg="#F39C12")
            messagebox.showinfo(res["message"][0], res["message"][1])
        elif res["status"] == "Unfollowed":
            btn_follw.config(text="● Ikut Pengguna", fg=bg_primary)
            messagebox.showinfo(res["message"][0], res["message"][1])
        else:
            messagebox.showerror(res["message"][0], res["message"][1])

    def submit_comment(entry_widget):
        """Menyaring kata kasar dan mengirim komentar baru ke database."""
        user_id = current_user.id
        comment_text = sensor.sensor_teks(entry_widget.get(), user_id)

        if comment_text == "Tulis Komentar":
            comment_text = ""

        res = comment_backend.comments_logic(current_user.id, post_data.id, comment_text)
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            entry_widget.delete(0, tk.END)
            if hasattr(card, 'list_container') and card.list_container.winfo_exists():
                render_comments(card.list_container)
        elif res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])

    def trigger_edit_comment(comment_id, old_content):
        """Membuka dialog edit komentar dan memperbarui isinya setelah disensor."""
        root_window = parent.winfo_toplevel()
        dialog = CustomEditDialog(root_window, "Edit Komentar", initial_value=old_content)
       
        new_content = sensor.sensor_teks(dialog.result, current_user.id)    
        res = comment_backend.update_comment_logic(comment_id, new_content)

        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            render_comments(card.list_container)
        else:
            messagebox.showerror(res["message"][0], res["message"][1])

    def trigger_delete_comment(comment_id):
        """Menampilkan konfirmasi hapus komentar dan me-refresh daftar komentar."""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus komentar ini?"):
            res = comment_backend.delete_comment_logic(comment_id)
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                render_comments(card.list_container)
            else:
                messagebox.showerror(res["message"][0], res["message"][1])

    def render_comments(container):
        """Menggambar ulang seluruh daftar komentar di dalam widget container."""
        for widget in container.winfo_children():
            widget.destroy()
        try:
            comments_list = comment_backend.get_comments_logic(post_data.id)
        except Exception:
            comments_list = []

        if not comments_list:
            lbl_empty = tk.Label(container, text="💬 No comments yet. Be the first to share your thoughts!", font=("Poppins", 9, "italic"), bg=bg_white, fg=text_muted)
            lbl_empty.pack(anchor="w", pady=12, padx=5)
            return

        for c in comments_list:
            c_id = getattr(c, 'id', None)
            c_user_id = getattr(c, 'user_id', None)
            c_user = getattr(c, 'username', 'User')
            c_text = getattr(c, 'content', '')
            
            item_box = tk.Frame(container, bg=bg_main, padx=14, pady=10)
            item_box.pack(fill="x", anchor="w", pady=4)
            
            item_header = tk.Frame(item_box, bg=bg_main)
            item_header.pack(fill="x", side="top")
            
            lbl_user = tk.Label(item_header, text=f"@{c_user.lower()}", font=("Poppins", 9, "bold"), bg=bg_main, fg=text_dark)
            lbl_user.pack(anchor="w", side="left")
            
            is_owner = (current_user.id == c_user_id)
            is_staff = (current_user.role.lower() in ["admin", "moderator"])
            
            if is_owner or is_staff:
                btn_del_c = tk.Button(
                    item_header, text="Delete", font=("Poppins", 8), bg=bg_main, fg="#FF4D4D",
                    relief="flat", activebackground=bg_main, cursor="hand2", bd=0,
                    command=lambda cid=c_id: trigger_delete_comment(cid)
                )
                btn_del_c.pack(side="right", padx=2)
            
            if is_owner:
                btn_edit_c = tk.Button(
                    item_header, text="Edit", font=("Poppins", 8), bg=bg_main, fg="#4D65FF",
                    relief="flat", activebackground=bg_main, cursor="hand2", bd=0,
                    command=lambda cid=c_id, txt=c_text: trigger_edit_comment(cid, txt)
                )
                btn_edit_c.pack(side="right", padx=2)
            
            lbl_msg = tk.Label(
                item_box, text=c_text, font=("Poppins", 9), bg=bg_main, fg=text_dark, 
                justify="left", wraplength=500, anchor="w"
            )
            lbl_msg.pack(fill="x", anchor="w", pady=(2, 0), side="top")

    def coment_button():
        """Toggle visibilitas area input dan list komponen komentar."""
        if not comment_state.get():
            comment_state.set(True)
            card.comment_ui = tk.Frame(right_content, bg=bg_white, pady=5)
            card.comment_ui.pack(fill="x", side="top", pady=(10, 0))
            
            input_frame = tk.Frame(card.comment_ui, bg=bg_white)
            input_frame.pack(fill="x", pady=(5, 10))
            
            ent_comment = tk.Entry(
                input_frame, font=("Poppins", 9), bg=bg_main, fg=text_dark,
                highlightbackground=border_col, highlightthickness=1, relief="flat"
            )
            ent_comment.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))
            ent_comment.insert(0, "Tulis Komentar")
            ent_comment.bind("<FocusIn>", lambda e: ent_comment.delete(0, tk.END) if ent_comment.get() == "Tulis Komentar" else None)
            ent_comment.bind("<FocusOut>", lambda e: ent_comment.insert(0, "Tulis Komentar.") if ent_comment.get().strip() == "" else None)
            
            btn_send_comment = tk.Button(
                input_frame, text="Tambah", font=("Poppins", 9, "bold"), bg=text_dark, fg=bg_white,
                relief="flat", cursor="hand2", padx=15, pady=4, bd=0,
                command=lambda: submit_comment(ent_comment)
            )
            btn_send_comment.pack(side="right")
            ent_comment.bind("<Return>", lambda e: submit_comment(ent_comment))
            
            card.list_container = tk.Frame(card.comment_ui, bg=bg_white)
            card.list_container.pack(fill="x", expand=True, pady=(5, 0))
            render_comments(card.list_container)
        else:
            comment_state.set(False)
            if hasattr(card, 'comment_ui') and card.comment_ui.winfo_exists():
                card.comment_ui.destroy()

    # UI Render Main Card 
    card = tk.Frame(parent, bg=bg_white, highlightbackground=border_col, highlightthickness=1, padx=16, pady=16)
    card.pack(fill="x", pady=6, padx=20)
    
    left_column = tk.Frame(card, bg=bg_white)
    left_column.pack(side="left", fill="y", anchor="n")
    
    avatar_frame = tk.Frame(left_column, bg="#E2E8F0", width=45, height=45)
    avatar_frame.pack(side="top")  
    avatar_frame.pack_propagate(False)
    
    initial_letter = post_data.username[0].upper() if post_data.username else "?"
    tk.Label(avatar_frame, text=initial_letter, fg=text_dark, bg="#E2E8F0", font=("Poppins", 11, "bold")).pack(expand=True)
    
    right_content = tk.Frame(card, bg=bg_white, padx=12)
    right_content.pack(side="left", fill="both", expand=True)
    
    meta_frame = tk.Frame(right_content, bg=bg_white)
    meta_frame.pack(fill="x", anchor="w")
    
    user_meta_box = tk.Frame(meta_frame, bg=bg_white)
    user_meta_box.pack(side="left", anchor="w")

    name_row = tk.Frame(user_meta_box, bg=bg_white)
    name_row.pack(anchor="w")

    tk.Label(
        name_row, text=post_data.username.capitalize(), 
        font=("Poppins", 10, "bold"), bg=bg_white, fg=text_dark
    ).pack(side="left")
    
    btn_follw = tk.Button(
        name_row, text=text_follow_awal, font=("Poppins", 9, "bold"), 
        bg=bg_white, fg=warna_follow_awal, relief="flat", cursor="hand2", 
        activebackground=bg_white, bd=0, command=follow_logic
    )
    if current_user.id != post_data.user_id:
        btn_follw.pack(side="left", padx=8)

    lbl_community = tk.Label(
        user_meta_box, text=post_data.comunity_name.lower(), font=("Poppins", 8, "bold"), 
        bg=bg_main, fg=bg_secondary, padx=6, pady=1
    )
    lbl_community.pack(anchor="w", pady=(4, 0))
        
    tk.Label(
        meta_frame, text=f"•  {post_data.created_at}", 
        font=("Poppins", 8), bg=bg_white, fg=text_muted
    ).pack(side="right", anchor="n", pady=2)
    
    # Isi Konten Postingan (Body Text)
    body_frame = tk.Frame(right_content, bg=bg_white)
    body_frame.pack(fill="x", anchor="w", pady=(14, 8))
    
    lbl_content = tk.Label(
        body_frame, text=post_data.content, font=("Poppins", 10), bg=bg_white, 
        fg=text_dark, justify="left", anchor="w", wraplength=520
    )
    lbl_content.pack(fill="x", anchor="w")
    
    # Footer Menu Aksi (Likes, Comments, Saves, Action)
    footer_frame = tk.Frame(right_content, bg=bg_white, pady=6)
    footer_frame.pack(fill="x", side="top")
    
    left_actions = tk.Frame(footer_frame, bg=bg_white)
    left_actions.pack(side="left", fill="y")

    btn_like = tk.Button(left_actions, text=text_like_awal, font=("Poppins", 9, "bold"), bg=bg_white, fg=warna_like_awal, relief="flat", cursor="hand2", activebackground=bg_white, bd=0, command=likes_logic)
    btn_like.pack(side="left", padx=(0, 20))

    btn_comment = tk.Button(left_actions, text="💬 Komentar", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_muted, relief="flat", cursor="hand2", activebackground=bg_white, bd=0, command=coment_button)
    btn_comment.pack(side="left", padx=(0, 20))

    btn_save = tk.Button(left_actions, text=text_save_awal, font=("Poppins", 9, "bold"), bg=bg_white, fg=warna_save_awal, relief="flat", cursor="hand2", activebackground=bg_white, bd=0, command=saved_logic)
    btn_save.pack(side="left", padx=(0, 20))
    
    right_actions = tk.Frame(footer_frame, bg=bg_white)
    right_actions.pack(side="right", fill="y")
    
    if current_user.username == post_data.username or current_user.role.lower() in ["admin", "moderator"]:
        btn_delete = tk.Button(right_actions, text="Hapus", font=("Poppins", 9), bg=bg_white, fg="#FF4D4D", relief="flat", cursor="hand2", activebackground=bg_white, bd=0, command=lambda: on_delete_callback(post_data.id))
        btn_delete.pack(side="right", padx=(15, 0))

        btn_edit = tk.Button(right_actions, text="Edit", font=("Poppins", 9), bg=bg_white, fg="#4D65FF", relief="flat", cursor="hand2", activebackground=bg_white, bd=0, command=lambda: edit_callback(post_data))
        btn_edit.pack(side="right")
        
    return card