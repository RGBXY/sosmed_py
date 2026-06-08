# gui/frames/moderator/comunity.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from constrants import *
from gui.components.sidebar import sidebar
from gui.components.header import main_header
from logic import Comunity_Logic 

class CommunityManagementFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_main)
        self.comunity_logic = Comunity_Logic()
        self.communities_data = self.comunity_logic.get_comunity_logic()

        def go_home():
            from gui.frames.home import HomeFrame
            self.master.switch_frame(HomeFrame, current_user=self.master.current_user)
             
        def go_dashboard():
            from gui.frames.moderator.dashboard_moderator import DashboardModerator
            self.master.switch_frame(DashboardModerator, current_user=self.master.current_user)

        def go_comunity_form():
            self.master.switch_frame(CommunityManagementFrame, current_user=self.master.current_user)
        
        nav_items = [
            {"title": "Home", "comand": go_home, "active": False},
            {"title": "Dashboard", "comand": go_dashboard, "active": False},
            {"title": "Comunity", "comand": go_comunity_form, "active": True}
        ]
        
        sidebar(self, current_user, nav_items)
        main_header(self, current_user, "Manajemen Komunitas")

        # Content Area
        content_area = tk.Frame(self, bg=bg_main, padx=30, pady=20)
        content_area.pack(side="left", fill="both", expand=True)

        # Judul Utama Halaman
        tk.Label(
            content_area, 
            text="Kelola Komunitas Anda", 
            font=("Poppins", 14, "bold"), 
            bg=bg_main, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 15))

        table_container = tk.Frame(
            content_area, 
            bg=bg_white, 
            highlightbackground=border_col, 
            highlightthickness=1,
            padx=15,
            pady=15
        )
        self.tree.configure(height=6)
        table_container.pack(fill="x", expand=True, pady=(0, 20))

        # Styling Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview.Heading", background=bg_primary, foreground=bg_white,
            font=("Poppins", 10, "bold"), padding=8
        )
        self.style.configure(
            "Treeview", background=bg_white, foreground=text_dark,
            fieldbackground=bg_white, rowheight=30, font=("Poppins", 9)
        )
        self.style.map("Treeview", background=[("selected", bg_secondary)])

        columns = ("id", "name", "description")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        self.tree.heading("name", text="Nama Komunitas")
        self.tree.column("name", width=180, anchor="w")
        self.tree.heading("description", text="Deskripsi")
        self.tree.column("description", width=400, anchor="w")

        self.scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        action_frame = tk.Frame(content_area, bg=bg_main)
        action_frame.pack(fill="x", pady=(0, 20))

        btn_edit = tk.Button(
            action_frame, text="📝 Edit Terpilih", command=self.handle_edit,
            bg=bg_primary, fg=bg_white, font=("Poppins", 9, "bold"),
            relief="flat", padx=15, pady=6, cursor="hand2"
        )
        btn_edit.pack(side="left", padx=(0, 10))

        btn_delete = tk.Button(
            action_frame, text="🗑️ Hapus Terpilih", command=self.handle_delete,
            bg="#FF4D4D", fg=bg_white, font=("Poppins", 9, "bold"),
            relief="flat", padx=15, pady=6, cursor="hand2"
        )
        btn_delete.pack(side="left")

        form_card = tk.Frame(
            content_area, 
            bg=bg_white, 
            highlightbackground=border_col, 
            highlightthickness=1,
            padx=25,
            pady=25
        )
        form_card.pack(fill="x", anchor="w")
        
        tk.Label(
            form_card, 
            text="Buat Komunitas Baru", 
            font=("Poppins", 12, "bold"), 
            bg=bg_white, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 15))
        
        tk.Label(form_card, text="Nama Komunitas", font=("Poppins", 9), bg=bg_white, fg=text_dark).pack(anchor="w")
        self.ent_name = tk.Entry(form_card, font=("Poppins", 10), bg=bg_white, fg="black", width=40)
        self.ent_name.pack(anchor="w", pady=(5, 15))

        tk.Label(form_card, text="Deskripsi Komunitas", font=("Poppins", 9), bg=bg_white, fg=text_dark).pack(anchor="w")
        self.ent_description = tk.Text(form_card, font=("Poppins", 10), bg=bg_white, fg="black", height=4, width=50)
        self.ent_description.pack(anchor="w", pady=(5, 20))
        
        tk.Frame(form_card, height=1, bg=border_col).pack(fill="x", pady=(0, 15))
        
        def create_comunity_action():
            user_id = current_user.id
            name = self.ent_name.get().strip()
            description = self.ent_description.get("1.0", tk.END).strip()

            if not name or not description:
                messagebox.showwarning("Peringatan", "Semua field form wajib diisi!")
                return

            res = self.comunity_logic.create_comunity_logic(user_id, name, description)

            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                # Kosongkan form input setelah sukses
                self.ent_name.delete(0, tk.END)
                self.ent_description.delete("1.0", tk.END)
                # Refresh data tabel otomatis
                self.communities_data = self.comunity_logic.get_comunity_logic()
                self.load_data(self.communities_data)

        btn_submit = tk.Button(
            form_card, 
            text="➕ Buat Komunitas", 
            command=create_comunity_action,
            bg=bg_primary, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat", padx=20, pady=8, cursor="hand2"
        )
        btn_submit.pack(side="left", padx=(0, 10))

        btn_back = tk.Button(
            form_card, 
            text="Kembali", 
            command=go_dashboard,
            bg=bg_main, 
            fg=text_dark, 
            font=("Poppins", 9),
            relief="flat", padx=15, pady=8, cursor="hand2"
        )
        btn_back.pack(side="left")

        self.load_data(self.communities_data)

    # Logic
    def load_data(self, communities_data):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if communities_data:
            for row in communities_data:
                self.tree.insert("", "end", values=(row[0], row[2], row[3]))
            
    def get_selected_community_id(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0])['values'][0]
        return None

    def handle_edit(self):
        community_id = self.get_selected_community_id()
        if not community_id:
            messagebox.showwarning("Peringatan", "Silahkan pilih komunitas dari tabel untuk diedit!")
            return
        print(f"Edit ID: {community_id}")

    def handle_delete(self):
        community_id = self.get_selected_community_id()
        if not community_id:
            messagebox.showwarning("Peringatan", "Silahkan pilih komunitas dari tabel untuk dihapus!")
            return
        
        user_res = messagebox.askyesno("Konfirmasi Hapus", "Apakah Anda yakin ingin menghapus komunitas ini secara permanen?")
        if user_res:
            messagebox.showinfo("Sukses", "Komunitas berhasil dihapus!")
            self.communities_data = self.comunity_logic.get_comunity_logic()
            self.load_data(self.communities_data)