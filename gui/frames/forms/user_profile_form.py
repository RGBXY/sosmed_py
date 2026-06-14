import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import User_Profile

class FormUserProfileFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.config(bg=bg_main)
        self.current_user = current_user
        self.change_user_profile = User_Profile()

        # Render Sidebar & Header bawaan proyek
        render_role_sidebar(self, current_user, active_title="User Profile")
        main_header(self, current_user, "User Profile")
        
        # --- UI LAYOUT CONTAINER ---
        content_area = tk.Frame(self, bg=bg_main, padx=40, pady=40)
        content_area.pack(side="left", fill="both", expand=True)
        
        # Profile Card Container
        profile_card = tk.Frame(
            content_area, 
            bg=bg_white, 
            highlightbackground=border_col, 
            highlightthickness=1,
            padx=35,
            pady=35
        )
        profile_card.pack(anchor="nw", fill="x") # Batasi lebar maksimal kartu agar estetik
        
        # Judul Form
        tk.Label(
            profile_card, 
            text="Ganti Username", 
            font=("Poppins", 14, "bold"), 
            bg=bg_white, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 4))

        # Deskripsi Bantuan Kecil
        tk.Label(
            profile_card, 
            text="Gunakan username unik baru untuk akun sosial media Anda.", 
            font=("Poppins", 9), 
            bg=bg_white, 
            fg=text_muted
        ).pack(anchor="w", pady=(0, 20))
        
        # Modernisasi Input Entry (Diberikan Padding & Frame Border)
        entry_container = tk.Frame(profile_card, bg=border_col, padx=1, pady=1)
        entry_container.pack(anchor="w", fill="x", pady=(0, 25))

        self.ent_new_username = tk.Entry(
            entry_container, 
            font=("Poppins", 10), 
            bg=bg_white, 
            fg=text_dark,
            bd=0,
            insertbackground=text_dark
        )
        # Memberikan efek padding internal pada teks entry
        self.ent_new_username.pack(fill="both", expand=True, padx=10, pady=8)
        self.ent_new_username.insert(0, self.current_user.username) # Isi dengan username lama secara otomatis
        
        # Separator Garis Tipis
        tk.Frame(profile_card, height=1, bg=border_col).pack(fill="x", pady=(0, 25))
        
        # --- BUTTON ACTIONS CONTAINER (Jajar Horizontal) ---
        btn_container = tk.Frame(profile_card, bg=bg_white)
        btn_container.pack(anchor="w", fill="x")

        # Tombol Submit (Utama - Di Sebelah Kiri)
        self.btn_submit = tk.Button(
            btn_container, 
            text="Simpan Perubahan", 
            command=self.change_username,
            bg=bg_primary, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_submit.pack(side="left") # Menggunakan side="left" agar berjajar horizontal
        
        # Tombol Kembali (Sekunder - Di Sebelah Kanan Tombol Submit)
        self.btn_back = tk.Button(
            btn_container, 
            text="Kembali", 
            command=self.back_to_dashboard,
            bg="#F3F4F6", # Menggunakan warna abu-abu netral agar kontras tombol utama terlihat kuat
            fg="#4B5563", 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_back.pack(side="left", padx=(10, 0))

        # --- EVENT HOVER BINDING ---
        self.btn_submit.bind("<Enter>", lambda e: self.btn_submit.config(bg=bg_secondary))
        self.btn_submit.bind("<Leave>", lambda e: self.btn_submit.config(bg=bg_primary))
        
        self.btn_back.bind("<Enter>", lambda e: self.btn_back.config(bg="#E5E7EB", fg=text_dark))
        self.btn_back.bind("<Leave>", lambda e: self.btn_back.config(bg="#F3F4F6", fg="#4B5563"))


    # =========================================================================
    # LOGIC FUNCTIONS (Dipindah Ke Tingkat Class)
    # =========================================================================
    def back_to_profile(self):
        from gui.frames.user_profile import UserProfileFrame
        self.master.switch_frame(
            UserProfileFrame,
            current_user=self.master.current_user
        )

    def change_username(self):
        current_username = self.current_user.username
        new_username = self.ent_new_username.get().strip()

        if not new_username:
            messagebox.showwarning("Input Kosong", "Username baru tidak boleh kosong!")
            return

        res = self.change_user_profile.change_username_logic(current_username, new_username)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.master.current_user = res["data"]

        self.back_to_profile()

    def back_to_dashboard(self):
        role = self.current_user.role.lower()
        if role == "admin":
            from gui.frames.admin.dashboard_admin import DashboardAdminFrame
            self.master.switch_frame(DashboardAdminFrame, current_user=self.current_user)
        elif role == "moderator":
            from gui.frames.moderator.dashboard_moderator import DashboardModeratorFrame
            self.master.switch_frame(DashboardModeratorFrame, current_user=self.current_user)
        else:
            from gui.frames.home import HomeFrame
            self.master.switch_frame(HomeFrame, current_user=self.current_user)