import tkinter as tk
from tkinter import messagebox, ttk
from constrants import * # Membawa konstanta warna: bg_white, bg_primary, bg_secondary, text_dark, dll.

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

# Import backend logic
from logic import (
    get_dashboard_metrics, 
    get_recent_violations, 
    clear_all_violation_logs,
    User_Profile # Kelas backend untuk memproses perubahan username dan delete user
)

class DashboardAdminFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white)
        
        self.user_profile_backend = User_Profile()
        self.current_user = current_user
        
        # Variabel untuk menyimpan data user pelanggar yang sedang dipilih dari tabel
        self.selected_target_user = None 
        
        # Render Sidebar & Header bawaan proyek
        render_role_sidebar(self, current_user, "Dashboard_Admin")
        main_header(self, current_user, "Dashboard")  
        
        # --- MAIN FRAME CONTAINER ---
        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True)
        
        self.content_frame = tk.Frame(main_frame, bg=bg_white, pady=25)
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.content_frame.pack_configure(padx=(20, 40))
        
        # Render seluruh komponen UI Utama
        self.render_dashboard_view()

    def render_dashboard_view(self):
        metrics = get_dashboard_metrics()
        recent_logs = get_recent_violations(limit=5)
        
        self.create_stats_cards(metrics)
        self.create_main_grid(recent_logs)

    def create_stats_cards(self, metrics):
        cards_data = [
            {"title": "Total Users", "value": metrics.get("total_users", 0), "color": "#3B82F6"},
            {"title": "Communities", "value": metrics.get("total_communities", 0), "color": "#10B981"},
            {"title": "Total Posts", "value": metrics.get("total_posts", 0), "color": "#F59E0B"},
            {"title": "Violations Log", "value": metrics.get("total_violations", 0), "color": "#EF4444"}
        ]
        
        cards_container = tk.Frame(self.content_frame, bg=bg_white)
        cards_container.pack(fill="x", pady=(0, 20))
        
        for i, card in enumerate(cards_data):
            card_frame = tk.Frame(cards_container, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB")
            card_frame.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 16, 0))
            
            accent_bar = tk.Frame(card_frame, bg=card["color"], height=4)
            accent_bar.pack(fill="x", side="top")
            
            pad_inner = tk.Frame(card_frame, bg=bg_white, padx=20, pady=18)
            pad_inner.pack(fill="both", expand=True)
            
            lbl_title = tk.Label(pad_inner, text=card["title"].upper(), font=("Poppins", 9, "bold"), fg="#9CA3AF", bg=bg_white)
            lbl_title.pack(anchor="w")
            
            lbl_value = tk.Label(pad_inner, text=f"{card['value']:,}", font=("Poppins", 24, "bold"), fg=text_dark, bg=bg_white)
            lbl_value.pack(anchor="w", pady=(8, 0))

    def create_main_grid(self, recent_logs):
        grid_container = tk.Frame(self.content_frame, bg=bg_white)
        grid_container.pack(fill="both", expand=True, pady=(10, 0))
        
        left_col = tk.Frame(grid_container, bg=bg_white)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.build_violations_table(left_col, recent_logs)
        
        right_col = tk.Frame(grid_container, bg=bg_white)
        right_col.pack(side="right", fill="y", anchor="n")
        self.build_quick_actions_panel(right_col)

    def build_violations_table(self, parent_frame, recent_logs):
        lbl_table_title = tk.Label(parent_frame, text="🔒 5 Pelanggaran Terakhir (Badwords Log)", 
                                   font=("Poppins", 12, "bold"), fg=text_dark, bg=bg_white)
        lbl_table_title.pack(anchor="w", pady=(0, 10))
        
        table_border_frame = tk.Frame(parent_frame, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB")
        table_border_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview.Heading", background=bg_primary, foreground=bg_white, font=("Poppins", 10, "bold"), bd=0, relief="flat")
        style.configure("Treeview", background=bg_white, foreground=text_dark, fieldbackground=bg_white, rowheight=35, font=("Poppins", 9))
        style.map("Treeview", background=[("selected", bg_secondary)])
        
        columns = ("id", "username", "timestamp")
        self.tree = ttk.Treeview(table_border_frame, columns=columns, show="headings", selectmode="browse", height=5)
        
        self.tree.heading("id", text="LOG ID")
        self.tree.heading("username", text="USERNAME PELANGGAR")
        self.tree.heading("timestamp", text="WAKTU KEJADIAN")
        
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("username", width=180, anchor="w")
        self.tree.column("timestamp", width=220, anchor="center")
        
        # Mapping row log pelanggar ke treeview
        for row in recent_logs:
            # Menyimpan data asli row database ke dalam iid/values item
            self.tree.insert("", "end", values=(row["id"], row["username"], row["created_at"]))
            
        scrollbar = ttk.Scrollbar(table_border_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        # --- EVENT DETECTION KETIKA ROW TABEL DIKLIK ---
        self.tree.bind("<<TreeviewSelect>>", self.on_table_row_selected)

    def build_quick_actions_panel(self, parent_frame):
        lbl_action_title = tk.Label(parent_frame, text="🛠️ Panel Kontrol", 
                                    font=("Poppins", 12, "bold"), fg=text_dark, bg=bg_white)
        lbl_action_title.pack(anchor="w", pady=(0, 10))
        
        panel_card = tk.Frame(parent_frame, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB", padx=20, pady=20)
        panel_card.pack(fill="x", anchor="n")
        
        lbl_desc = tk.Label(panel_card, text="Pintasan utilitas sistem untuk memantau data secara real-time.", 
                            font=("Poppins", 9), fg="#6B7280", bg=bg_white, wraplength=180, justify="left")
        lbl_desc.pack(anchor="w", pady=(0, 20))
        
        btn_refresh = tk.Button(panel_card, text="🔄  Refresh Data", font=("Poppins", 10, "bold"),
                                bg="#3B82F6", fg="white", activebackground="#2563EB", activeforeground="white",
                                bd=0, height=2, cursor="hand2", command=self.refresh_dashboard)
        btn_refresh.pack(fill="x", pady=(0, 12))
        
        btn_clear_logs = tk.Button(panel_card, text="🗑️  Clear Badword Logs", font=("Poppins", 10, "bold"),
                                   bg="#FEE2E2", fg="#EF4444", activebackground="#FCA5A5", activeforeground="#991B1B",
                                   bd=0, height=2, cursor="hand2", command=self.clear_logs)
        btn_clear_logs.pack(fill="x", pady=(0, 12))   

        # --- SEPARATOR LINE ---
        separator = tk.Frame(panel_card, bg="#E5E7EB", height=1)
        separator.pack(fill="x", pady=10)

        # --- AREA MANAJEMEN USER PELANGGAR (TARGET) ---
        # Label dinamis penanda user mana yang sedang dikunci/diklik
        self.lbl_target_info = tk.Label(panel_card, text="Pilih user pada tabel untuk mengelola", 
                                        font=("Poppins", 9, "italic"), fg="#9CA3AF", bg=bg_white)
        self.lbl_target_info.pack(anchor="w", pady=(5, 12))

        # Tombol aksi manajemen: Awalnya di-set STATE DISABLED (tidak bisa diklik sebelum tabel dipilih)
        self.btn_change_username = tk.Button(panel_card, text="👤  Ubah Username User", font=("Poppins", 9, "bold"),
                                        bg="#F3F4F6", fg=text_dark, activebackground="#E5E7EB", activeforeground=text_dark,
                                        bd=0, height=2, state="disabled", command=self.popup_ganti_username_target)
        self.btn_change_username.pack(fill="x", pady=(0, 12))

        self.btn_delete_account = tk.Button(panel_card, text="❌  Hapus Akun Pelanggar", font=("Poppins", 9, "bold"),
                                       bg="#FFF7ED", fg="#EA580C", activebackground="#FFEDD5", activeforeground="#C2410C",
                                       bd=0, height=2, state="disabled", command=self.aksi_hapus_akun_target)
        self.btn_delete_account.pack(fill="x")

    # --- LOGIKA EVENT BINDING ---
    def on_table_row_selected(self, event):
        """Memicu perubahan tombol panel kontrol saat salah satu row tabel diklik"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        # Ambil data dari baris yang diklik
        item_values = self.tree.item(selected_item[0], "values")
        log_id = item_values[0]
        target_username = item_values[1]
        
        # PROTEKSI: Cek apakah user yang diklik adalah akun admin itu sendiri
        if target_username == self.current_user.username:
            messagebox.showwarning("Akses Ditolak", "Anda tidak diperbolehkan memanipulasi atau menghapus akun Anda sendiri!")
            self.tree.selection_remove(selected_item) # Reset pilihan klik di tabel
            self.reset_action_buttons()
            return
        
        # Jika lolos validasi, simpan target ke state frame
        self.selected_target_user = {
            "log_id": log_id,
            "username": target_username
            # Catatan: Jika query get_recent_violations menyertakan user_id asli dari DB, 
            # Anda bisa memasukkannya ke kolom treeview tersembunyi/ditampilkan untuk dipakai di delete_user_logic.
        }
        
        # Aktifkan tombol & ubah teks info target pelapor
        self.lbl_target_info.config(text=f"Target: {target_username} (Log #{log_id})", fg="#1E40AF", font=("Poppins", 9, "bold"))
        self.btn_change_username.config(state="normal", cursor="hand2")
        self.btn_delete_account.config(state="normal", cursor="hand2")

    def reset_action_buttons(self):
        """Mengembalikan tombol kontrol ke mode terkunci (disabled)"""
        self.selected_target_user = None
        self.lbl_target_info.config(text="Pilih user pada tabel untuk mengelola", fg="#9CA3AF", font=("Poppins", 9, "italic"))
        self.btn_change_username.config(state="disabled", cursor="")
        self.btn_delete_account.config(state="disabled", cursor="")

    # --- EKSEKUSI LOGIKA USER_PROFILE TARGET ---
    def popup_ganti_username_target(self):
        if not self.selected_target_user:
            return
            
        popup = tk.Toplevel(self)
        popup.title("Ubah Username Pelanggar")
        popup.geometry("350x200")
        popup.configure(bg=bg_white)
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        current_target = self.selected_target_user["username"]

        tk.Label(popup, text=f"Ubah Username: {current_target}", font=("Poppins", 10, "bold"), bg=bg_white, fg=text_dark).pack(pady=15)
        
        form_frame = tk.Frame(popup, bg=bg_white)
        form_frame.pack(fill="x", padx=20)

        ent_new_username = tk.Entry(form_frame, font=("Poppins", 10), bd=1, relief="solid")
        ent_new_username.pack(fill="x", pady=5)
        ent_new_username.focus_set()

        def submit_username():
            new_input = ent_new_username.get().strip()
            # Eksekusi fungsi backend: Mengubah nama user target (bukan admin)
            res = self.user_profile_backend.change_username_logic(current_target, new_input)

            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1], parent=popup)
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1], parent=popup)
                popup.destroy()
                self.refresh_dashboard()

        btn_save = tk.Button(popup, text="Update Username", font=("Poppins", 9, "bold"), bg=bg_primary, fg="white",
                             bd=0, width=15, height=2, command=submit_username)
        btn_save.pack(pady=15)

    def aksi_hapus_akun_target(self):
        if not self.selected_target_user:
            return
            
        target_name = self.selected_target_user["username"]
        
        konfirmasi = messagebox.askyesno("Hapus Akun Pengguna", 
                                         f"Apakah Anda yakin ingin menghapus akun '{target_name}' secara permanen?\nSemua log pelanggarannya juga akan ikut bersih.")
        if konfirmasi:
            # PANGGIL BACKEND: Gunakan ID atau Username sesuai parameter sistem backend Anda.
            # Jika backend Anda delete_user_logic(id) membutuhkan ID User asli, 
            # pastikan log_id/user_id diteruskan ke sini dengan benar.
            res = self.user_profile_backend.delete_user_logic(target_name) 

            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.refresh_dashboard()

    # --- UTILITY MANAGEMENT ---
    def refresh_dashboard(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.render_dashboard_view()
        self.reset_action_buttons() # Kembalikan tombol ke keadaan disabled setelah refresh
        messagebox.showinfo("Sukses", "Data dashboard berhasil diperbarui!")

    def clear_logs(self):
        confirm = messagebox.askyesno("Konfirmasi Tindakan", "Apakah Anda yakin ingin menghapus seluruh log pelanggaran pengguna?")
        if confirm:
            sukses = clear_all_violation_logs()
            if sukses:
                self.refresh_dashboard()
                messagebox.showinfo("Sukses", "Semua log pelanggaran berhasil dibersihkan.")
            else:
                messagebox.showerror("Error", "Gagal membersihkan log dari database.")