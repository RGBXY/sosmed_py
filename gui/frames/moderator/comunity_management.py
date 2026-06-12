# gui/components/community_table.py
import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import Comunity_Logic 

class CommunityManagementFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white)
        self.comunities = Comunity_Logic()
        self.current_user = current_user
        self.selected_community_id = None 

        render_role_sidebar(self, current_user, "Comunity_Management")
        main_header(self, current_user, "Komunitas")

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        container_form_frame = tk.Frame(main_frame, bg=bg_white)
        container_form_frame.pack(fill="x", padx=10, pady=10)

        form_frame = tk.Frame(container_form_frame, bg=bg_white)
        form_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(form_frame, text="Nama Komunitas:", bg=bg_white).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ent_name = tk.Entry(form_frame, width=30)
        self.ent_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Deskripsi Komunitas:", bg=bg_white).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ent_deskripsi = tk.Entry(form_frame, width=30)
        self.ent_deskripsi.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(container_form_frame, bg=bg_white)
        btn_frame.pack(pady=10, padx=10, fill="x")

        self.btn_add = tk.Button(btn_frame, text="Tambah", command=self.tambah_komunitas, bg="green", fg="white", width=10)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_edit = tk.Button(btn_frame, text="Simpan Edit", command=self.edit_komunitas, bg="orange", fg="white", width=10)
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(btn_frame, text="Hapus", command=self.hapus_komunitas, bg="red", fg="white", width=10)
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_clear = tk.Button(btn_frame, text="Clear", command=self.clear_form, bg="grey", fg="white", width=10)
        self.btn_clear.grid(row=0, column=3, padx=5)

        table_frame = tk.Frame(main_frame, bg=bg_white)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
        # Styling Treeview
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

        columns = ("id", "name", "description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        
        self.tree.heading("name", text="Nama Komunitas")
        self.tree.column("name", width=150, anchor="w")
        
        self.tree.heading("description", text="Deskripsi")
        self.tree.column("description", width=300, anchor="w")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_table_data()


    # METHOD 
    def refresh_table_data(self):
        data = self.comunities.get_comunity_logic()
        self.load_data(data)

    def clear_form(self):
        self.ent_name.delete(0, tk.END)
        self.ent_deskripsi.delete(0, tk.END)
        self.selected_community_id = None  # Reset ID yang dipilih

    def tambah_komunitas(self):
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
        self.clear_form()
        self.selected_community_id = id_komunitas
        self.ent_name.insert(0, nama_komunitas)
        self.ent_deskripsi.insert(0, deskripsi_komunitas)

    def on_tree_select(self, event):
        selected_id = self.get_selected_community_id()
        if selected_id:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item)['values']
            nama_komunitas = values[1] 
            deskripsi_komunitas = values[2] 
            self.kursor_pilih_data(selected_id, nama_komunitas, deskripsi_komunitas)

    def load_data(self, communities_data):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in communities_data:
            print(row.id, row.user_id)
            self.tree.insert("", "end", values=(row.id, row.name, row.description))
            
    def get_selected_community_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None