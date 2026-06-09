import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import Comunity_Logic 

class ComunityFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white)
        self.comunities = Comunity_Logic()
        self.current_user = current_user
        self.selected_community_id = None 

        # Setup Sidebar Main Header
        render_role_sidebar(self, current_user, "Comunity")
        main_header(self, current_user, "Komunitas")

        # Main Container
        self.main_content = tk.Frame(self, bg=bg_main)
        self.main_content.pack(side="right", fill="both", expand=True)

        self.render_input_form()

        tk.Frame(self.main_content, height=2, bg=border_col).pack(fill="x", padx=20, pady=10)

        self.render_scrollable_area()
        
        self.refresh_page_data()

    def render_input_form(self):
        form_card = tk.Frame(
            self.main_content, bg=bg_white, 
            highlightbackground=border_col, highlightthickness=1,
            padx=20, pady=20
        )
        form_card.pack(fill="x", padx=20, pady=15)

        self.lbl_form_title = tk.Label(
            form_card, text="Buat Komunitas", 
            font=("Poppins", 11, "bold"), bg=bg_white, fg=bg_primary
        )
        self.lbl_form_title.pack(anchor="w", pady=(0, 15))

        input_grid = tk.Frame(form_card, bg=bg_white)
        input_grid.pack(fill="x")

        tk.Label(input_grid, text="Nama Komunitas", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_name = tk.Entry(input_grid, font=("Poppins", 10), bg=bg_main, relief="flat", highlightbackground=border_col, highlightthickness=1)
        self.ent_name.grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=5)

        tk.Label(input_grid, text="Deskripsi Singkat", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark).grid(row=1, column=0, sticky="w", pady=5)
        self.ent_deskripsi = tk.Entry(input_grid, font=("Poppins", 10), bg=bg_main, relief="flat", highlightbackground=border_col, highlightthickness=1)
        self.ent_deskripsi.grid(row=1, column=1, sticky="ew", padx=(15, 0), pady=5)

        input_grid.columnconfigure(1, weight=1)

        # Btn Container
        self.btn_frame = tk.Frame(form_card, bg=bg_white)
        self.btn_frame.pack(fill="x", pady=(15, 0))

        self.btn_submit = tk.Button(
            self.btn_frame, text="Tambah Komunitas", command=self.tambah_komunitas,
            font=("Poppins", 9, "bold"), bg=bg_primary, fg=bg_white, relief="flat", padx=15, pady=5, cursor="hand2"
        )
        self.btn_submit.pack(side="left", padx=(0, 10))

        self.btn_clear = tk.Button(
            self.btn_frame, text="Clear / Batal", command=self.clear_form,
            font=("Poppins", 9), bg=border_col, fg=text_dark, relief="flat", padx=15, pady=5, cursor="hand2"
        )
        self.btn_clear.pack(side="left")

    def render_scrollable_area(self):
        scroll_container = tk.Frame(self.main_content, bg=bg_main)
        scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.canvas = tk.Canvas(scroll_container, bg=bg_main, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Card Container
        self.card_container = tk.Frame(self.canvas, bg=bg_main)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.card_container, anchor="nw")

        # Scroll Event
        self.card_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.canvas_window, width=event.width))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") if self.canvas.winfo_exists() else None)

    def load_cards(self, data):
        for widget in self.card_container.winfo_children():
            widget.destroy()

        if not data:
            tk.Label(
                self.card_container, text="📭 Belum ada komunitas yang dibuat.",
                font=("Poppins", 10, "italic"), bg=bg_main, fg=text_muted
            ).pack(pady=30)
            return

        # Card 
        for row in data:
            card = tk.Frame(
                self.card_container, bg=bg_white,
                highlightbackground=border_col, highlightthickness=1,
                padx=15, pady=15
            )
            card.pack(fill="x", pady=6)

            info_frame = tk.Frame(card, bg=bg_white)
            info_frame.pack(side="left", fill="both", expand=True)

            tk.Label(
                info_frame, text=f"{row.name}",
                font=("Poppins", 11, "bold"), bg=bg_white, fg=text_dark
            ).pack(anchor="w")

            tk.Label(
                info_frame, text=row.description,
                font=("Poppins", 9), bg=bg_white, fg=text_muted, wraplength=450, justify="left"
            ).pack(anchor="w", pady=(4, 0))

            action_frame = tk.Frame(card, bg=bg_white)
            action_frame.pack(side="right", fill="y")

            if self.current_user.id == row.user_id or self.current_user.role.lower() == "admin" or self.current_user.role.lower() == "moderator":
                btn_edit = tk.Button(
                    action_frame, text="Edit", command=lambda r=row: self.set_form_to_edit_mode(r),
                    font=("Poppins", 8, "bold"), bg=bg_white, fg="#1E88E5", relief="flat", cursor="hand2"
                )
                btn_edit.pack(side="left", padx=5, expand=True)

                btn_delete = tk.Button(
                    action_frame, text="Hapus", command=lambda r=row: self.hapus_komunitas(r.id),
                    font=("Poppins", 8, "bold"), bg=bg_white, fg="#E53935", relief="flat", cursor="hand2"
                )
                btn_delete.pack(side="left", padx=5, expand=True)

    # Update Logic
    def refresh_page_data(self):
        data = self.comunities.get_comunity_logic()
        self.load_cards(data)

    def clear_form(self):
        self.ent_name.delete(0, tk.END)
        self.ent_deskripsi.delete(0, tk.END)
        self.selected_community_id = None
        
        self.lbl_form_title.configure(text="Buat Komunitas Baru", fg=bg_primary)
        self.btn_submit.configure(text="Tambah Komunitas", command=self.tambah_komunitas, bg=bg_primary)

    def set_form_to_edit_mode(self, community_row):
        self.clear_form()
        self.selected_community_id = community_row.id
        
        self.ent_name.insert(0, community_row.name)
        self.ent_deskripsi.insert(0, community_row.description)
        
        self.lbl_form_title.configure(text="Edit Komunitas", fg=bg_primary)
        self.btn_submit.configure(text="Simpan Perubahan", command=self.edit_komunitas, bg=bg_primary)
        self.canvas.yview_moveto(0)

    def tambah_komunitas(self):
        user_id = self.current_user.id
        nama_komunitas = self.ent_name.get().strip()
        deskripsi_komunitas = self.ent_deskripsi.get().strip()
        
        res = self.comunities.create_comunity_logic(user_id, nama_komunitas, deskripsi_komunitas)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_page_data()

    def edit_komunitas(self):
        nama_komunitas = self.ent_name.get().strip()
        deskripsi_komunitas = self.ent_deskripsi.get().strip()
        
        if not self.selected_community_id:
            messagebox.showerror("Error", "ID data tidak valid.")
            return
            
        res = self.comunities.update_comunity_logic(self.selected_community_id, nama_komunitas, deskripsi_komunitas) 

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.clear_form()
            self.refresh_page_data()

    def hapus_komunitas(self, community_id):
        user_res = messagebox.askyesno("Hapus Komunitas", "Apakah Anda yakin ingin menghapus komunitas ini secara permanen?")
        if user_res:
            res = self.comunities.delete_comunity_logic(community_id) 
    
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.clear_form()
                self.refresh_page_data()