# gui/components/badword_table.py
import tkinter as tk
from tkinter import ttk, messagebox
from constrants import * # Pastikan tidak typo dari 'constraints' Anda sebelumnya
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import Badword_Logic, Sensor_Logic 

class BadwordManagementFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white)
        
        # Instance backend untuk sensor RAM dan CRUD badword
        self.sensor_backend = Sensor_Logic()
        self.badword_backend = Badword_Logic(self.sensor_backend)
        
        self.current_user = current_user
        self.selected_badword_id = None 

        # Sesuai konfigurasi sistem navigasi Anda
        render_role_sidebar(self, current_user, "Badword_Management")
        main_header(self, current_user, "Badword Management")

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # --- FORM CONTAINER ---
        container_form_frame = tk.Frame(main_frame, bg=bg_white)
        container_form_frame.pack(fill="x", padx=10, pady=10)

        form_frame = tk.Frame(container_form_frame, bg=bg_white)
        form_frame.pack(padx=10, pady=10, fill="x")

        # Form disesuaikan hanya menginput Kata (Toxic Word)
        tk.Label(form_frame, text="Toxic Word:", bg=bg_white, font=("Poppins", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ent_word = tk.Entry(form_frame, width=40, font=("Poppins", 10))
        self.ent_word.grid(row=0, column=1, padx=5, pady=5)
        
        # --- BUTTONS FRAME ---
        btn_frame = tk.Frame(container_form_frame, bg=bg_white)
        btn_frame.pack(pady=10, padx=10, fill="x")

        self.btn_add = tk.Button(btn_frame, text="Tambah", command=self.tambah_badword, bg="green", fg="white", width=12, font=("Poppins", 9, "bold"))
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_edit = tk.Button(btn_frame, text="Simpan Edit", command=self.edit_badword, bg="orange", fg="white", width=12, font=("Poppins", 9, "bold"))
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_delete = tk.Button(btn_frame, text="Hapus", command=self.hapus_badword, bg="red", fg="white", width=12, font=("Poppins", 9, "bold"))
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.btn_clear = tk.Button(btn_frame, text="Clear", command=self.clear_form, bg="grey", fg="white", width=12, font=("Poppins", 9, "bold"))
        self.btn_clear.grid(row=0, column=3, padx=5)

        # --- TABLE TREEVIEW ---
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

        # Kolom diubah menjadi ID dan Word saja
        columns = ("id", "toxic_word")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=100, anchor="center")
        
        self.tree.heading("toxic_word", text="Kata Dilarang (Toxic Word)")
        self.tree.column("toxic_word", width=400, anchor="w")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Load data awal
        self.refresh_table_data()

    # --- METHODS ---
    def refresh_table_data(self):
        data = self.badword_backend.get_badwords_logic()
        self.load_data(data)

    def clear_form(self):
        self.ent_word.delete(0, tk.END)
        self.selected_badword_id = None 

    def tambah_badword(self):
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
        self.clear_form()
        self.selected_badword_id = id_badword
        self.ent_word.insert(0, toxic_word)

    def on_tree_select(self, event):
        selected_id = self.get_selected_badword_id()
        if selected_id:
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item)['values']
            toxic_word = values[1] 
            self.kursor_pilih_data(selected_id, toxic_word)

    def load_data(self, badwords_data):
        # Bersihkan baris lama di tabel
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # [BAB 5: PERULANGAN] - Memasukkan data objek ke komponen Treeview GUI
        for row in badwords_data:
            # Mengambil data menggunakan tanda titik (.) karena bertipe objek dari model Badwords
            self.tree.insert("", "end", values=(row.id, row.word))
            
    def get_selected_badword_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None