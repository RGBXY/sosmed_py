# ============================================================
# SECTION: IMPORTS
# ============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import User_Profile, Auth


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class UserManagementFrame(tk.Frame):
    """Frame panel manajemen data pengguna sistem bagi administrator."""

    def __init__(self, parent, current_user):
        """Menginisialisasi layout form entri data, tombol aksi moderasi, dan tabel daftar akun."""
        super().__init__(parent, bg=bg_white)
        self.user_backend = User_Profile()  
        self.auth_backend = Auth()  
        self.current_user = current_user
        self.selected_user_id = None 

        render_role_sidebar(self, current_user, "User_Management")
        main_header(self, current_user, "User Management")  

        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True)

        container_form_frame = tk.Frame(main_frame, bg=bg_white)
        container_form_frame.pack(fill="x", padx=(20, 40), pady=(15, 10))

        # Panel Entri Data Form
        form_frame = tk.Frame(container_form_frame, bg=bg_white, highlightthickness=1, highlightbackground=border_col, padx=20, pady=15)
        form_frame.pack(fill="x")

        lbl_section = tk.Label(form_frame, text="📝 FORM KELOLA DATA PENGGUNA", font=("Poppins", 10, "bold"), fg=text_dark, bg=bg_white)
        lbl_section.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        form_font = ("Poppins", 9)
        
        tk.Label(form_frame, text="Username", font=form_font, fg=text_dark, bg=bg_white).grid(row=1, column=0, sticky="w", pady=6)
        self.ent_username = tk.Entry(form_frame, width=40, font=form_font, bg=bg_white, fg=text_dark, highlightthickness=1, highlightbackground=border_col, relief="flat")
        self.ent_username.grid(row=1, column=1, padx=(15, 0), pady=6, ipady=4, sticky="w")

        tk.Label(form_frame, text="Password Baru", font=form_font, fg=text_dark, bg=bg_white).grid(row=2, column=0, sticky="w", pady=6)
        self.ent_password = tk.Entry(form_frame, width=40, font=form_font, show="*", bg=bg_white, fg=text_dark, highlightthickness=1, highlightbackground=border_col, relief="flat")
        self.ent_password.grid(row=2, column=1, padx=(15, 0), pady=6, ipady=4, sticky="w")

        tk.Label(form_frame, text="Konfirmasi Password", font=form_font, fg=text_dark, bg=bg_white).grid(row=3, column=0, sticky="w", pady=6)
        self.ent_confirm_password = tk.Entry(form_frame, width=40, font=form_font, show="*", bg=bg_white, fg=text_dark, highlightthickness=1, highlightbackground=border_col, relief="flat")
        self.ent_confirm_password.grid(row=3, column=1, padx=(15, 0), pady=6, ipady=4, sticky="w")

        tk.Label(form_frame, text="Role Akses System", font=form_font, fg=text_dark, bg=bg_white).grid(row=4, column=0, sticky="w", pady=6)
        self.cb_role = ttk.Combobox(form_frame, values=["user", "moderator", "admin"], width=38, font=form_font, state="readonly")
        self.cb_role.grid(row=4, column=1, padx=(15, 0), pady=6, ipady=3, sticky="w")
        self.cb_role.set("user") 
        
        # Panel Tombol Aksi Moderasi
        btn_frame = tk.Frame(container_form_frame, bg=bg_white)
        btn_frame.pack(fill="x", pady=(15, 10))

        btn_font = ("Poppins", 9, "bold")

        self.btn_add = tk.Button(btn_frame, text="➕   Tambah User", command=self.tambah_user, bg=text_dark, fg=bg_white, activebackground=dark, activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_add.pack(side="left", padx=(0, 10), ipady=6)

        self.btn_edit = tk.Button(btn_frame, text="💾   Simpan Edit", command=self.edit_user, bg=bg_secondary, fg=bg_white, activebackground=dark, activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_edit.pack(side="left", padx=10, ipady=6)

        self.btn_delete = tk.Button(btn_frame, text="🚫   Hapus User", command=self.hapus_user, bg="#EF4444", fg=bg_white, activebackground="#DC2626", activeforeground=bg_white, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_delete.pack(side="left", padx=10, ipady=6)

        self.btn_clear = tk.Button(btn_frame, text="🧹   Clear Form", command=self.clear_form, bg=bg_main, fg=text_dark, activebackground=border_col, activeforeground=text_dark, width=15, font=btn_font, relief="flat", bd=0, cursor="hand2")
        self.btn_clear.pack(side="left", padx=10, ipady=6)

        # Panel Treeview Daftar Tabel
        table_container = tk.Frame(main_frame, bg=bg_white)
        table_container.pack(fill="both", expand=True, padx=(20, 40), pady=(5, 20))

        lbl_table_title = tk.Label(table_container, text="👥 Daftar Seluruh Akun Terdaftar", font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_table_title.pack(anchor="w", pady=(0, 10))

        table_frame = tk.Frame(table_container, bg=bg_white, highlightthickness=1, highlightbackground=border_col)
        table_frame.pack(fill="both", expand=True)
            
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

        columns = ("id", "username", "role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse", height=10)
        
        self.tree.heading("id", text="USER ID")
        self.tree.column("id", width=100, minwidth=70, anchor="center", stretch=True)
        
        self.tree.heading("username", text="USERNAME")
        self.tree.column("username", width=350, minwidth=150, anchor="w", stretch=True)
        
        self.tree.heading("role", text="ROLE AKSES")
        self.tree.column("role", width=200, minwidth=100, anchor="center", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=1, pady=1)

        self.refresh_table_data()

    def refresh_table_data(self):
        """Memuat ulang seluruh rekaman data pengguna dari backend ke dalam tabel."""
        try:
            data = self.auth_backend.get_user_logic()
            self.load_data(data)
        except Exception as e:
            print(f"Gagal mengambil daftar pengguna: {e}")

    def clear_form(self):
        """Mengosongkan teks seluruh input field form dan mereset selection id user."""
        self.ent_username.delete(0, tk.END)
        self.ent_password.delete(0, tk.END)
        self.ent_confirm_password.delete(0, tk.END)
        self.cb_role.set("user")
        self.selected_user_id = None 

    def tambah_user(self):
        """Validasi data input dan mendaftarkan akun pengguna baru ke sistem via backend."""
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        confirm_password = self.ent_confirm_password.get().strip()
        role = self.cb_role.get()
        
        res = self.auth_backend.resgiter_admin_logic(username, password, role, confirm_password)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_table_data()

    def edit_user(self):
        """Menyimpan modifikasi kredensial atau peran akses data pengguna lama."""
        id = self.selected_user_id
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        confirm_password = self.ent_confirm_password.get().strip()
        role = self.cb_role.get()
        
        if not self.selected_user_id:
            messagebox.showerror("Error", "Pilih user dari tabel terlebih dahulu!")
            return
            
        res = self.auth_backend.edit_resgiter_admin_logic(id, username, password, role, confirm_password) 

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_table_data()

    def hapus_user(self):
        """Menghapus akun pengguna terpilih secara permanen dari basis data."""
        if not self.selected_user_id:
            messagebox.showerror("Error", "Pilih user dari tabel terlebih dahulu!")
            return
        
        if self.selected_user_id == self.current_user.id:
            messagebox.showwarning("Peringatan", "Anda tidak bisa menghapus akun Anda sendiri dari panel ini!")
            return

        user_res = messagebox.askyesno("Hapus User", "Apakah Anda yakin ingin menghapus pengguna ini secara permanen?")

        if user_res:
            res = self.user_backend.delete_user_logic(self.selected_user_id) 
    
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.clear_form()
                self.refresh_table_data()
            
    def kursor_pilih_data(self, id_user, username, role):
        """Memasukkan rincian data baris tabel terpilih kembali ke dalam widget input form."""
        self.clear_form()
        self.selected_user_id = id_user
        self.ent_username.insert(0, username)
        self.cb_role.set(role)

    def on_tree_select(self, event):
        """Memicu pengambilan rincian data kolom saat sebuah baris tabel di klik oleh kursor."""
        selected_id = self.get_selected_user_id()
        if selected_id:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item)['values']
            username = values[1] 
            role = values[2] 
            self.kursor_pilih_data(selected_id, username, role)

    def load_data(self, user_data_list):
        """Menghapus seluruh baris lama dan merender array baris data pengguna baru pada Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in user_data_list:
            self.tree.insert("", "end", values=(row.id, row.username, row.role))
            
    def get_selected_user_id(self):
        """Mengembalikan nilai index ID baris pengguna yang sedang aktif dipilih pada tabel."""
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None