import tkinter as tk
from tkinter import messagebox
from constrants import *

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

# Logic
from logic import User_Profile, Follow_Logic # Tambahkan Follow_Logic di sini

# App
class UserProfileFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.config(bg=bg_main)
        self.change_user_profile = User_Profile()
        self.follow_backend = Follow_Logic() # Inisialisasi logic follow

        # Ambil data total follower & following dari database
        # Amankan dengan try-except atau default ke 0 jika fungsi belum siap
        try:
            self.total_followers = self.follow_backend.get_follower_count_logic(current_user.id)
            self.total_following = self.follow_backend.get_following_count_logic(current_user.id)
        except Exception:
            self.total_followers = 0
            self.total_following = 0

        render_role_sidebar(self, current_user, "")
        main_header(self, current_user, "User Profile")
        
        content_area = tk.Frame(self, bg=bg_main, padx=40, pady=40)
        content_area.pack(side="left", fill="both", expand=True)
        
        profile_card = tk.Frame(
            content_area, 
            bg=bg_white, 
            highlightbackground=border_col, 
            highlightthickness=1,
            padx=30,
            pady=30
        )
        profile_card.pack(anchor="nw", fill="x")
        
        # --- SEKTOR ATAS: AVATAR & STATISTIK (FOLLOWER/FOLLOWING) ---
        header_profile = tk.Frame(profile_card, bg=bg_white)
        header_profile.pack(fill="x", pady=(0, 20))

        avatar_frame = tk.Frame(header_profile, bg=bg_primary, width=80, height=80)
        avatar_frame.pack(side="left", anchor="w")
        avatar_frame.pack_propagate(False)
        
        initial_letter = current_user.username[0].upper() if current_user.username else "?"
        tk.Label(
            avatar_frame, 
            text=initial_letter, 
            fg=bg_white, 
            bg=bg_primary, 
            font=("Poppins", 26, "bold")
        ).pack(expand=True)
        
        # Container Statistik di sebelah kanan Avatar
        stats_frame = tk.Frame(header_profile, bg=bg_white, padx=30)
        stats_frame.pack(side="left", fill="y")
        
        # Kotak Follower
        follower_box = tk.Frame(stats_frame, bg=bg_white, padx=15)
        follower_box.pack(side="left", fill="y")
        tk.Label(follower_box, text=str(self.total_followers), font=("Poppins", 16, "bold"), bg=bg_white, fg=text_dark).pack()
        tk.Label(follower_box, text="Pengikut", font=("Poppins", 9), bg=bg_white, fg=text_muted).pack()

        # Kotak Following
        following_box = tk.Frame(stats_frame, bg=bg_white, padx=15)
        following_box.pack(side="left", fill="y")
        tk.Label(following_box, text=str(self.total_following), font=("Poppins", 16, "bold"), bg=bg_white, fg=text_dark).pack()
        tk.Label(following_box, text="Mengikuti", font=("Poppins", 9), bg=bg_white, fg=text_muted).pack()
        
        # --- SEKTOR TENGAH: INFORMASI DATA AKUN ---
        tk.Label(
            profile_card, 
            text="Informasi Akun", 
            font=("Poppins", 13, "bold"), 
            bg=bg_white, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 10))
        
        tk.Label(profile_card, text="Username", font=("Poppins", 9), bg=bg_white, fg=text_muted).pack(anchor="w")
        lbl_username = tk.Label(
            profile_card, 
            text=current_user.username, 
            font=("Poppins", 11, "bold"), 
            bg=bg_white, 
            fg=text_dark
        )
        lbl_username.pack(anchor="w", pady=(0, 15))
        
        tk.Label(profile_card, text="Role Akses", font=("Poppins", 9), bg=bg_white, fg=text_muted).pack(anchor="w")
        lbl_role = tk.Label(
            profile_card, 
            text=current_user.role.upper(), 
            font=("Poppins", 9, "bold"), 
            bg=border_col, 
            fg=bg_secondary,
            padx=10,
            pady=3
        )
        lbl_role.pack(anchor="w", pady=(0, 20))
        
        tk.Frame(profile_card, height=1, bg=border_col).pack(fill="x", pady=(0, 20))
        
        # --- SEKTOR BAWAH: ACTION BUTTONS LAYOUT (HORIZONTAL) ---
        actions_frame = tk.Frame(profile_card, bg=bg_white)
        actions_frame.pack(fill="x", anchor="w")

        def back_to_dashboard():
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
                res = self.change_user_profile.delete_user_logic(user_id)
                if res["status"] == "Error":
                    messagebox.showerror(res["message"][0], res["message"][1])
                    return
                if res["status"] == "Success":
                    messagebox.showinfo(res["message"][0], res["message"][1])
                    from gui.frames.auth.login import LoginFrame
                    self.master.switch_frame(LoginFrame, auth_success=self.master.auth_success)              

        btn_back = tk.Button(
            actions_frame, 
            text="🔙 Kembali", 
            command=back_to_dashboard,
            bg="#F3F4F6", 
            fg=text_dark, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn_back.pack(side="left", padx=(0, 10))

        btn_ganti = tk.Button(
            actions_frame, 
            text="✏️ Ganti Username", 
            command=ganti,
            bg=bg_primary, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn_ganti.pack(side="left", padx=(0, 10))

        btn_hapus = tk.Button(
            actions_frame, 
            text="🗑️ Hapus Akun", 
            command=hapus,
            bg="#FF4D4D", 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        btn_hapus.pack(side="right")
        
        # Hover Animations
        btn_back.bind("<Enter>", lambda e: btn_back.config(bg=border_col))
        btn_back.bind("<Leave>", lambda e: btn_back.config(bg="#F3F4F6"))
        
        btn_ganti.bind("<Enter>", lambda e: btn_ganti.config(bg=bg_secondary))
        btn_ganti.bind("<Leave>", lambda e: btn_ganti.config(bg=bg_primary))
        
        btn_hapus.bind("<Enter>", lambda e: btn_hapus.config(bg="#CC3D3D"))
        btn_hapus.bind("<Leave>", lambda e: btn_hapus.config(bg="#FF4D4D"))