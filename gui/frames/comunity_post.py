import tkinter as tk
from tkinter import messagebox, ttk
from constrants import *

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from gui.components.post_card import CreatePostCard

# Logic
from logic import Community_Logic, Post_Logic


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class ComunityPostFrame(tk.Frame):
    """Frame utama penyedia halaman feed postingan dan manajemen interaksi grup diskusi komunitas."""

    def __init__(self, parent, current_user, comunity_id):
        """Menginisialisasi session user, menarik data relasi komunitas, serta membangun layout feed scrollable."""
        super().__init__(parent, bg=bg_white)
        self.comunities = Community_Logic()
        self.posts = Post_Logic()
        self.current_user = current_user
        self.comunity_id = comunity_id
        self.community_data = None
        self.community_member = None

        # Ambil data detail komunitas saat ini
        try:
            self.community_data = self.comunities.get_community_detail_logic(comunity_id)
            self.community_member = self.comunities.get_community_members_logic(comunity_id)
            community_name = self.community_data.name
        except Exception:
            community_name = "👥 Grup Diskusi"

        # Setup Sidebar & Top Bar Nav
        render_role_sidebar(self, current_user, "Comunity Post")
        main_header(self, current_user, "Community Feed")

        # Main Layout Container
        self.main_content = tk.Frame(self, bg=bg_main)
        self.main_content.pack(side="right", fill="both", expand=True)

        # --- HERO ZONE HEADER ---
        self.hero_section = tk.Frame(self.main_content, bg=bg_white, padx=25, pady=20, highlightbackground=border_col, highlightthickness=1)
        self.hero_section.pack(fill="x", anchor="n")

        title_frame = tk.Frame(self.hero_section, bg=bg_white)
        title_frame.pack(side="left", fill="both", expand=True)

        self.lbl_community_title = tk.Label(title_frame, text=community_name, font=("Poppins", 14, "bold"), bg=bg_white, fg=text_dark)
        self.lbl_community_title.pack(anchor="w")

        # Tombol aksi interaktif untuk melihat daftar anggota kelompok
        btn_view_members = tk.Button(
            title_frame, text="👥 Lihat Daftar Anggota", command=self.open_members_list,
            font=("Poppins", 9, "underline"), bg=bg_white, fg="#2563EB", relief="flat", activebackground=bg_white, cursor="hand2"
        )
        btn_view_members.pack(anchor="w", pady=(2, 0))

        # Kontrol Aksi Sisi Kanan (Join/Leave & Postingan)
        self.action_top_frame = tk.Frame(self.hero_section, bg=bg_white)
        self.action_top_frame.pack(side="right", fill="y", padx=(10, 0))

        self.render_action_buttons()

        # --- FEED SCOPE ---
        self.render_scrollable_area()
        self.handle_form_success()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================
    def render_action_buttons(self):
        """Merender ulang tombol kontrol aksi di pojok kanan atas berdasarkan status keanggotaan pengguna."""
        for widget in self.action_top_frame.winfo_children():
            widget.destroy()

        self.is_member = self.comunities.check_membership_logic(self.comunity_id, self.current_user.id)

        # 1. Tombol Buat Postingan Baru
        btn_create_post = tk.Button(
            self.action_top_frame, text="✍️ Buat Postingan", command=self.go_to_create_post,
            font=("Poppins", 9, "bold"), bg=bg_primary, fg=bg_white, relief="flat", padx=15, pady=8, cursor="hand2"
        )
        btn_create_post.pack(side="right", padx=(10, 0))

        # 2. Tombol Dinamis Join / Leave
        
        if not self.community_data.user_id == self.current_user.id:
            if self.is_member:
                btn_status = tk.Button(
                    self.action_top_frame, text="Leave Group", command=lambda: self.toggle_membership_detail("leave"),
                    font=("Poppins", 9, "bold"), bg="#F3F4F6", fg="#4B5563", relief="flat", padx=15, pady=8, cursor="hand2"
                )
            else:
                btn_status = tk.Button(
                    self.action_top_frame, text="➕ Join Group", command=lambda: self.toggle_membership_detail("join"),
                    font=("Poppins", 9, "bold"), bg="#0284C7", fg=bg_white, relief="flat", padx=15, pady=8, cursor="hand2"
                )
            btn_status.pack(side="right", padx=(10, 0))

        # 3. Tombol Kembali
        btn_back_hub = tk.Button(
            self.action_top_frame, text="🔙 Hub", command=self.back_to_community_hub,
            font=("Poppins", 9, "bold"), bg=bg_main, fg=text_dark, relief="flat", padx=15, pady=8, cursor="hand2"
        )
        btn_back_hub.pack(side="right")

    def go_to_create_post(self):
        """Membuka jendela pop-up modal form untuk membuat kiriman artikel baru khusus bagi anggota terdaftar."""
        if not self.is_member:
            messagebox.showwarning("Akses Ditolak", "Kamu harus bergabung (Join) menjadi member komunitas ini terlebih dahulu sebelum bisa mengirim postingan!")
            return

        from gui.components.post_form_window import PostFormWindow
        
        PostFormWindow(
            parent_frame=self,
            current_user=self.current_user,
            forced_community_id=self.comunity_id, 
            on_submit_callback=self.handle_form_success 
        )

    def handle_edit_post(self, post_data):
        """Membuka modal penyuntingan kiriman dengan memuat ulang parameter teks lama postingan target."""
        from gui.components.post_form_window import PostFormWindow
        
        PostFormWindow(
            parent_frame=self,
            current_user=self.current_user,
            edit_post_data=post_data,
            forced_community_id=self.comunity_id,
            on_submit_callback=self.handle_form_success
        )

    def open_members_list(self):
        """Memicu pembuatan jendela Toplevel baru untuk melihat profil seluruh member aktif grup ini."""
        CommunityMembersWindow(self, self.comunity_id, self.community_data)

    def handle_form_success(self):
        """Menarik ulang data kiriman dari layer database dan memperbarui tumpukan kartu konten feed."""
        data = self.comunities.get_comunity_post_logic(self.comunity_id, self.current_user.id)
        self.load_cards(data)

    def toggle_membership_detail(self, action):
        """Menangani proses pendaftaran masuk atau keluar dari ekosistem member grup komunitas."""
        if action == "join":
            res = self.comunities.join_community_logic(self.comunity_id, self.current_user.id)
        else:
            user_res = messagebox.askyesno("Keluar Grup", "Yakin ingin meninggalkan grup diskusi ini?")
            if not user_res: return
            res = self.comunities.leave_community_logic(self.comunity_id, self.current_user.id)

        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.render_action_buttons()
            self.handle_form_success()
        else:
            messagebox.showerror(res["message"][0], res["message"][1])

    def render_scrollable_area(self):
        """Membangun area Canvas dan Scrollbar pembungkus kartu postingan agar halaman bisa digulir vertikal."""
        scroll_container = tk.Frame(self.main_content, bg=bg_main)
        scroll_container.pack(fill="both", expand=True, padx=(25, 40), pady=15)

        self.canvas = tk.Canvas(scroll_container, bg=bg_main, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.card_container = tk.Frame(self.canvas, bg=bg_main)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.card_container, anchor="nw")

        self.card_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.canvas_window, width=event.width))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") if self.canvas.winfo_exists() else None)

    def load_cards(self, data):
        """Mengosongkan kontainer feed lama dan menyusun tumpukan komponen PostCard secara repetitif."""
        for widget in self.card_container.winfo_children():
            widget.destroy()

        if not data:
            empty_feed = tk.Frame(self.card_container, bg=bg_main)
            empty_feed.pack(expand=True, fill="both", pady=60)
            tk.Label(empty_feed, text="💬", font=("Poppins", 28), bg=bg_main).pack()
            tk.Label(empty_feed, text="Belum ada postingan di sini. Yuk, bagikan ide pertamamu!", font=("Poppins", 10, "italic"), bg=bg_main, fg=text_muted).pack(pady=8)
            return

        for post in data:
            CreatePostCard(
                parent=self.card_container, post_data=post, current_user=self.current_user,
                on_delete_callback=self.on_delete, edit_callback=self.handle_edit_post, on_liked=self.handle_refresh_likes
            )

    def back_to_community_hub(self):
        """Mengalihkan frame aktif kontainer master kembali menuju halaman sentral pusat komunitas."""
        from gui.frames.comunity import ComunityFrame
        self.master.switch_frame(ComunityFrame, current_user=self.current_user)

    def on_delete(self, id):
        """Menghapus data kiriman postingan dari record sistem berdasarkan id unik yang dipasok."""
        if messagebox.askyesno("Hapus Kiriman", "Apakah Anda yakin ingin menghapus postingan ini?"):
            res = self.posts.delete_post_logic(id)
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.handle_form_success()
            else:
                messagebox.showerror(res["message"][0], res["message"][1])

    def handle_refresh_likes(self):
        """Metode perantara callback event untuk menyegarkan tampilan status like."""
        self.handle_form_success()


class CommunityMembersWindow(tk.Toplevel):
    """Pop-up modal sub-jendela modern untuk menginspeksi jajaran keanggotaan grup diskusi."""
    
    def __init__(self, parent_frame, community_id, community_data):
        """Menginisialisasi konfigurasi geometri modal dialog penampil daftar nama user."""
        super().__init__(parent_frame)
        self.parent_frame = parent_frame
        self.comunities = parent_frame.comunities
        
        self.title("Anggota Komunitas")
        self.configure(bg=bg_white)
        self.resizable(False, False)
        self.grab_set()

        width, height = 400, 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Top Banner Title
        top_frame = tk.Frame(self, bg=bg_white, padx=20, pady=15)
        top_frame.pack(fill="x")
        
        tk.Label(top_frame, text="👥 Anggota Grup", font=("Poppins", 12, "bold"), bg=bg_white, fg=text_dark).pack(anchor="w")
        tk.Label(top_frame, text="Daftar pengguna aktif yang tergabung dalam ruang ini.", font=("Poppins", 8), bg=bg_white, fg=text_muted).pack(anchor="w")
        
        tk.Frame(self, height=1, bg=border_col).pack(fill="x", padx=20)

        # Scrollable Member List Area
        list_container = tk.Frame(self, bg=bg_main, padx=15, pady=10)
        list_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_container, bg=bg_main, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        scroll_content = tk.Frame(canvas, bg=bg_main)
        canvas_window = canvas.create_window((0, 0), window=scroll_content, anchor="nw")

        scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(canvas_window, width=event.width))

        # Muat data baris relasi anggota
        self.load_member_rows(scroll_content, community_id, community_data)

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================

    def load_member_rows(self, container, community_id, community_data):
        """Menarik record dari database dan mencetak kartu nama anggota beserta badge jabatan."""
        members_list = self.comunities.get_community_members_logic(community_id)
        creator_id = community_data.user_id

        if not members_list:
            tk.Label(container, text="Grup ini belum memiliki anggota aktif.", font=("Poppins", 9, "italic"), bg=bg_main, fg=text_muted).pack(pady=40)
            return
            
        for row in members_list:
            member_id = row.id
            member_username = row.username

            row_frame = tk.Frame(container, bg=bg_white, padx=12, pady=10, highlightbackground=border_col, highlightthickness=1)
            row_frame.pack(fill="x", pady=4)

            # Informasi Akun Anggota
            lbl_user = tk.Label(row_frame, text=f"👤 {member_username}", font=("Poppins", 10, "bold" if member_id == creator_id else "normal"), bg=bg_white, fg=text_dark)
            lbl_user.pack(side="left")

            if member_id == creator_id:
                badge_admin = tk.Label(
                    row_frame, text="👑 Admin Grup", font=("Poppins", 7, "bold"), 
                    bg="#FEF3C7", fg="#D97706", padx=6, pady=2
                )
                badge_admin.pack(side="left", padx=8)
            else:
                badge_member = tk.Label(
                    row_frame, text="Member", font=("Poppins", 7), 
                    bg="#F3F4F6", fg="#6B7280", padx=6, pady=2
                )
                badge_member.pack(side="left", padx=8)