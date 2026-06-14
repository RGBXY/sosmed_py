import tkinter as tk
from tkinter import messagebox
from logic import Like_Logic, Comment_Logic, Saved_Post_Logic, Follow_Logic, Sensor_Logic
from constrants import *

class CustomEditDialog(tk.Toplevel):
    """Kelas kustom dialog modal berbasis Toplevel Frame untuk mengubah konten komentar."""

    def __init__(self, parent, title, initial_value=""):
        """Menginisialisasi layout dialog modal kustom dengan gaya desain Hubble."""
        super().__init__(parent)
        self.title(title)
        self.configure(bg=bg_white)

        # Membuat Instance Sensor_Logic
        self.sensor = Sensor_Logic()
        
        # Membuat dialog menjadi modal (fokus penuh, me-lock window utama)
        self.transient(parent)
        self.grab_set()
        
        # Mengatur ukuran dan posisi di tengah window utama
        self.geometry("400x180")
        self.resizable(False, False)
        
        self.result = None
        
        # Label Instruksi
        tk.Label(
            self, text="Ubah komentar Anda:", font=("Poppins", 10, "bold"), 
            bg=bg_white, fg=text_dark
        ).pack(anchor="w", padx=20, pady=(20, 5))
        
        # Entry Input Box
        self.entry = tk.Entry(
            self, font=("Poppins", 10), bg=bg_main, fg=text_dark,
            highlightbackground=border_col, highlightthickness=1, relief="flat"
        )
        self.entry.pack(fill="x", padx=20, pady=5, ipady=6)
        self.entry.insert(0, initial_value)
        self.entry.focus_set()
        
        # Container Tombol Aksi
        btn_frame = tk.Frame(self, bg=bg_white)
        btn_frame.pack(fill="x", side="bottom", pady=20, padx=20)
        
        # Tombol Batal
        tk.Button(
            btn_frame, text="Batal", font=("Poppins", 9), bg=border_col, fg=text_dark,
            relief="flat", cursor="hand2", padx=15, pady=4, command=self.on_cancel
        ).pack(side="right", padx=(10, 0))
        
        # Tombol Simpan
        tk.Button(
            btn_frame, text="Simpan", font=("Poppins", 9, "bold"), bg=bg_primary, fg=bg_white,
            relief="flat", cursor="hand2", padx=15, pady=4, command=self.on_save
        ).pack(side="right")
        
        # Bind tombol Enter untuk menyimpan otomatis
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
    
    # --- Konfigurasi State Warna & Teks Sejak Awal Render ---
    if already_liked:
        text_like_awal = f"❤️ {initial_count} Suka"
        warna_like_awal = "#FF4D4D"
    else:
        text_like_awal = f"🤍 {initial_count} Suka"
        warna_like_awal = text_muted

    if already_saved:
        text_save_awal = "🔖 Disimpan"
        warna_save_awal = "#4D65FF" 
    else:
        text_save_awal = "🔖 Simpan"
        warna_save_awal = text_muted

    if initial_follow_status == "accepted":
        text_follow_awal = "👤 Mengikuti"
        warna_follow_awal = "#2ECC71"
    elif initial_follow_status == "pending":
        text_follow_awal = "⏳ Menunggu"
        warna_follow_awal = "#F39C12"
    else:
        text_follow_awal = "➕ Ikuti"
        warna_follow_awal = text_muted

    # --- Fungsi Logika Internal ---
    def likes_logic():
        """Menangani logika klik tombol Suka, memperbarui database, dan mengubah tampilan warna tombol secara dinamis."""
        user_id = current_user.id
        post_id = post_data.id
        res = likes.like_logic(user_id, post_id)
        if res["status"] == "like":
            btn_like.config(text=f"❤️ {initial_count + 1} Suka", fg="#FF4D4D") 
            on_liked()
        elif res["status"] == "unlike":
            btn_like.config(text=f"🤍 {initial_count} Suka", fg=text_muted)
            on_liked()

    def saved_logic():
        """Menangani logika simpan/hapus postingan dari bookmark dan memunculkan dialog informasi."""
        user_id = current_user.id
        post_id = post_data.id
        res = saved_backend.saved_post_logic(user_id, post_id)
        if res["status"] == "save":
            btn_save.config(text="🔖 Disimpan", fg="#4D65FF")
            messagebox.showinfo("Berhasil", "Postingan disimpan ke bookmark!")
            on_liked()
        elif res["status"] == "unsave":
            btn_save.config(text="🔖 Simpan", fg=text_muted)
            messagebox.showinfo("Berhasil", "Postingan dihapus dari bookmark.")
            on_liked()

    def follow_logic():
        """Menangani relasi mengikuti (follow) antar user dan memperbarui status tombol menjadi Menunggu/Ikuti."""
        follower_id = current_user.id
        following_id = post_data.user_id
        res = follow_backend.follow_user_logic(follower_id, following_id)
        
        if res["status"] == "Success":
            btn_follw.config(text="⏳ Menunggu", fg="#F39C12")
            messagebox.showinfo(res["message"][0], res["message"][1])
        elif res["status"] == "Unfollowed":
            btn_follw.config(text="➕ Ikuti", fg=text_muted)
            messagebox.showinfo(res["message"][0], res["message"][1])
        else:
            messagebox.showerror(res["message"][0], res["message"][1])

    def submit_comment(entry_widget):
        """Menyaring input teks dari sensor badwords, memvalidasi kekosongan, dan mengirim data komentar ke backend."""
        user_id = current_user.id
        comment_text = sensor.sensor_teks(entry_widget.get(), user_id)
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
        """Menampilkan custom frame dialog modal untuk mengubah konten komentar lama milik pengguna."""
        # Menghubungkan dialog baru ke root window utama paling atas
        root_window = parent.winfo_toplevel()
        
        # Memanggil Custom Edit Dialog
        dialog = CustomEditDialog(root_window, "Edit Komentar", initial_value=old_content)
        
        # Memastikan user tidak menutup window langsung atau mengosongkan teks
        if dialog.result is not None:
            if not dialog.result.strip():
                messagebox.showwarning("Peringatan", "Komentar tidak boleh kosong!")
                return
            
            # Logika Sensor: Menyaring kata kasar dari hasil edit komentar baru sebelum dikirim ke backend
            new_content = sensor.sensor_teks(dialog.result, current_user.id)
            
            res = comment_backend.upadate_comment_logic(comment_id, new_content)
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                render_comments(card.list_container)
            else:
                messagebox.showerror(res["message"][0], res["message"][1])

    def trigger_delete_comment(comment_id):
        """Menampilkan konfirmasi sebelum menghapus komentar terpilih dari database."""
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus komentar ini?"):
            res = comment_backend.delete_comment_logic(comment_id)
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                render_comments(card.list_container)
            else:
                messagebox.showerror(res["message"][0], res["message"][1])

    def render_comments(container):
        """Membersihkan dan menggambar ulang seluruh daftar komentar yang terikat pada postingan ini."""
        for widget in container.winfo_children():
            widget.destroy()
        try:
            comments_list = comment_backend.get_comments_logic(post_data.id)
        except Exception:
            comments_list = []

        if not comments_list:
            lbl_empty = tk.Label(container, text="💬 Belum ada komentar. Jadilah yang pertama!", font=("Poppins", 9, "italic"), bg=bg_white, fg=text_muted)
            lbl_empty.pack(anchor="w", pady=10, padx=5)
            return

        for c in comments_list:
            c_id = getattr(c, 'id', None)
            c_user_id = getattr(c, 'user_id', None)
            c_user = getattr(c, 'username', 'User')
            c_text = getattr(c, 'content', '')
            
            item_box = tk.Frame(container, bg="#F8F9FA", padx=12, pady=10, highlightbackground=border_col, highlightthickness=1)
            item_box.pack(fill="x", anchor="w", pady=4)
            
            item_header = tk.Frame(item_box, bg="#F8F9FA")
            item_header.pack(fill="x", side="top")
            
            lbl_user = tk.Label(item_header, text=c_user.capitalize(), font=("Poppins", 9, "bold"), bg="#F8F9FA", fg=text_dark)
            lbl_user.pack(anchor="w", side="left")
            
            is_owner = (current_user.id == c_user_id)
            is_staff = (current_user.role.lower() in ["admin", "moderator"])
            
            if is_owner or is_staff:
                btn_del_c = tk.Button(
                    item_header, text="Hapus", font=("Poppins", 8), bg="#F8F9FA", fg="#FF4D4D",
                    relief="flat", activebackground="#F8F9FA", cursor="hand2",
                    command=lambda cid=c_id: trigger_delete_comment(cid)
                )
                btn_del_c.pack(side="right", padx=2)
            
            if is_owner:
                btn_edit_c = tk.Button(
                    item_header, text="Edit", font=("Poppins", 8), bg="#F8F9FA", fg="#4D65FF",
                    relief="flat", activebackground="#F8F9FA", cursor="hand2",
                    command=lambda cid=c_id, txt=c_text: trigger_edit_comment(cid, txt)
                )
                btn_edit_c.pack(side="right", padx=2)
            
            lbl_msg = tk.Label(
                item_box, text=c_text, font=("Poppins", 9), bg="#F8F9FA", fg=text_dark, 
                justify="left", wraplength=580, anchor="w"
            )
            lbl_msg.pack(fill="x", anchor="w", pady=(4, 0), side="top")

    def coment_button():
        """Bekerja sebagai toggle switch untuk menampilkan atau menyembunyikan area kolom komentar (expand/collapse UI)."""
        if not comment_state.get():
            comment_state.set(True)
            card.comment_ui = tk.Frame(card, bg=bg_white, pady=5)
            card.comment_ui.pack(fill="x", after=footer_frame)
            
            tk.Frame(card.comment_ui, height=1, bg=border_col).pack(fill="x", pady=(10, 10))
            
            input_frame = tk.Frame(card.comment_ui, bg=bg_white)
            input_frame.pack(fill="x", pady=(0, 10))
            
            ent_comment = tk.Entry(
                input_frame, font=("Poppins", 9), bg=bg_main, fg=text_dark,
                highlightbackground=border_col, highlightthickness=1, relief="flat"
            )
            ent_comment.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 10))
            ent_comment.insert(0, "Tulis komentar...")
            ent_comment.bind("<FocusIn>", lambda e: ent_comment.delete(0, tk.END) if ent_comment.get() == "Tulis komentar..." else None)
            ent_comment.bind("<FocusOut>", lambda e: ent_comment.insert(0, "Tulis komentar...") if ent_comment.get().strip() == "" else None)
            
            btn_send_comment = tk.Button(
                input_frame, text="Kirim", font=("Poppins", 9, "bold"), bg=bg_primary, fg=bg_white,
                relief="flat", cursor="hand2", padx=15, pady=4,
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

    # --- UI RENDER MAIN CARD ---
    card = tk.Frame(parent, bg=bg_white, highlightbackground=border_col, highlightthickness=1, padx=20, pady=20)
    card.pack(fill="x", pady=8, padx=20)
    
    header_frame = tk.Frame(card, bg=bg_white)
    header_frame.pack(fill="x")
    
    avatar_frame = tk.Frame(header_frame, bg=bg_primary, width=40, height=40)
    avatar_frame.pack(side="left")  
    avatar_frame.pack_propagate(False)
    initial_letter = post_data.username[0].upper() if post_data.username else "?"
    tk.Label(avatar_frame, text=initial_letter, fg=bg_white, bg=bg_primary, font=("Poppins", 12, "bold")).pack(expand=True)
    
    info_frame = tk.Frame(header_frame, bg=bg_white, padx=12)
    info_frame.pack(side="left", fill="y")
    
    meta_frame = tk.Frame(info_frame, bg=bg_white)
    meta_frame.pack(anchor="w")
    tk.Label(meta_frame, text=post_data.username.capitalize(), font=("Poppins", 10, "bold"), bg=bg_white, fg=text_dark).pack(side="left")
    
    lbl_role = tk.Label(
        meta_frame, text=post_data.comunity_name.upper(), font=("Poppins", 7, "bold"), 
        bg=border_col, fg=bg_secondary, padx=8, pady=2
    )
    lbl_role.pack(side="left", padx=10)
    
    tk.Label(info_frame, text=post_data.created_at, font=("Poppins", 8), bg=bg_white, fg=text_muted).pack(anchor="w", pady=(2, 0))
    
    body_frame = tk.Frame(card, bg=bg_white, pady=15)
    body_frame.pack(fill="x")
    lbl_content = tk.Label(
        body_frame, text=post_data.content, font=("Poppins", 10), bg=bg_white, 
        fg=text_dark, justify="left", anchor="w", wraplength=620
    )
    lbl_content.pack(fill="x", anchor="w")
    
    tk.Frame(card, height=1, bg=border_col).pack(fill="x", pady=(0, 10))
    
    footer_frame = tk.Frame(card, bg=bg_white)
    footer_frame.pack(fill="x")
    
    left_actions = tk.Frame(footer_frame, bg=bg_white)
    left_actions.pack(side="left", fill="y")

    btn_like = tk.Button(left_actions, text=text_like_awal, font=("Poppins", 9, "bold"), bg=bg_white, fg=warna_like_awal, relief="flat", cursor="hand2", activebackground=bg_white, command=likes_logic)
    btn_like.pack(side="left", padx=(0, 15))

    btn_comment = tk.Button(left_actions, text="💬 Komentar", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_muted, relief="flat", cursor="hand2", activebackground=bg_white, command=coment_button)
    btn_comment.pack(side="left", padx=(0, 15))

    btn_save = tk.Button(left_actions, text=text_save_awal, font=("Poppins", 9, "bold"), bg=bg_white, fg=warna_save_awal, relief="flat", cursor="hand2", activebackground=bg_white, command=saved_logic)
    btn_save.pack(side="left", padx=(0, 15))
    
    btn_follw = tk.Button(left_actions, text=text_follow_awal, font=("Poppins", 9, "bold"), bg=bg_white, fg=warna_follow_awal, relief="flat", cursor="hand2", activebackground=bg_white, command=follow_logic)
    if current_user.id != post_data.user_id:
        btn_follw.pack(side="left", padx=(0, 15))

    right_actions = tk.Frame(footer_frame, bg=bg_white)
    right_actions.pack(side="right", fill="y")
    
    if current_user.username == post_data.username or current_user.role.lower() in ["admin", "moderator"]:
        btn_delete = tk.Button(right_actions, text="🗑️ Hapus", font=("Poppins", 9), bg=bg_white, fg="#FF4D4D", relief="flat", cursor="hand2", activebackground=bg_white, command=lambda: on_delete_callback(post_data.id))
        btn_delete.pack(side="right", padx=(15, 0))

        btn_edit = tk.Button(right_actions, text="✏️ Edit", font=("Poppins", 9), bg=bg_white, fg="#4D65FF", relief="flat", cursor="hand2", activebackground=bg_white, command=lambda: edit_callback(post_data))
        btn_edit.pack(side="right")
        
    return card