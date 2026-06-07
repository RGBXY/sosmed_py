# GUI
import tkinter as tk
from tkinter import messagebox
from constrants import *

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

# Logic
from logic import User_Profile

# App
class UserProfileFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.config(bg=bg_main)
        self.change_user_profile = User_Profile()

        render_role_sidebar(self, current_user, "")
       
        main_header(self, current_user, "User Profile")
        
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
        
        # Avatar Placeholder (Inisial nama user lingkaran / box)
        avatar_frame = tk.Frame(profile_card, bg=bg_primary, width=70, height=70)
        avatar_frame.pack(anchor="w", pady=(0, 15))
        avatar_frame.pack_propagate(False)
        
        # Mengambil huruf pertama username untuk avatar
        initial_letter = current_user.username[0].upper() if current_user.username else "?"
        tk.Label(
            avatar_frame, 
            text=initial_letter, 
            fg=bg_white, 
            bg=bg_primary, 
            font=("Poppins", 24, "bold")
        ).pack(expand=True)
        
        # Detail Informasi User
        tk.Label(
            profile_card, 
            text="Informasi Akun", 
            font=("Poppins", 14, "bold"), 
            bg=bg_white, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 10))
        
        # Field: Username
        tk.Label(profile_card, text="Username", font=("Poppins", 9), bg=bg_white, fg=text_muted).pack(anchor="w")
        lbl_username = tk.Label(
            profile_card, 
            text=current_user.username, 
            font=("Poppins", 11, "bold"), 
            bg=bg_white, 
            fg=text_dark
        )
        lbl_username.pack(anchor="w", pady=(0, 15))
        
        # Field: Role
        tk.Label(profile_card, text="Role Akses", font=("Poppins", 9), bg=bg_white, fg=text_muted).pack(anchor="w")
        lbl_role = tk.Label(
            profile_card, 
            text=current_user.role.upper(), 
            font=("Poppins", 10, "bold"), 
            bg=border_col, # Efek badge background
            fg=text_dark,
            padx=10,
            pady=2
        )
        lbl_role.pack(anchor="w", pady=(0, 20))
        
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

        def ganti():
            from gui.frames.forms.user_profile_form import FormUserProfileFrame
            self.master.switch_frame(FormUserProfileFrame, current_user=current_user)

        def hapus():
            res_user = messagebox.askyesno("Hapus Akun", "Apakah yakin anda ingin menghapus akun anda?")

            if res_user:
                user_id = current_user.id

                print(user_id)
                res = self.change_user_profile.delete_user_logic(user_id)

                if res["status"] == "Error":
                    messagebox.showerror(res["message"][0], res["message"][1])
                    return
                
                if res["status"] == "Success":
                    messagebox.showinfo(res["message"][0], res["message"][1])

                    from gui.frames.auth.login import LoginFrame
                    self.master.switch_frame(LoginFrame, auth_success=self.master.auth_success)              

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

        btn_ganti = tk.Button(
            profile_card, 
            text="Ganti username", 
            command=ganti,
            bg=bg_primary, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn_ganti.pack(anchor="w")

        btn_hapus = tk.Button(
            profile_card, 
            text="hapus akun", 
            command=hapus,
            bg=bg_primary, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn_hapus.pack(anchor="w")
        
        # Efek Hover Tombol
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg=bg_secondary))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg=bg_primary))