# ============================================================
# SECTION: IMPORTS
# ============================================================
import tkinter as tk
from tkinter import messagebox
from constrants import *

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from gui.components.post_card import CreatePostCard  

# Logic
from logic import Saved_Post_Logic  


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class SavedPostFrame(tk.Frame):
    """Frame halaman khusus untuk menampilkan daftar postingan yang telah disimpan/di-bookmark oleh pengguna."""

    def __init__(self, parent, current_user):
        """Menginisialisasi session user, membangun tata letak grid, dan mempersiapkan penampung kartu data."""
        super().__init__(parent, bg=bg_white) 
        self.current_user = current_user
        self.has_scroll = False  
        
        # Setup Sidebar and Header
        render_role_sidebar(self, current_user, "Saved_Post")
        
        # Main Content Container dibuat full di sebelah kanan
        self.main_content = tk.Frame(self, bg=bg_main)  # Menggunakan bg_main agar konsisten dengan Home
        self.main_content.pack(side="right", fill="both", expand=True)
        
        main_header(self.main_content, current_user, "Saved Post")
        
        # Frame pembungkus area scrollable agar padding-nya rapi
        self.feed_area = tk.Frame(self.main_content, bg=bg_main, padx=20, pady=5)
        self.feed_area.pack(fill="both", expand=True)
        
        self._create_scrollable_area()
        self.load_saved_posts()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================

    def load_saved_posts(self):
        """Menarik record data postingan yang di-bookmark dari layer bisnis dan merender kartu konten ke layar."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        try:
            saved_backend = Saved_Post_Logic()
            saved_posts_list = saved_backend.get_saved_posts_logic(self.current_user.id)
        except Exception as e:
            print(f"Error saat mengambil data saved posts: {e}")
            saved_posts_list = []
            
        if not saved_posts_list:
            lbl_empty = tk.Label(
                self.scrollable_frame, 
                text="🗂️ Belum ada postingan yang disimpan.", 
                font=("Poppins", 11, "italic"), 
                bg=bg_main, 
                fg=text_muted
            )
            lbl_empty.pack(pady=40, fill="x", expand=True)
            return

        for post in saved_posts_list:
            setattr(post, 'is_saved_by_me', True)
            
            CreatePostCard(
                parent=self.scrollable_frame,
                post_data=post,
                current_user=self.current_user,
                on_delete_callback=self.handle_delete_post,
                edit_callback=self.handle_edit_post,
                on_liked=self.handle_refresh_likes,
            )
            
    def handle_delete_post(self, post_id):
        """Menampilkan dialog konfirmasi dan memicu penghapusan data postingan asli melalui Post_Logic backend."""
        if messagebox.askyesno("Konfirmasi", "Hapus postingan ini secara permanen?"):
            from logic import Post_Logic
            post_backend = Post_Logic()
            res = post_backend.delete_post_logic(post_id)
            
            if res.get("status") == "Success":
                messagebox.showinfo("Sukses", res.get("message")[1])
                self.load_saved_posts()  
            else:
                messagebox.showerror("Gagal", res.get("message")[1])
            
    def handle_edit_post(self, post_data):
        """Mengarahkan navigasi pengguna kembali ke HomeFrame dengan membawa parameter data untuk disunting."""
        from gui.frames.home import HomeFrame
        self.master.switch_frame(HomeFrame, data_edit=post_data, current_user=self.current_user)
        
    def handle_refresh_likes(self):
        """Callback event ketika interaksi suka (like) dipicu untuk memperbarui informasi status kartu."""
        self.load_saved_posts()

    def _create_scrollable_area(self):
        """Membangun komponen Canvas dan Scrollbar pembungkus feed serta mendaftarkan event handler responsif."""
        scroll_container = tk.Frame(self.feed_area, bg=bg_main)
        scroll_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(scroll_container, bg=bg_main, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_main)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_frame_configure(self, event):
        """Menghitung ulang area scrollregion Canvas dan menyembunyikan scrollbar jika tinggi konten mencukupi."""
        bbox = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=bbox)
        
        content_height = bbox[3] - bbox[1]
        canvas_height = self.canvas.winfo_height()
        
        if content_height <= canvas_height:
            self.scrollbar.pack_forget()
            self.has_scroll = False
        else:
            self.scrollbar.pack(side="right", fill="y")
            self.has_scroll = True

    def on_canvas_configure(self, event):
        """Memaksa lebar window internal frame agar selalu mengikuti perubahan dimensi canvas induknya."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def on_mousewheel(self, event):
        """Menangkap input mousewheel untuk memicu pergeseran halaman yview jika status scroll aktif."""
        if self.canvas.winfo_exists() and getattr(self, 'has_scroll', False):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")