import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import Badword_Logic, Sensor_Logic 


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class BadwordManagementFrame(tk.Frame):
    """Frame panel kontrol admin untuk manajemen CRUD daftar kata terlarang (toxic words)."""

    def __init__(self, parent, current_user):
        """Menginisialisasi engine sensor backend, layout form entri, tombol aksi, dan tabel Treeview data."""
        super().__init__(parent, bg=bg_white)
        
        # Instance backend untuk sensor RAM dan CRUD badword
        self.sensor_backend = Sensor_Logic()
        self.badword_backend = Badword_Logic(self.sensor_backend)
        
        self.current_user = current_user
        self.selected_badword_id = None 

        # Render Navigasi & Header bawaan proyek
        render_role_sidebar(self, current_user, "Badword_Management")
        main_header(self, current_user, "Badword Management")

        # --- MAIN FRAME CONTAINER ---
        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True)

        # Container Utama untuk Form dengan Padding Samping yang Pas
        container_form_frame = tk.Frame(main_frame, bg=bg_white)
        container_form_frame.pack(fill="x", padx=(20, 40), pady=(15, 10))

        # 1. PANEL ENTRI DATA (Diberi border halus estetik)
        form_frame = tk.Frame(container_form_frame, bg=bg_white, highlightthickness=1, highlightbackground=border_col, padx=20, pady=15)
        form_frame.pack(fill="x")

        lbl_section = tk.Label(form_frame, text="📝 FORM KELOLA KATA DILARANG (TOXIC WORD)", font=("Poppins", 10, "bold"), fg=text_dark, bg=bg_white)
        lbl_section.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        form_font = ("Poppins", 9)

        tk.Label(form_frame, text="Toxic Word", font=form_font, fg=text_dark, bg=bg_white).grid(row=1, column=0, sticky="w", pady=6)
        self.ent_word = tk.Entry(form_frame, width=40, font=form_font, bg=bg_white, fg=text_dark, highlightthickness=1, highlightbackground=border_col, relief="flat")
        self.ent_word.grid(row=1, column=1, padx=(15, 0), pady=6, ipady=4, sticky="w")
        
        # 2. PANEL TOMBOL AKSI MODERASI (Di bawah form entri)
        btn_frame = tk.Frame(container_form_frame, bg=bg_white)
        btn_frame.pack(fill="x", pady=(15, 10))

        btn_font = ("Poppins", 9, "bold")

        self.btn_add = tk.Button(btn_frame, text="➕  Tambah", command=self.tambah_badword, bg=text_dark, fg=bg_white, activebackground=dark, activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_add.pack(side="left", padx=(0, 10), ipady=6)

        self.btn_edit = tk.Button(btn_frame, text="💾  Simpan Edit", command=self.edit_badword, bg=bg_secondary, fg=bg_white, activebackground=dark, activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_edit.pack(side="left", padx=10, ipady=6)

        self.btn_delete = tk.Button(btn_frame, text="🚫  Hapus", command=self.hapus_badword, bg="#EF4444", fg=bg_white, activebackground="#DC2626", activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_delete.pack(side="left", padx=10, ipady=6)

        self.btn_clear = tk.Button(btn_frame, text="🧹  Clear Form", command=self.clear_form, bg=bg_main, fg=text_dark, activebackground=border_col, activeforeground=text_dark, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_clear.pack(side="left", padx=10, ipady=6)

        # 3. PANEL DAFTAR TABEL TREEVIEW (Full Width Screen)
        table_container = tk.Frame(main_frame, bg=bg_white)
        table_container.pack(fill="both", expand=True, padx=(20, 40), pady=(5, 20))

        lbl_table_title = tk.Label(table_container, text="🔤 Daftar Kata Terlarang Saat Ini", font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
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

        # Kolom tabel: ID dan Word saja
        columns = ("id", "toxic_word")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse", height=10)
        
        self.tree.heading("id", text="ID KATA")
        self.tree.column("id", width=120, minwidth=80, anchor="center", stretch=True)
        
        self.tree.heading("toxic_word", text="KATA DILARANG (TOXIC WORD)")
        self.tree.column("toxic_word", width=500, minwidth=250, anchor="w", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        # Load data awal
        self.refresh_table_data()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================
    def refresh_table_data(self):
        """Menarik ulang list data kata terlarang dari backend untuk disinkronkan ke tabel UI."""
        data = self.badword_backend.get_badwords_logic()
        self.load_data(data)

    def clear_form(self):
        """Mengosongkan isian kolom teks pada form input kata dan mereset ID tracker."""
        self.ent_word.delete(0, tk.END)
        self.selected_badword_id = None 

    def tambah_badword(self):
        """Mengirim data kata toxic baru dari form input untuk disimpan ke dalam database."""
        word_input = self.ent_word.get().strip()
        
        res = self.badword_backend.create_badword_logic(word_input)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_table_data()

    def edit_badword(self):
        """Memperbarui teks kata terlarang yang dipilih berdasarkan ID data yang aktif."""
        word_input = self.ent_word.get().strip()
        
        if not self.selected_badword_id:
            messagebox.showerror("Error", "Pilih kata dari tabel terlebih dahulu!")
            return
            
        res = self.badword_backend.update_badword_logic(self.selected_badword_id, word_input) 

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_table_data()

    def hapus_badword(self):
        """Menghapus entri kata terlarang dari database setelah konfirmasi persetujuan user."""
        if not self.selected_badword_id:
            messagebox.showerror("Error", "Pilih kata dari tabel terlebih dahulu!")
            return
        
        user_res = messagebox.askyesno("Hapus Data", "Apakah Anda yakin ingin menghapus kata ini dari daftar?")

        if user_res:
            res = self.badword_backend.delete_badword_logic(self.selected_badword_id) 
    
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.clear_form()
                self.refresh_table_data()
            
    def kursor_pilih_data(self, id_badword, toxic_word):
        """Memasukkan record data baris tabel yang diklik ke dalam variabel penampung form."""
        self.clear_form()
        self.selected_badword_id = id_badword
        self.ent_word.insert(0, toxic_word)

    def on_tree_select(self, event):
        """Event trigger saat baris tabel di-klik untuk membaca nilai kolom lalu melemparkannya ke form."""
        selected_id = self.get_selected_badword_id()
        if selected_id:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item)['values']
            toxic_word = values[1] 
            self.kursor_pilih_data(selected_id, toxic_word)

    def load_data(self, badwords_data):
        """Menghapus seluruh baris lama Treeview dan merender ulang baris data dari database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in badwords_data:
            self.tree.insert("", "end", values=(row.id, row.word))
            
    def get_selected_badword_id(self):
        """Mengembalikan nilai ID unik (Primary Key) dari record baris tabel yang sedang aktif dipilih."""
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None
