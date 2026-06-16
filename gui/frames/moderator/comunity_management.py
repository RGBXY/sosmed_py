import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import Community_Logic 


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class CommunityManagementFrame(tk.Frame):
    """Frame panel kontrol admin untuk manajemen CRUD (Create, Read, Update, Delete) data komunitas."""

    def __init__(self, parent, current_user):
        """Menginisialisasi engine logic, tata letak form input teks, tombol aksi, dan tabel Treeview data."""
        super().__init__(parent, bg=bg_white)
        self.comunities = Community_Logic()
        self.current_user = current_user
        self.selected_community_id = None 

        # Render Navigasi & Header bawaan proyek
        render_role_sidebar(self, current_user, "Comunity_Management")
        main_header(self, current_user, "Komunitas")

        # --- MAIN FRAME CONTAINER ---
        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True)

        # Container Utama untuk Form dengan Padding Samping yang Pas
        container_form_frame = tk.Frame(main_frame, bg=bg_white)
        container_form_frame.pack(fill="x", padx=(20, 40), pady=(15, 10))

        # 1. PANEL ENTRI DATA (Diberi border halus estetik)
        form_frame = tk.Frame(container_form_frame, bg=bg_white, highlightthickness=1, highlightbackground=border_col, padx=20, pady=15)
        form_frame.pack(fill="x")

        lbl_section = tk.Label(form_frame, text="📝 FORM KELOLA DATA KOMUNITAS", font=("Poppins", 10, "bold"), fg=text_dark, bg=bg_white)
        lbl_section.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        form_font = ("Poppins", 9)

        tk.Label(form_frame, text="Nama Komunitas", font=form_font, fg=text_dark, bg=bg_white).grid(row=1, column=0, sticky="w", pady=6)
        self.ent_name = tk.Entry(form_frame, width=40, font=form_font, bg=bg_white, fg=text_dark, highlightthickness=1, highlightbackground=border_col, relief="flat")
        self.ent_name.grid(row=1, column=1, padx=(15, 0), pady=6, ipady=4, sticky="w")

        tk.Label(form_frame, text="Deskripsi Komunitas", font=form_font, fg=text_dark, bg=bg_white).grid(row=2, column=0, sticky="w", pady=6)
        self.ent_deskripsi = tk.Entry(form_frame, width=60, font=form_font, bg=bg_white, fg=text_dark, highlightthickness=1, highlightbackground=border_col, relief="flat")
        self.ent_deskripsi.grid(row=2, column=1, padx=(15, 0), pady=6, ipady=4, sticky="w")
        
        # 2. PANEL TOMBOL AKSI MODERASI (Di bawah form entri)
        btn_frame = tk.Frame(container_form_frame, bg=bg_white)
        btn_frame.pack(fill="x", pady=(15, 10))

        btn_font = ("Poppins", 9, "bold")

        self.btn_add = tk.Button(btn_frame, text="➕  Tambah", command=self.tambah_komunitas, bg=text_dark, fg=bg_white, activebackground=dark, activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_add.pack(side="left", padx=(0, 10), ipady=6)

        self.btn_edit = tk.Button(btn_frame, text="💾  Simpan Edit", command=self.edit_komunitas, bg=bg_secondary, fg=bg_white, activebackground=dark, activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_edit.pack(side="left", padx=10, ipady=6)

        self.btn_delete = tk.Button(btn_frame, text="🚫  Hapus", command=self.hapus_komunitas, bg="#EF4444", fg=bg_white, activebackground="#DC2626", activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_delete.pack(side="left", padx=10, ipady=6)

        self.btn_clear = tk.Button(btn_frame, text="🧹  Clear Form", command=self.clear_form, bg=bg_main, fg=text_dark, activebackground=border_col, activeforeground=text_dark, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_clear.pack(side="left", padx=10, ipady=6)

        # 3. PANEL DAFTAR TABEL TREEVIEW (Full Width Screen)
        table_container = tk.Frame(main_frame, bg=bg_white)
        table_container.pack(fill="both", expand=True, padx=(20, 40), pady=(5, 20))

        lbl_table_title = tk.Label(table_container, text="🌐 Daftar Komunitas Terdaftar", font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_table_title.pack(anchor="w", pady=(0, 10))

        table_frame = tk.Frame(table_container, bg=bg_white, highlightthickness=1, highlightbackground=border_col)
        table_frame.pack(fill="both", expand=True)
            
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

        columns = ("id", "name", "description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse", height=10)
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=100, minwidth=70, anchor="center", stretch=True)
        
        self.tree.heading("name", text="NAMA KOMUNITAS")
        self.tree.column("name", width=250, minwidth=150, anchor="w", stretch=True)
        
        self.tree.heading("description", text="DESKRIPSI")
        self.tree.column("description", width=450, minwidth=250, anchor="w", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        self.refresh_table_data()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================

    def refresh_table_data(self):
        """Menarik data komunitas terbaru dari database via backend untuk memperbarui isi tabel."""
        data = self.comunities.get_comunity_logic()
        self.load_data(data)

    def clear_form(self):
        """Membersihkan seluruh field teks input pada form entri data dan mereset pelacak ID data."""
        self.ent_name.delete(0, tk.END)
        self.ent_deskripsi.delete(0, tk.END)
        self.selected_community_id = None  

    def tambah_komunitas(self):
        """Mengambil isian teks form lalu mengirimkan instruksi pembuatan rekam komunitas baru ke backend."""
        user_id = self.current_user.id
        nama_komunitas = self.ent_name.get().strip()
        deskripsi_komunitas = self.ent_deskripsi.get().strip()
        
        res = self.comunities.create_comunity_logic(user_id, nama_komunitas, deskripsi_komunitas)
        data = self.comunities.get_comunity_logic()

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.load_data(data)
            self.clear_form()
            self.refresh_table_data()

    def edit_komunitas(self):
        """Memperbarui modifikasi teks deskripsi atau nama komunitas berdasarkan baris data ID terpilih."""
        nama_komunitas = self.ent_name.get().strip()
        deskripsi_komunitas = self.ent_deskripsi.get().strip()
        
        if not self.selected_community_id:
            messagebox.showerror("Error", "Pilih data dari tabel terlebih dahulu!")
            return
            
        res = self.comunities.update_comunity_logic(self.selected_community_id, nama_komunitas, deskripsi_komunitas) 

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_table_data()

    def hapus_komunitas(self):
        """Menghapus entri data komunitas tertentu secara permanen dari database setelah konfirmasi user."""
        if not self.selected_community_id:
            messagebox.showerror("Error", "Pilih data dari tabel terlebih dahulu!")
            return
        
        user_res = messagebox.askyesno("Hapus Data", "Apakah yakin anda ingin menghapus data ini?")

        if user_res:
            res = self.comunities.delete_comunity_logic(self.selected_community_id) 
    
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.clear_form()
                self.refresh_table_data()
            
    def kursor_pilih_data(self, id_komunitas, nama_komunitas, deskripsi_komunitas):
        """Memasukkan record data baris tabel yang diklik ke dalam variabel penampung form."""
        self.clear_form()
        self.selected_community_id = id_komunitas
        self.ent_name.insert(0, nama_komunitas)
        self.ent_deskripsi.insert(0, deskripsi_komunitas)

    def on_tree_select(self, event):
        """Event trigger saat baris tabel di-klik untuk membaca nilai kolom lalu melemparkannya ke form."""
        selected_id = self.get_selected_community_id()
        if selected_id:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item)['values']
            nama_komunitas = values[1] 
            deskripsi_komunitas = values[2] 
            self.kursor_pilih_data(selected_id, nama_komunitas, deskripsi_komunitas)

    def load_data(self, communities_data):
        """Menghapus seluruh baris lama Treeview dan merender ulang baris data dari database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in communities_data:
            self.tree.insert("", "end", values=(row.id, row.name, row.description))
            
    def get_selected_community_id(self):
        """Mengembalikan nilai ID unik (Primary Key) dari record baris tabel yang sedang aktif dipilih."""
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None