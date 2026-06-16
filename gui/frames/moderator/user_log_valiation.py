import tkinter as tk
from tkinter import ttk, messagebox
from constrants import * 
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

from data import get_recent_violations, clear_all_violation_logs
from logic import User_Profile 


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class ViolationsManagementFrame(tk.Frame):
    """Frame panel kontrol admin untuk memantau log pelanggaran kata terlarang dan tindakan moderasi akun."""

    def __init__(self, parent, current_user):
        """Menginisialisasi layout split-screen: tabel log di sisi kiri dan tombol aksi kendali di sisi kanan."""
        super().__init__(parent, bg=bg_white)
        self.user_profile_logic = User_Profile() 
        self.current_user = current_user
        self.selected_user_id = None
        self.selected_log_id = None

        # Render Navigasi & Header bawaan proyek
        render_role_sidebar(self, current_user, "Violations_Management")
        main_header(self, current_user, "Log Pelanggaran Kata")

        # --- MAIN FRAME CONTAINER ---
        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True, padx=(20, 40), pady=(15, 20))

        # Split Layout: Kiri untuk Tabel Log, Kanan untuk Panel Kontrol
        left_frame = tk.Frame(main_frame, bg=bg_white)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        right_frame = tk.Frame(main_frame, bg=bg_white, width=280)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False) 

        # =================================================================
        # 1. BAGIAN TABEL LOG PELANGGARAN (KIRI)
        # =================================================================
        lbl_table_title = tk.Label(left_frame, text="🔒 5 Pelanggaran Terakhir (Badwords Log)", 
                                   font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_table_title.pack(anchor="w", pady=(0, 10))
        
        table_border_frame = tk.Frame(left_frame, bg=bg_white, highlightthickness=1, highlightbackground=border_col)
        table_border_frame.pack(fill="both", expand=True)
        
        # Kustomisasi Tampilan Tabel Menyesuaikan Tema Utama Hubble
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(
            "Treeview.Heading", 
            background=bg_main, 
            foreground=text_dark, 
            font=("Poppins", 9, "bold"), 
            relief="flat",
            borderwidth=0
        )
        
        self.style.configure(
            "Treeview", 
            background=bg_white, 
            foreground=text_dark, 
            fieldbackground=bg_white, 
            rowheight=32, 
            font=("Poppins", 9),
            borderwidth=0
        )
        
        self.style.map("Treeview", background=[("selected", dark)], foreground=[("selected", bg_white)])
        
        columns = ("id", "username", "timestamp", "user_id")
        self.tree = ttk.Treeview(table_border_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="LOG ID")
        self.tree.column("id", width=80, minwidth=60, anchor="center", stretch=True)
        
        self.tree.heading("username", text="USERNAME PELANGGAR")
        self.tree.column("username", width=200, minwidth=120, anchor="w", stretch=True)
        
        self.tree.heading("timestamp", text="WAKTU KEJADIAN")
        self.tree.column("timestamp", width=220, minwidth=150, anchor="center", stretch=True)
        
        self.tree.column("user_id", width=0, stretch=False) # Kolom ID Sembunyi Permanen
        
        scrollbar = ttk.Scrollbar(table_border_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_table_row_selected)

        # =================================================================
        # 2. BAGIAN PANEL KONTROL MODERASI (KANAN)
        # =================================================================
        lbl_action_title = tk.Label(right_frame, text="🛠️ Panel Kontrol", 
                                    font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_action_title.pack(anchor="w", pady=(0, 10))
        
        panel_card = tk.Frame(right_frame, bg=bg_white, highlightthickness=1, highlightbackground=border_col, padx=15, pady=20)
        panel_card.pack(fill="both", expand=True)
        
        btn_font = ("Poppins", 9, "bold")

        btn_refresh = tk.Button(panel_card, text="🔄   Refresh Semua Data", font=btn_font,
                                 bg=bg_main, fg=text_dark, activebackground=border_col, activeforeground=text_dark,
                                 bd=0, relief="flat", cursor="hand2", command=self.refresh_dashboard)
        btn_refresh.pack(fill="x", pady=(0, 12), ipady=6)
        
        btn_clear_logs = tk.Button(panel_card, text="🗑️   Clear Badword Logs", font=btn_font,
                                bg=text_dark, fg=bg_white, activebackground=dark, activeforeground=bg_white,
                                bd=0, relief="flat", cursor="hand2", command=self.clear_logs)
        btn_clear_logs.pack(fill="x", pady=(0, 15), ipady=6)   

        separator = tk.Frame(panel_card, bg=border_col, height=1)
        separator.pack(fill="x", pady=(0, 15))

        self.btn_delete_account = tk.Button(panel_card, text="❌   Hapus Akun Pelanggar", font=btn_font,
                                    bg="#EF4444", fg=bg_white, activebackground="#DC2626", activeforeground=bg_white,
                                    disabledforeground="#9CA3AF", bd=0, relief="flat", state="disabled", 
                                    cursor="hand2", command=self.aksi_hapus_akun_target)
        self.btn_delete_account.pack(fill="x", ipady=6)

        # Load data awal saat aplikasi dibuka
        self.refresh_dashboard()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================
    def refresh_dashboard(self):
        """Mengambil ulang 5 data log pelanggaran terbaru dari database dan menyegarkan status tombol kontrol."""
        recent_logs = get_recent_violations()
        self._load_data(recent_logs)
        
        # Reset data seleksi & kunci tombol hapus akun
        self.selected_user_id = None
        self.selected_log_id = None
        self.btn_delete_account.config(state="disabled")

    def clear_logs(self):
        """Membersihkan seluruh rekam data log riwayat pelanggaran kata dari sistem setelah dikonfirmasi."""
        confirm = messagebox.askyesno("Hapus Log", "Apakah Anda yakin ingin menghapus seluruh riwayat log pelanggaran?")
        if confirm:
            success = clear_all_violation_logs()
            if success:
                messagebox.showinfo("Sukses", "Semua riwayat log pelanggaran telah dibersihkan.")
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", "Gagal membersihkan log pelanggaran.")

    def aksi_hapus_akun_target(self):
        """Mengeksekusi penghapusan akun pengguna yang melakukan pelanggaran berdasarkan baris tabel terpilih."""
        if not self.selected_user_id:
            messagebox.showerror("Error", "Pilih user dari tabel terlebih dahulu!")
            return
            
        confirm = messagebox.askyesno("Konfirmasi Hapus Akun", "Apakah Anda yakin ingin menghapus akun pelanggar ini secara permanen?")
        if confirm:
            response = self.user_profile_logic.delete_user_logic(self.selected_user_id)
            
            if response["status"] == "Error":
                messagebox.showerror(response["message"][0], response["message"][1])
                return
            
            if response["status"] == "Success":
                messagebox.showinfo(response["message"][0], response["message"][1])
                self.refresh_dashboard()

    def _load_data(self, recent_logs):
        """Menghapus elemen baris lama pada tabel Treeview dan mengisi ulang dengan data log terbaru."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in recent_logs:
            if isinstance(row, dict):
                self.tree.insert("", "end", values=(row["id"], row["username"], row["created_at"], row.get("user_id", "")))
            else:
                # Mengingat query menggunakan indeks tuple: row[0]=id, row[1]=username, row[2]=created_at, row[3]=user_id
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))

    def _on_table_row_selected(self, event):
        """Event trigger saat baris log dipilih untuk merekam ID target dan mengaktifkan panel hapus akun."""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            self.selected_log_id = values[0]
            username = values[1]
            self.selected_user_id = values[3] 
            
            # Perbarui teks info target & aktifkan tombol hapus akun
            self.btn_delete_account.config(state="normal")