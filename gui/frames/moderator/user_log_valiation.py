import tkinter as tk
from tkinter import ttk, messagebox
from constrants import * 
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

from data import get_recent_violations, clear_all_violation_logs
from logic import User_Profile 

class ViolationsManagementFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white)
        self.user_profile_logic = User_Profile() 
        self.current_user = current_user
        self.selected_user_id = None
        self.selected_log_id = None

        render_role_sidebar(self, current_user, "Violations_Management")
        main_header(self, current_user, "Log Pelanggaran Kata")

        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        left_frame = tk.Frame(main_frame, bg=bg_white)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = tk.Frame(main_frame, bg=bg_white, width=250)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False) 

        # =================================================================
        # 1. BAGIAN TABEL (KIRI)
        # =================================================================
        lbl_table_title = tk.Label(left_frame, text="🔒 5 Pelanggaran Terakhir (Badwords Log)", 
                                   font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_table_title.pack(anchor="w", pady=(0, 10))
        
        table_border_frame = tk.Frame(left_frame, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB")
        table_border_frame.pack(fill="both", expand=True)
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", background=bg_primary, foreground=bg_white, 
                             font=("Poppins", 9, "bold"), bd=0, relief="flat")
        self.style.configure("Treeview", background=bg_white, foreground=text_dark, 
                             fieldbackground=bg_white, rowheight=32, font=("Poppins", 9))
        self.style.map("Treeview", background=[("selected", bg_secondary)])
        
        columns = ("id", "username", "timestamp", "user_id")
        self.tree = ttk.Treeview(table_border_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="LOG ID")
        self.tree.heading("username", text="USERNAME PELANGGAR")
        self.tree.heading("timestamp", text="WAKTU KEJADIAN")
        
        self.tree.column("id", width=70, anchor="center")
        self.tree.column("username", width=160, anchor="w")
        self.tree.column("timestamp", width=200, anchor="center")
        self.tree.column("user_id", width=0, stretch=False) # Kolom Tersembunyi
        
        scrollbar = ttk.Scrollbar(table_border_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_table_row_selected)

        # =================================================================
        # 2. BAGIAN PANEL KONTROL (KANAN)
        # =================================================================
        lbl_action_title = tk.Label(right_frame, text="🛠️ Panel Kontrol", 
                                    font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_action_title.pack(anchor="w", pady=(0, 10))
        
        panel_card = tk.Frame(right_frame, bg=bg_white, highlightthickness=1, highlightbackground="#E5E7EB", padx=15, pady=15)
        panel_card.pack(fill="both", expand=True)
        
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

        self.btn_delete_account = tk.Button(panel_card, text="❌   Hapus Akun Pelanggar", font=("Poppins", 9, "bold"),
                                       bg="#FFF7ED", fg="#EA580C", activebackground="#FFEDD5", activeforeground="#C2410C",
                                       bd=0, height=2, state="disabled", command=self.aksi_hapus_akun_target)
        self.btn_delete_account.pack(fill="x")

        # Load data awal saat aplikasi dibuka
        self.refresh_dashboard()

    # =================================================================
    # METHOD LOGIC & EVENT HANDLER IMPLEMENTATION
    # =================================================================
    def load_data(self, recent_logs):
        """Memasukkan data dari database ke dalam Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in recent_logs:
            if isinstance(row, dict):
                self.tree.insert("", "end", values=(row["id"], row["username"], row["created_at"], row.get("user_id", "")))
            else:
                # Mengingat query menggunakan indeks tuple: row[0]=id, row[1]=username, row[2]=created_at, row[3]=user_id
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))

    def on_table_row_selected(self, event):
        """Membaca baris aktif dan menyimpan metadata target."""
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0])['values']
            self.selected_log_id = values[0]
            username = values[1]
            self.selected_user_id = values[3] 
            
            # Perbarui teks info target & aktifkan tombol hapus akun
            self.btn_delete_account.config(state="normal")

    def refresh_dashboard(self):
        """Mengambil ulang 5 data log terbaru dan mereset komponen panel."""
        # Memanggil fungsi backend yang mengambil log pelanggaran terbaru (Limit default=5)
        recent_logs = get_recent_violations()
        self.load_data(recent_logs)
        
        # Reset data seleksi & kunci tombol hapus akun
        self.selected_user_id = None
        self.selected_log_id = None
        self.btn_delete_account.config(state="disabled")

    def export_to_csv(self):
        # Fitur utilitas tambahan Anda
        messagebox.showinfo("Export", "Logs berhasil di-export ke CSV!")

    def clear_logs(self):
        """Menghapus semua log pelanggaran kata kasar."""
        confirm = messagebox.askyesno("Hapus Log", "Apakah Anda yakin ingin menghapus seluruh riwayat log pelanggaran?")
        if confirm:
            # Memanggil fungsi backend clear log
            success = clear_all_violation_logs()
            if success:
                messagebox.showinfo("Sukses", "Semua riwayat log pelanggaran telah dibersihkan.")
                self.refresh_dashboard()
            else:
                messagebox.showerror("Error", "Gagal membersihkan log pelanggaran.")

    def aksi_hapus_akun_target(self):
        """Mengeksekusi penghapusan akun pelaku pelanggaran berdasarkan baris terpilih."""
        if not self.selected_user_id:
            messagebox.showerror("Error", "Pilih user dari tabel terlebih dahulu!")
            return
            
        confirm = messagebox.askyesno("Konfirmasi Hapus Akun", "Apakah Anda yakin ingin menghapus akun pelanggar ini secara permanen?")
        if confirm:
            # Memanggil class logic User_Profile .delete_user_logic(id)
            response = self.user_profile_logic.delete_user_logic(self.selected_user_id)
            
            if response["status"] == "Error":
                messagebox.showerror(response["message"][0], response["message"][1])
                return
            
            if response["status"] == "Success":
                messagebox.showinfo(response["message"][0], response["message"][1])
                self.refresh_dashboard() # Segar kembali tabel & bersihkan pilihan data target