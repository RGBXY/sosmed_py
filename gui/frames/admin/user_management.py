import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import User_Profile, Auth

class UserManagementFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white)
        self.user_backend = User_Profile()  
        self.auth_backend = Auth()  # Digunakan untuk register, edit, dan get users
        self.current_user = current_user
        self.selected_user_id = None 

        # Render Navigasi & Header
        render_role_sidebar(self, current_user, "User_Management")
        main_header(self, current_user, "User Management")  

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        container_form_frame = tk.Frame(main_frame, bg=bg_white)
        container_form_frame.pack(fill="x", padx=10, pady=10)

        form_frame = tk.Frame(container_form_frame, bg=bg_white)
        form_frame.pack(padx=10, pady=10, fill="x")

        # --- FIELD FORM USER ---
        tk.Label(form_frame, text="Username:", bg=bg_white).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ent_username = tk.Entry(form_frame, width=30)
        self.ent_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Password:", bg=bg_white).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ent_password = tk.Entry(form_frame, width=30, show="*")  
        self.ent_password.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Confirm Password:", bg=bg_white).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.ent_confirm_password = tk.Entry(form_frame, width=30, show="*")
        self.ent_confirm_password.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Role Akses:", bg=bg_white).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.cb_role = ttk.Combobox(form_frame, values=["user", "moderator", "admin"], width=28, state="readonly")
        self.cb_role.grid(row=3, column=1, padx=5, pady=5)
        self.cb_role.set("user") 
        
        # --- PANEL TOMBOL AKSI ---
        btn_frame = tk.Frame(container_form_frame, bg=bg_white)
        btn_frame.pack(pady=10, padx=10, fill="x")

        self.btn_add = tk.Button(btn_frame, text="Tambah User", command=self.tambah_user, bg="green", fg="white", width=12, font=("Poppins", 9, "bold"), relief="flat", cursor="hand2")
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_edit = tk.Button(btn_frame, text="Simpan Edit", command=self.edit_user, bg="orange", fg="white", width=12, font=("Poppins", 9, "bold"), relief="flat", cursor="hand2")
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(btn_frame, text="Hapus User", command=self.hapus_user, bg="red", fg="white", width=12, font=("Poppins", 9, "bold"), relief="flat", cursor="hand2")
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_clear = tk.Button(btn_frame, text="Clear", command=self.clear_form, bg="grey", fg="white", width=12, font=("Poppins", 9, "bold"), relief="flat", cursor="hand2")
        self.btn_clear.grid(row=0, column=3, padx=5)

        # --- KOMPONEN TABEL TREEVIEW ---
        table_frame = tk.Frame(main_frame, bg=bg_white)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure(
            "Treeview.Heading",
            background=bg_primary,
            foreground=bg_white,
            font=("Poppins", 10, "bold"),
        )
            
        self.style.configure(
            "Treeview",
            background=bg_white,
            foreground=text_dark,
            fieldbackground=bg_white,
            rowheight=30,
            font=("Poppins", 9)
        )
        
        self.style.map("Treeview", background=[("selected", bg_secondary)])

        columns = ("id", "username", "role")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID User")
        self.tree.column("id", width=60, anchor="center")
        
        self.tree.heading("username", text="Username")
        self.tree.column("username", width=250, anchor="w")
        
        self.tree.heading("role", text="Role Akses")
        self.tree.column("role", width=150, anchor="center")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table_data()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================
    
    def refresh_table_data(self):
        try:
            # Diarahkan ke auth_backend sesuai letak def get_user_logic()
            data = self.auth_backend.get_user_logic()
            self.load_data(data)
        except Exception as e:
            print(f"Gagal mengambil daftar pengguna: {e}")

    def clear_form(self):
        self.ent_username.delete(0, tk.END)
        self.ent_password.delete(0, tk.END)
        self.ent_confirm_password.delete(0, tk.END)
        self.cb_role.set("user")
        self.selected_user_id = None 

    def tambah_user(self):
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        confirm_password = self.ent_confirm_password.get().strip()
        role = self.cb_role.get()
        
        # Diarahkan ke auth_backend
        res = self.auth_backend.resgiter_admin_logic(username, password, role, confirm_password)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_table_data()

    def edit_user(self):
        id = self.selected_user_id
        username = self.ent_username.get().strip()
        password = self.ent_password.get().strip()
        confirm_password = self.ent_confirm_password.get().strip()
        role = self.cb_role.get()
        
        if not self.selected_user_id:
            messagebox.showerror("Error", "Pilih user dari tabel terlebih dahulu!")
            return
            
        # Diarahkan ke edit_resgiter_admin_logic milik auth_backend
        res = self.auth_backend.edit_resgiter_admin_logic(id, username, password, role, confirm_password) 

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_table_data()

    def hapus_user(self):
        if not self.selected_user_id:
            messagebox.showerror("Error", "Pilih user dari tabel terlebih dahulu!")
            return
        
        if self.selected_user_id == self.current_user.id:
            messagebox.showwarning("Peringatan", "Anda tidak bisa menghapus akun Anda sendiri dari panel ini!")
            return

        user_res = messagebox.askyesno("Hapus User", "Apakah Anda yakin ingin menghapus pengguna ini secara permanen?")

        if user_res:
            # Fungsi delete tetap berada di user_backend (User_Profile)
            res = self.user_backend.delete_user_logic(self.selected_user_id) 
    
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.clear_form()
                self.refresh_table_data()
            
    def kursor_pilih_data(self, id_user, username, role):
        self.clear_form()
        self.selected_user_id = id_user
        self.ent_username.insert(0, username)
        self.cb_role.set(role)

    def on_tree_select(self, event):
        selected_id = self.get_selected_user_id()
        if selected_id:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item)['values']
            username = values[1] 
            role = values[2] 
            self.kursor_pilih_data(selected_id, username, role)

    def load_data(self, user_data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in user_data_list:
            self.tree.insert("", "end", values=(row.id, row.username, row.role))
            
    def get_selected_user_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None