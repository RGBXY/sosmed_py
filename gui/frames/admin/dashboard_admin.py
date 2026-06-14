import csv  # Pustaka bawaan untuk menulis format file CSV
import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog  # Menambahkan filedialog untuk simpan dokumen
from constrants import * # Membawa konstanta warna: bg_white, bg_primary, bg_secondary, text_dark, dll.

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

# Import backend logic
from logic import (
    get_dashboard_metrics, 
    get_recent_violations, 
    clear_all_violation_logs,
    get_user_activity_summary,
    export_metrics_to_csv,
    User_Profile # Kelas backend untuk memproses perubahan username dan delete user
)

class DashboardAdminFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white)
        
        self.user_profile_backend = User_Profile()
        self.current_user = current_user
        
        # Variabel untuk menyimpan data user pelanggar yang sedang dipilih dari tabel log
        self.selected_target_user = None 
        
        # Render Sidebar & Header bawaan proyek
        render_role_sidebar(self, current_user, "Dashboard_Admin")
        main_header(self, current_user, "Dashboard")  
        
        # --- MAIN FRAME CONTAINER ---
        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True)
        
        self.content_frame = tk.Frame(main_frame, bg=bg_white, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.content_frame.pack_configure(padx=(20, 40))
        
        # Render seluruh komponen UI Utama
        self.render_dashboard_view()

    def render_dashboard_view(self):
        # Ambil data statistik dari backend
        metrics = get_dashboard_metrics()
        
        # 1. Bagian Atas: Ringkasan Kartu Statistik (Selalu Terlihat)
        self.create_stats_cards(metrics)
        
        # 2. Bagian Bawah: Penataan Tabular (Notebook) untuk Mengakomodasi Semua Fungsi Baru
        self.create_dashboard_tabs()

    def create_stats_cards(self, metrics):
        cards_data = [
            {"title": "Total Users", "value": metrics.get("total_users", 0), "color": "#3B82F6"},
            {"title": "Communities", "value": metrics.get("total_communities", 0), "color": "#10B981"},
            {"title": "Total Posts", "value": metrics.get("total_posts", 0), "color": "#F59E0B"},
            {"title": "Violations Log", "value": metrics.get("total_violations", 0), "color": "#EF4444"}
        ]
        
        cards_container = tk.Frame(self.content_frame, bg=bg_white)
        cards_container.pack(fill="x", pady=(0, 15))
        
        for i, card in enumerate(cards_data):
            card_frame = tk.Frame(cards_container, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB")
            card_frame.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 16, 0))
            
            accent_bar = tk.Frame(card_frame, bg=card["color"], height=4)
            accent_bar.pack(fill="x", side="top")
            
            pad_inner = tk.Frame(card_frame, bg=bg_white, padx=20, pady=15)
            pad_inner.pack(fill="both", expand=True)
            
            lbl_title = tk.Label(pad_inner, text=card["title"].upper(), font=("Poppins", 9, "bold"), fg="#9CA3AF", bg=bg_white)
            lbl_title.pack(anchor="w")
            
            lbl_value = tk.Label(pad_inner, text=f"{card['value']:,}", font=("Poppins", 22, "bold"), fg=text_dark, bg=bg_white)
            lbl_value.pack(anchor="w", pady=(6, 0))

    def create_dashboard_tabs(self):
        """Membuat komponen Tab (Notebook) untuk memisahkan menu manajemen utama dan metrik baru."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=bg_white, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Poppins", 10, "bold"), padding=[15, 6], background="#F3F4F6", foreground="#6B7280")
        style.map("TNotebook.Tab", background=[("selected", bg_primary)], foreground=[("selected", bg_white)])

        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(fill="both", expand=True, pady=(10, 0))

        # --- TAB 1: LOG PELANGGARAN & CONTROL PANEL (Fungsi Lama) ---
        self.tab_violations = tk.Frame(self.notebook, bg=bg_white, pady=15)
        self.notebook.add(self.tab_violations, text=" 🔒 Badwords Log & Kontrol ")
        self.build_tab_violations_content()

        # --- TAB 4: USER ACTIVITY SUMMARY (Fungsi Baru) ---
        self.tab_activity = tk.Frame(self.notebook, bg=bg_white, pady=15)
        self.notebook.add(self.tab_activity, text=" 👥 Aktivitas User ")
        self.build_tab_activity_content()

    # =========================================================================
    # KONTEN TAB 1: LOG PELANGGARAN & PANEL KONTROL
    # =========================================================================
    def build_tab_violations_content(self):
        recent_logs = get_recent_violations(limit=5)

        grid_container = tk.Frame(self.tab_violations, bg=bg_white)
        grid_container.pack(fill="both", expand=True)
        
        left_col = tk.Frame(grid_container, bg=bg_white)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.build_violations_table(left_col, recent_logs)
        
        right_col = tk.Frame(grid_container, bg=bg_white)
        right_col.pack(side="right", fill="y", anchor="n")
        self.build_quick_actions_panel(right_col)

    def build_violations_table(self, parent_frame, recent_logs):
        lbl_table_title = tk.Label(parent_frame, text="🔒 5 Pelanggaran Terakhir (Badwords Log)", 
                                   font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_table_title.pack(anchor="w", pady=(0, 10))
        
        table_border_frame = tk.Frame(parent_frame, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB")
        table_border_frame.pack(fill="both", expand=True)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", background=bg_primary, foreground=bg_white, font=("Poppins", 9, "bold"), bd=0, relief="flat")
        style.configure("Treeview", background=bg_white, foreground=text_dark, fieldbackground=bg_white, rowheight=32, font=("Poppins", 9))
        style.map("Treeview", background=[("selected", bg_secondary)])
        
        # 1. TAMBAHKAN "user_id" ke dalam tuple columns
        columns = ("id", "username", "timestamp", "user_id")
        self.tree = ttk.Treeview(table_border_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="LOG ID")
        self.tree.heading("username", text="USERNAME PELANGGAR")
        self.tree.heading("timestamp", text="WAKTU KEJADIAN")
        # Tidak perlu membuat heading untuk user_id jika ingin disembunyikan
        
        self.tree.column("id", width=70, anchor="center")
        self.tree.column("username", width=160, anchor="w")
        self.tree.column("timestamp", width=200, anchor="center")
        
        # 2. SEMBUNYIKAN KOLOM USER_ID (Atur width=0 dan stretch=False)
        self.tree.column("user_id", width=0, stretch=False) 
        
        # 3. MASUKKAN DATA USER_ID KE VALUES
        # Catatan: Pastikan fungsi backend `get_recent_violations()` Anda sudah mengembalikan data user_id/id_user ya!
        for row in recent_logs:
            if isinstance(row, dict):
                self.tree.insert("", "end", values=(row["id"], row["username"], row["created_at"], row.get("user_id", "")))
            else:
                # Jika formatnya tuple/list, sesuaikan indeksnya (misal indeks ke-3 adalah user_id)
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))
            
        scrollbar = ttk.Scrollbar(table_border_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_table_row_selected)

    def build_quick_actions_panel(self, parent_frame):
        lbl_action_title = tk.Label(parent_frame, text="🛠️ Panel Kontrol", 
                                    font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_action_title.pack(anchor="w", pady=(0, 10))
        
        panel_card = tk.Frame(parent_frame, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB", padx=15, pady=15)
        panel_card.pack(fill="x", anchor="n")
        
        lbl_desc = tk.Label(panel_card, text="Pintasan utilitas sistem untuk memantau data secara real-time.", 
                            font=("Poppins", 8), fg="#6B7280", bg=bg_white, wraplength=180, justify="left")
        lbl_desc.pack(anchor="w", pady=(0, 15))
        
        btn_refresh = tk.Button(panel_card, text="🔄   Refresh Semua Data", font=("Poppins", 9, "bold"),
                                bg="#3B82F6", fg="white", activebackground="#2563EB", activeforeground="white",
                                bd=0, height=2, cursor="hand2", command=self.refresh_dashboard)
        btn_refresh.pack(fill="x", pady=(0, 10))

        btn_export = tk.Button(panel_card, text="📊   Export Logs to CSV", font=("Poppins", 9, "bold"),
                               bg="#10B981", fg="white", activebackground="#059669", activeforeground="white",
                               bd=0, height=2, cursor="hand2", command=self.export_to_csv)
        btn_export.pack(fill="x", pady=(0, 10))
        
        btn_clear_logs = tk.Button(panel_card, text="🗑️   Clear Badword Logs", font=("Poppins", 9, "bold"),
                                   bg="#FEE2E2", fg="#EF4444", activebackground="#FCA5A5", activeforeground="#991B1B",
                                   bd=0, height=2, cursor="hand2", command=self.clear_logs)
        btn_clear_logs.pack(fill="x", pady=(0, 10))   

        separator = tk.Frame(panel_card, bg="#E5E7EB", height=1)
        separator.pack(fill="x", pady=8)

        self.lbl_target_info = tk.Label(panel_card, text="Pilih user pada tabel untuk mengelola", 
                                        font=("Poppins", 8, "italic"), fg="#9CA3AF", bg=bg_white)
        self.lbl_target_info.pack(anchor="w", pady=(5, 10))

        self.btn_delete_account = tk.Button(panel_card, text="❌   Hapus Akun Pelanggar", font=("Poppins", 9, "bold"),
                                       bg="#FFF7ED", fg="#EA580C", activebackground="#FFEDD5", activeforeground="#C2410C",
                                       bd=0, height=2, state="disabled", command=self.aksi_hapus_akun_target)
        self.btn_delete_account.pack(fill="x")

    # =========================================================================
    # KONTEN TAB 4: USER ACTIVITY SUMMARY (Fungsi Baru)
    # =========================================================================
    def build_tab_activity_content(self):
        lbl_title = tk.Label(self.tab_activity, text="👥 Ringkasan Aktivitas Kumulatif Seluruh Pengguna", font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_title.pack(anchor="w", pady=(0, 10))

        # Mengambil data real-time via fungsi backend logic
        activity_data = get_user_activity_summary()

        table_frame = tk.Frame(self.tab_activity, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB")
        table_frame.pack(fill="both", expand=True)

        columns = ("user_id", "username", "role", "posts", "likes_given", "comments_written", "violations")
        self.tree_act = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="none")
        
        self.tree_act.heading("user_id", text="USER ID")
        self.tree_act.heading("username", text="USERNAME")
        self.tree_act.heading("role", text="ROLE")
        self.tree_act.heading("posts", text="TOTAL POSTS")
        self.tree_act.heading("likes_given", text="LIKES GIVEN")
        self.tree_act.heading("comments_written", text="COMMENTS WRITTEN")
        self.tree_act.heading("violations", text="TOTAL VIOLATIONS")

        self.tree_act.column("user_id", width=70, anchor="center")
        self.tree_act.column("username", width=120, anchor="w")
        self.tree_act.column("role", width=90, anchor="center")
        self.tree_act.column("posts", width=95, anchor="center")
        self.tree_act.column("likes_given", width=110, anchor="center")
        self.tree_act.column("comments_written", width=140, anchor="center")
        self.tree_act.column("violations", width=120, anchor="center")

        for row in activity_data:
            if isinstance(row, dict):
                self.tree_act.insert("", "end", values=(row["user_id"], row["username"], row["role"], row["total_posts"], row["total_likes_given"], row["total_comments_written"], row["total_violations"]))
            else:
                self.tree_act.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_act.yview)
        self.tree_act.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.tree_act.pack(fill="both", expand=True, padx=1, pady=1)

        # Mengintegrasikan fungsi ekspor backend: export_metrics_to_csv('activity', ...)
        btn_export_act = tk.Button(self.tab_activity, text="📥   Export Semua Aktivitas Pengguna ke CSV", font=("Poppins", 9, "bold"),
                                      bg="#10B981", fg="white", activebackground="#059669", activeforeground="white",
                                      bd=0, height=2, cursor="hand2", command=lambda: self.export_metric_via_backend('activity', 'laporan_aktivitas_user.csv'))
        btn_export_act.pack(anchor="e", pady=(15, 0))

    # --- ACTION HANDLER UTILITAS UNTUK INTEGRASI EXPORT BACKEND LOGIC ---
    def export_metric_via_backend(self, metric_type, default_filename):
        """Membuka File Dialog Simpan Dokumen dan meneruskan hasilnya ke fungsi logic `export_metrics_to_csv`"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title=f"Simpan Laporan Metrik {metric_type.capitalize()}"
        )
        if not file_path:
            return
            
        # Panggil fungsi utilitas bawaan file logic Anda
        sukses = export_metrics_to_csv(metric_type, file_path)
        if sukses:
            messagebox.showinfo("Ekspor Berhasil", f"Data metrik '{metric_type}' berhasil diekspor dan disimpan ke:\n{file_path}")
        else:
            messagebox.showerror("Ekspor Gagal", f"Terjadi kesalahan internal backend saat memproses berkas CSV.")

    # --- LOGIKA EVENT BINDING & MANAJEMEN USER TARGET ---
    def on_table_row_selected(self, event):
        """Memicu perubahan tombol panel kontrol saat salah satu row tabel diklik"""
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        item_values = self.tree.item(selected_item[0], "values")
        log_id = item_values[0]
        target_username = item_values[1]
        target_user_id = item_values[3] # <--- Ambil user_id dari kolom ke-4 (indeks 3)
        
        if target_username == self.current_user.username:
            messagebox.showwarning("Akses Ditolak", "Anda tidak diperbolehkan memanipulasi atau menghapus akun Anda sendiri!")
            self.tree.selection_remove(selected_item) 
            self.reset_action_buttons()
            return
        
        # Simpan user_id ke dictionary
        self.selected_target_user = {
            "log_id": log_id,
            "username": target_username,
            "user_id": target_user_id # <--- Masukkan ke sini
        }
        
        self.lbl_target_info.config(text=f"Target: {target_username} (User #{target_user_id})", fg="#1E40AF", font=("Poppins", 8, "bold"))
        self.btn_delete_account.config(state="normal", cursor="hand2")

    def reset_action_buttons(self):
        """Mengembalikan tombol kontrol ke mode terkunci (disabled)"""
        self.selected_target_user = None
        self.lbl_target_info.config(text="Pilih user pada tabel untuk mengelola", fg="#9CA3AF", font=("Poppins", 8, "italic"))
        self.btn_delete_account.config(state="disabled", cursor="")

    # --- LOGIKA FITUR EXPORT TO CSV MANUAL (DARI TREEVIEW TABEL LOG) ---
    def export_to_csv(self):
        """Mengekspor seluruh baris data dari komponen Treeview ke dalam berkas CSV."""
        tree_items = self.tree.get_children()
        
        if not tree_items:
            messagebox.showwarning("Data Kosong", "Tidak ada data log pelanggaran di tabel untuk diekspor!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Simpan Log Pelanggaran"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(["LOG ID", "USERNAME PELANGGAR", "WAKTU KEJADIAN"])
                
                for item in tree_items:
                    row_values = self.tree.item(item, "values")
                    writer.writerow(row_values)
                    
            messagebox.showinfo("Export Berhasil", f"Data berhasil disimpan ke:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Gagal", f"Terjadi kesalahan saat menulis berkas CSV:\n{str(e)}")

    # --- EKSEKUSI LOGIKA USER_PROFILE TARGET ---
    # --- EKSEKUSI LOGIKA USER_PROFILE TARGET ---
    def aksi_hapus_akun_target(self):
        if not self.selected_target_user:
            return
            
        # Ambil user_id yang asli untuk dihapus
        target_id = self.selected_target_user["user_id"] 
        target_name = self.selected_target_user["username"]
        
        konfirmasi = messagebox.askyesno("Hapus Akun Pengguna", 
                                         f"Apakah Anda yakin ingin menghapus akun '{target_name}' secara permanen?\nSemua log pelanggarannya juga akan ikut bersih.")
        if konfirmasi:
            # Mengirimkan User ID asli ke backend
            res = self.user_profile_backend.delete_user_logic(target_id) 

            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.refresh_dashboard()

    # --- UTILITY MANAGEMENT ---
    def refresh_dashboard(self):
        """Membersihkan frame konten utama dan memuat ulang semua data terbaru dari database."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.render_dashboard_view()
        self.reset_action_buttons() 
        messagebox.showinfo("Sukses", "Semua data dashboard & laporan metrik berhasil diperbarui!")

    def clear_logs(self):
        confirm = messagebox.askyesno("Konfirmasi Tindakan", "Apakah Anda yakin ingin menghapus seluruh log pelanggaran pengguna?")
        if confirm:
            sukses = clear_all_violation_logs()
            if sukses:
                self.refresh_dashboard()
                messagebox.showinfo("Sukses", "Semua log pelanggaran berhasil dibersihkan.")
            else:
                messagebox.showerror("Error", "Gagal membersihkan log dari database.")