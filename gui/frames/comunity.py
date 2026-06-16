import tkinter as tk
from tkinter import messagebox, ttk
from constrants import *

from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

from logic import Community_Logic 


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class ComunityFrame(tk.Frame):
    """Frame hub utama untuk menjelajahi daftar komunitas, mendaftar keanggotaan, dan mengelola ruang diskusi."""

    def __init__(self, parent, current_user):
        """Menginisialisasi layout hub komunitas, tombol pembuatan grup baru, dan memicu pemuatan kartu data."""
        super().__init__(parent, bg=bg_white)
        self.comunities = Community_Logic()
        self.current_user = current_user

        # Setup Sidebar & Main Header
        render_role_sidebar(self, current_user, "Comunity")
        main_header(self, current_user, "Komunitas")

        # Main Container
        self.main_content = tk.Frame(self, bg=bg_main)
        self.main_content.pack(side="right", fill="both", expand=True)

        # --- TOP HEADER HUB ---
        top_bar = tk.Frame(self.main_content, bg=bg_main)
        top_bar.pack(fill="x", padx=25, pady=(20, 10))

        lbl_explore = tk.Label(
            top_bar, text="🌐 Jelajahi Komunitas", 
            font=("Poppins", 13, "bold"), bg=bg_main, fg=text_dark
        )
        lbl_explore.pack(side="left", anchor="w")

        btn_trigger_create = tk.Button(
            top_bar, text="➕ Buat Komunitas Baru", 
            command=self.open_create_community_window,
            font=("Poppins", 9, "bold"), bg=dark, fg=bg_white, 
            relief="flat", padx=15, pady=8, cursor="hand2"
        )
        btn_trigger_create.pack(side="right")
        btn_trigger_create.bind("<Enter>", lambda e: btn_trigger_create.config(bg=bg_secondary))
        btn_trigger_create.bind("<Leave>", lambda e: btn_trigger_create.config(bg=dark))

        tk.Frame(self.main_content, height=1, bg=border_col).pack(fill="x", padx=25, pady=(5, 10))

        self.render_scrollable_area()
        self.refresh_page_data()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================
    def refresh_page_data(self):
        """Menarik ulang list record seluruh komunitas dari database untuk didistribusikan ke generator komponen."""
        data = self.comunities.get_comunity_logic()
        self.load_cards(data)

    def open_create_community_window(self):
        """Membuka jendela pop-up modal sub-form dengan konfigurasi pembuatan entitas komunitas baru."""
        CommunityFormWindow(self, title="Buat Komunitas Baru", is_edit=False)

    def open_edit_community_window(self, community_row):
        """Membuka jendela pop-up modal sub-form dengan menyuntikkan data record lama untuk proses penyuntingan."""
        CommunityFormWindow(self, title="Edit Komunitas Anda", is_edit=True, data=community_row)

    def hapus_komunitas(self, community_id):
        """Mengeksekusi penghapusan records data komunitas secara permanen dari sistem berdasarkan id parameter."""
        user_res = messagebox.askyesno("Hapus Komunitas", "Apakah Anda yakin ingin menghapus komunitas ini secara permanen?")
        if user_res:
            res = self.comunities.delete_comunity_logic(community_id) 
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.refresh_page_data()
            else:
                messagebox.showerror(res["message"][0], res["message"][1])

    def toggle_membership(self, community_id, action):
        """Menangani logika pendaftaran (join) atau pembatalan keanggotaan (leave) pengguna pada komunitas tertentu."""
        if action == "join":
            res = self.comunities.join_community_logic(community_id, self.current_user.id)
        else:
            user_res = messagebox.askyesno("Keluar Komunitas", "Apakah Anda yakin ingin meninggalkan komunitas ini?")
            if not user_res: return
            res = self.comunities.leave_community_logic(community_id, self.current_user.id)

        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.refresh_page_data()
        else:
            messagebox.showerror(res["message"][0], res["message"][1])

    def render_scrollable_area(self):
        """Membangun sistem scroll view vertikal memanfaatkan komponen Canvas dan Scrollbar bawaan Tkinter."""
        scroll_container = tk.Frame(self.main_content, bg=bg_main)
        scroll_container.pack(fill="both", expand=True, padx=(25, 40), pady=(0, 20))

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
        """Mengosongkan kontainer lama dan merender ulang jajaran kartu box komunitas beserta proteksi hak akses fiturnya."""
        for widget in self.card_container.winfo_children():
            widget.destroy()

        if not data:
            empty_frame = tk.Frame(self.card_container, bg=bg_main)
            empty_frame.pack(expand=True, fill="both", pady=80)
            tk.Label(empty_frame, text="📭", font=("Poppins", 32), bg=bg_main).pack()
            tk.Label(
                empty_frame, text="Belum ada komunitas yang dibuat.",
                font=("Poppins", 10, "italic"), bg=bg_main, fg=text_muted
            ).pack(pady=5)
            return

        for row in data:
            # FILTER HILANGKAN GLOBAL FEED
            if row.name.strip().lower() == "global feed":
                continue

            card = tk.Frame(
                self.card_container, bg=bg_white,
                highlightbackground=border_col, highlightthickness=1,
                padx=20, pady=18
            )
            card.pack(fill="x", pady=6)

            info_frame = tk.Frame(card, bg=bg_white)
            info_frame.pack(side="left", fill="both", expand=True)

            tk.Label(
                info_frame, text=f"👥 {row.name}",
                font=("Poppins", 11, "bold"), bg=bg_white, fg=text_dark
            ).pack(anchor="w")

            tk.Label(
                info_frame, text=row.description,
                font=("Poppins", 10), bg=bg_white, fg=text_muted, 
                wraplength=450, justify="left"
            ).pack(anchor="w", pady=(6, 0))

            action_frame = tk.Frame(card, bg=bg_white)
            action_frame.pack(side="right", fill="y", padx=(15, 0))

            # --- LOGIKA TOMBOL JOIN / LEAVE DINAMIS ---
            is_joined = self.comunities.check_membership_logic(row.id, self.current_user.id)

            # Validasi Akses Modifikasi (Hanya Creator/Admin/Moderator Global)
            if self.current_user.id == row.user_id or self.current_user.role.lower() in ["admin", "moderator"]:
                btn_edit = tk.Button(
                    action_frame, text="Edit", command=lambda r=row: self.open_edit_community_window(r),
                    font=("Poppins", 9, "bold"), bg=bg_white, fg=text_muted, relief="flat", cursor="hand2"
                )
                btn_edit.pack(side="left", padx=4)

                btn_delete = tk.Button(
                    action_frame, text="Hapus", command=lambda r=row: self.hapus_komunitas(r.id),
                    font=("Poppins", 9, "bold"), bg=bg_white, fg="#EF4444", relief="flat", cursor="hand2"
                )
                btn_delete.pack(side="left", padx=4)

            # Komunitas Biasa (Bisa Join/Leave normal jika bukan pemilik komunitas)
            if not row.user_id == self.current_user.id:
                if is_joined:
                    btn_join_action = tk.Button(
                        action_frame, text="Leave", command=lambda r=row: self.toggle_membership(r.id, r.user_id, "leave"),
                        font=("Poppins", 9, "bold"), bg="#F3F4F6", fg="#6B7280", 
                        relief="flat", padx=10, pady=6, cursor="hand2"
                    )
                else:
                    btn_join_action = tk.Button(
                        action_frame, text="Join", command=lambda r=row: self.toggle_membership(r.id, r.user_id, "join"),
                        font=("Poppins", 9, "bold"), bg="#E0F2FE", fg="#0369A1", 
                        relief="flat", padx=10, pady=6, cursor="hand2"
                    )
                btn_join_action.pack(side="left", padx=4)

            btn_view = tk.Button(
                action_frame, text="Buka Komunitas ➔", command=lambda r=row: self.set_detail_post(r.id),
                font=("Poppins", 9, "bold"), bg=bg_main, fg="#2563EB", 
                relief="flat", padx=12, pady=6, cursor="hand2"
            )
            btn_view.pack(side="left", anchor="center", padx=4)

    def set_detail_post(self, id):
        """Mengalihkan frame utama aplikasi menuju halaman feed postingan internal grup diskusi."""
        from gui.frames.comunity_post import ComunityPostFrame
        self.master.switch_frame(ComunityPostFrame, current_user=self.current_user, comunity_id=id)


class CommunityFormWindow(tk.Toplevel):
    """Sub-jendela pop-up modal dialog untuk menangani form pengisian data pendaftaran maupun revisi informasi komunitas."""
    
    def __init__(self, parent_frame, title, is_edit=False, data=None):
        """Menginisialisasi rancangan geometri modal dialog penangkap nilai parameter input form teks."""
        super().__init__(parent_frame)
        self.parent_frame = parent_frame
        self.is_edit = is_edit
        self.data = data

        self.title(title)
        self.configure(bg=bg_white)
        self.resizable(False, False)
        self.grab_set()

        width, height = 450, 280
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        container = tk.Frame(self, bg=bg_white, padx=25, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text=title, font=("Poppins", 12, "bold"), bg=bg_white, fg=text_dark).pack(anchor="w", pady=(0, 15))

        tk.Label(container, text="Nama Komunitas", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark).pack(anchor="w", pady=(5, 2))
        self.ent_name = tk.Entry(container, font=("Poppins", 10), bg=bg_main, relief="flat", highlightbackground=border_col, highlightthickness=1)
        self.ent_name.pack(fill="x", ipady=6, pady=(0, 10))

        tk.Label(container, text="Deskripsi Singkat", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark).pack(anchor="w", pady=(5, 2))
        self.ent_deskripsi = tk.Entry(container, font=("Poppins", 10), bg=bg_main, relief="flat", highlightbackground=border_col, highlightthickness=1)
        self.ent_deskripsi.pack(fill="x", ipady=6, pady=(0, 20))

        btn_container = tk.Frame(container, bg=bg_white)
        btn_container.pack(fill="x")

        submit_text = "Simpan Perubahan" if is_edit else "Tambah Komunitas"
        submit_command = self.eksekusi_edit if is_edit else self.eksekusi_tambah

        self.btn_submit = tk.Button(btn_container, text=submit_text, command=submit_command, font=("Poppins", 9, "bold"), bg=dark, fg=bg_white, relief="flat", padx=15, pady=6, cursor="hand2")
        self.btn_submit.pack(side="right", padx=(10, 0))

        btn_cancel = tk.Button(btn_container, text="Batal", command=self.destroy, font=("Poppins", 9), bg=bg_main, fg=text_dark, relief="flat", padx=15, pady=6, cursor="hand2")
        btn_cancel.pack(side="right")

        if is_edit and data:
            self.ent_name.insert(0, data.name)
            self.ent_deskripsi.insert(0, data.description)

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================

    def eksekusi_tambah(self):
        """Mengirim parameter isian kolom entitas teks menuju layer database bisnis untuk merekam komunitas baru."""
        user_id = self.parent_frame.current_user.id
        nama = self.ent_name.get().strip()
        deskripsi = self.ent_deskripsi.get().strip()
        res = self.parent_frame.comunities.create_comunity_logic(user_id, nama, deskripsi)
        self.handle_response(res)

    def eksekusi_edit(self):
        """Mengirim parameter teks revisi kolom menuju sistem repositori backend untuk memperbarui record lama."""
        nama = self.ent_name.get().strip()
        deskripsi = self.ent_deskripsi.get().strip()
        res = self.parent_frame.comunities.update_comunity_logic(self.data.id, nama, deskripsi) 
        self.handle_response(res)

    def handle_response(self, res):
        """Memvalidasi response map pasca transaksi query eksekusi bisnis dan menyegarkan frame induk."""
        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1], parent=self)
        else:
            messagebox.showinfo(res["message"][0], res["message"][1], parent=self)
            self.parent_frame.refresh_page_data()
            self.destroy()