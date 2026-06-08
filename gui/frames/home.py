import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.post_form import PostForm
from gui.components.header import main_header
from gui.components.post_card import CreatePostCard
from gui.utils.navigation import render_role_sidebar
from logic import Post_Logic

class HomeFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.post = Post_Logic()
        self.post_data = self.post.get_posts_logic()
        self.post_data_edit = None

        render_role_sidebar(self, current_user, "Home")

        right_container = tk.Frame(self, bg=bg_main)
        right_container.pack(side="left", fill="both", expand=True)
        
        main_header(right_container, current_user, "Home")

        self.feed_area = tk.Frame(right_container, bg=bg_main, padx=20, pady=20)
        self.feed_area.pack(fill="both", expand=True, side="left")

        self.form_container = tk.Frame(self.feed_area, bg=bg_main)
        self.form_container.pack(fill="x", anchor="n")

        side_content = tk.Frame(right_container, bg=bg_main, padx=20, pady=20)
        side_content.pack(fill="both", expand=True, side="left")

        tk.Label(side_content, text="galo").pack()

        # Memanggil fungsi render_post_form milik class
        self.render_post_form()

        # =========================================================================
        # PERBAIKAN 2: Setup Canvas & Scrollbar untuk area postingan
        # =========================================================================
        # Wadah utama pembungkus scroll
        scroll_container = tk.Frame(self.feed_area, bg=bg_main)
        scroll_container.pack(fill="both", expand=True, pady=(15, 0))

        # Canvas tempat menampung data yang bisa digeser
        self.canvas = tk.Canvas(scroll_container, bg=bg_main, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Batang scrollbar di sisi kanan canvas
        self.scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Wadah internal asli (self.container_posts) dimasukkan ke dalam Canvas
        self.container_posts = tk.Frame(self.canvas, bg=bg_main)
        
        # Masukkan Frame ke dalam window Canvas agar bisa di-scroll
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container_posts, anchor="nw")

        # Flag internal untuk mengontrol izin scroll roda mouse
        self.has_scroll = False

        # Hubungkan fungsi untuk menyesuaikan lebar dan area scroll otomatis saat ada data baru
        self.container_posts.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Aktifkan scroll menggunakan mouse wheel (Roda Mouse)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        # =========================================================================

        self.load_data()

    # =========================================================================
    # FUNGSI-FUNGSI UTAMA SEKARANG BERADA DI LEVEL CLASS (DENGAN INDENTASI BENAR)
    # =========================================================================
    def render_post_form(self):
        """Fungsi pembantu untuk memuat ulang komponen PostForm"""
        for item in self.form_container.winfo_children():
            item.destroy()
            
        # Gambar ulang PostForm dengan data edit terbaru (bisa berupa None atau Objek Post)
        PostForm(self.form_container, self.current_user, self.post_data_edit, on_submit=self.load_data)

    def update(self, post_data):
        self.post_data_edit = post_data
        # Setelah variabel diisi, picu fungsi di atas agar form berubah jadi mode edit!
        self.render_post_form()

    def load_data(self):
        # Setiap kali data selesai di-submit/load, kembalikan status edit ke None
        self.post_data_edit = None
        if hasattr(self, 'form_container'):
            self.render_post_form()
            
        for item in self.container_posts.winfo_children():
            item.destroy()
            
        post_data = self.post.get_posts_logic()
       
        for post in post_data:
            CreatePostCard(
                self.container_posts, 
                post, 
                self.current_user, 
                on_delete_callback=self.on_delete,
                edit_callback=self.update
            )

    # =========================================================================
    # FUNGSI HELPER UNTUK SYSTEM SCROLLBAR
    # =========================================================================
    def on_frame_configure(self, event):
        """Memperbarui area scroll dan menyembunyikannya jika data sedikit"""
        bbox = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=bbox)
        
        # Logika pembatas: Cek apakah tinggi konten melebihi tinggi layar jendela canvas
        content_height = bbox[3] - bbox[1]
        canvas_height = self.canvas.winfo_height()
        
        if content_height <= canvas_height:
            self.scrollbar.pack_forget() # Sembunyikan scrollbar jika data cuma 1 atau sedikit
            self.has_scroll = False      # Kunci roda mouse agar tidak bisa scroll naik-turun kosong
        else:
            self.scrollbar.pack(side="right", fill="y") # Tampilkan kembali jika data penuh
            self.has_scroll = True

    def on_canvas_configure(self, event):
        """Memastikan lebar postingan melebar mengikuti ukuran layar aplikasi"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        """Membantu user agar bisa scroll pakai roda mouse (hanya jika data penuh)"""
        if self.canvas.winfo_exists() and getattr(self, 'has_scroll', False):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_delete(self, id):
        res_user = messagebox.askyesno("Delete Post", "Yakin anda ingin menghapus data?")

        if res_user:
            res = self.post.delete_post_logic(id)
            
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
                
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.load_data()