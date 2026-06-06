import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.sidebar import sidebar
from gui.components.header import main_header
from logic import User_Profile

class FormUserProfileFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.config(bg=bg_main)
        self.change_user_profile = User_Profile()
        
        # 1. Navigasi Fungsi Sidebar
        def go_home():
            from gui.frames.home import HomeFrame

            self.master.switch_frame(
                HomeFrame,
                current_user=self.master.current_user
            )
             
        def go_activity():
            from gui.frames.comunity import ComunityFrame

            self.master.switch_frame(
                ComunityFrame,
                current_user=self.master.current_user
            )
        
        # Navigasi Menu Sidebar
        nav_items = [
            {
                "title": "Home",
                "comand": go_home,
                "active": False
            },
            {
                "title": "Comunity",
                "comand": go_activity,
                "active": False
            }
        ]
        
        # 2. Render Komponen Global (Sidebar & Header)
        sidebar(self, current_user, nav_items)
        main_header(self, current_user, "User Profile")

        def back_to_profile():
            from gui.frames.user_profile import UserProfileFrame

            self.master.switch_frame(
                UserProfileFrame,
                current_user=self.master.current_user
            )

        def change_username():
            current_username = current_user.username
            new_username = self.ent_new_username.get()

            res = self.change_user_profile.change_username(current_username, new_username)

            print(res)

            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.master.current_user = res["data"]

            back_to_profile()
        
        # 3. Kontainer Utama Konten (Mengisi sisa area kanan)
        content_area = tk.Frame(self, bg=bg_main, padx=40, pady=40)
        content_area.pack(side="left", fill="both", expand=True)
        
        # 4. Profile Card (Kotak Putih Modern)
        profile_card = tk.Frame(
            content_area, 
            bg=bg_white, 
            highlightbackground=border_col, 
            highlightthickness=1,
            padx=30,
            pady=30
        )
        profile_card.pack(anchor="nw", fill="x") # Batasi lebar card agar rapi
        
        # Detail Informasi User
        tk.Label(
            profile_card, 
            text="Ganti Username", 
            font=("Poppins", 14, "bold"), 
            bg=bg_white, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 10))
        
        # Field: Role
        self.ent_new_username = tk.Entry(profile_card, font=("Poppins", 9), bg=bg_white, fg=text_muted)
        self.ent_new_username.pack(anchor="w", pady=(0, 20))
        
        # Pembatas Garis Halus
        tk.Frame(profile_card, height=1, bg=border_col).pack(fill="x", pady=(0, 20))
        
        # Tombol Aksi (Contoh: Kembali ke Dashboard)
        def back_to_dashboard():
            # Mengarahkan user berdasarkan role-nya masing-masing
            if current_user.role.lower() == "admin":
                from gui.frames.admin.dashboard_admin import DashboardAdminFrame
                self.master.switch_frame(DashboardAdminFrame, current_user=current_user)
            elif current_user.role.lower() == "moderator":
                from gui.frames.moderator.dashboard_moderator import DashboardModeratorFrame
                self.master.switch_frame(DashboardModeratorFrame, current_user=current_user)
            else:
                from gui.frames.home import HomeFrame
                self.master.switch_frame(HomeFrame, current_user=current_user)

        btn_back = tk.Button(
            profile_card, 
            text="Kembali ke Dashboard", 
            command=back_to_dashboard,
            bg=bg_primary, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn_back.pack(anchor="w")

        btn_submit = tk.Button(
            profile_card, 
            text="Ganti Username", 
            command=change_username,
            bg=bg_primary, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn_submit.pack(anchor="w")
        
        # Efek Hover Tombol
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg=bg_secondary))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg=bg_primary))