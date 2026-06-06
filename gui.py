import tkinter as tk
from tkinter import messagebox, ttk
from logic import Auth, User_Profile

# Color
bg_main      = "#EFF2F7"
bg_          = "#EFF2F7"
bg_primary   = "#6C6FF1"
bg_secondary = "#5759BB"
bg_white     = "#ffffff"
text_muted   = "#9496B0"
text_dark    = "#1C1D3A"
border_col   = "#E2E5F5"

# Logout Fnc for Button
def logout(parent):
    cheack = messagebox.askyesno("Keluar", "Apakah yakin ingin keluar?")
    
    if cheack:
        parent.master.logout()
    else:
        return
 
# Sidebar
def sidebar(parent, current_user, nav_items):
    sidebar_frame = tk.Frame(parent, width=320, bg=bg_white,
                             highlightbackground=border_col, highlightthickness=1)
    sidebar_frame.pack(side="left", fill="y")
    sidebar_frame.pack_propagate(False)
 
    nav_header_frame = tk.Frame(sidebar_frame, padx=20, pady=20, bg=bg_white)
    nav_header_frame.pack(fill="x")
 
    # Sidebar Header
    tk.Label(nav_header_frame, text=current_user.username,
             bg=bg_white, fg=text_dark, font=("Poppins", 12, "bold")).pack(anchor="w")
    tk.Label(nav_header_frame, text=current_user.role,
             bg=bg_white, fg=text_muted, font=("Poppins", 8)).pack(anchor="w")
 
    tk.Frame(sidebar_frame, height=1, bg=border_col).pack(fill="x", padx=16, pady=4)
    
    
    for i in nav_items:
        is_active = i.get("active", False)
        tk.Button(sidebar_frame, text=f"  {i['title']}",
                  command=i["comand"],
                  bg=bg_primary if is_active else bg_white,
                  fg=bg_white   if is_active else text_dark,
                  relief="flat", font=("Poppins", 9),
                  anchor="w", padx=12, pady=8, cursor="hand2"
        ).pack(fill="x", padx=12, pady=2)

    tk.Button(sidebar_frame, text="  Logout",
                  command=lambda:logout(parent),
                  bg=bg_primary if is_active else bg_white,
                  fg=bg_white   if is_active else text_dark,
                  relief="flat", font=("Poppins", 9),
                  anchor="w", padx=12, pady=8, cursor="hand2"
        ).pack(fill="x", padx=12, pady=2, anchor="s")
 
    return sidebar_frame
 
# Main Header
def main_header(parent, current_user, screen_name):
    # Main container untuk seluruh header
    main_frame = tk.Frame(parent, bg=bg_main)
    main_frame.pack(side="top", fill="x", anchor="n") # Diubah ke side="top" agar horizontal full di atas

    # 1. Buat kontainer khusus untuk konten (Screen Name & Profile) biar bisa justify-between
    content_frame = tk.Frame(main_frame, bg=bg_white)
    content_frame.pack(fill="x", side="top")

    # KIRI: Screen Name
    tk.Label(
        content_frame, 
        text=f"{screen_name}", 
        font=("Poppins", 14, "bold"), 
        bg=bg_white, 
        fg=text_dark, 
        height=4, 
        padx=20
    ).pack(side="left") # Tarik ke kiri mentok

    # KANAN: Profile
    tk.Button(
        content_frame, 
        text="Profile", 
        font=("Poppins", 11), 
        bg=bg_white, 
        fg=text_dark,
        padx=20,
        relief="flat"
    ).pack(side="right") # Tarik ke kanan mentok (Ini kunci "space-between"-nya!)

    # 2. Garis pembagi (Border bawah/Line) ditaruh di bawah content_frame
    tk.Frame(main_frame, height=2, bg=bg_primary).pack(fill="x", side="top")
 
    return main_frame

# Login Frame
class LoginApp(tk.Frame):
    def __init__(self, parent, auth_success):
        super().__init__(parent)   
        self.auth = Auth() 
        self.user = None
        self.auth_success = auth_success
        self.config(bg=bg_main)
        
        def btn_on_enter(e):
            btn_login.config(bg=bg_secondary)
            
        def btn_on_leave(e):
            btn_login.config(bg=bg_primary)
            
        def login():
            ent_username = self.ent_name.get()
            ent_password = self.ent_password.get()
            res = self.auth.login(ent_username, ent_password)
                        
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.user = res["data"]
                print(self.user.username)
                
                self.auth_success(self.user)

        def go_register():
            self.master.switch_frame(
                RegisterApp, 
                auth_success=self.master.auth_success
            )
                
        form_frame = tk.Frame(self, bg=bg_white)
        form_frame.pack(expand=True, ipadx=24)
            
        tk.Label(form_frame, text="Login to Hubble", font=("Poppins", 20), bg=bg_white).pack(pady=(20))
        
        tk.Label(form_frame, text="Username", font=("Poppins", 8), bg=bg_white).pack(anchor="w", padx=20)
        self.ent_name = tk.Entry(form_frame, width=45, bd=1, relief="solid")
        self.ent_name.pack(ipady=4)
        
        tk.Label(form_frame, text="Password", font=("Poppins", 8), bg=bg_white).pack(anchor="w", pady=(10, 0), padx=20)
        self.ent_password = tk.Entry(form_frame, show="*", width=45, bd=1, relief="solid")
        self.ent_password.pack(ipady=4)
        
        btn_login = tk.Button(form_frame, text="LOGIN", command=login, width=38, bg=bg_primary, foreground=bg_white, height=2, font=("Poppins", 9, "bold"))
        btn_login.pack(pady=(30))
        btn_login.bind("<Enter>", btn_on_enter)
        btn_login.bind("<Leave>", btn_on_leave)

        btn_change_register = tk.Button(form_frame, command=go_register, text="Register", relief="flat")
        btn_change_register.pack(pady=(0, 30))

# Register Frame
class RegisterApp(tk.Frame):
    def __init__(self, parent, auth_success):
        super().__init__(parent)

        self.auth = Auth() 
        self.user = None
        self.auth_success = auth_success
        self.config(bg=bg_main)
        
        def btn_on_enter(e):
            btn_login.config(bg=bg_secondary)
            
        def btn_on_leave(e):
            btn_login.config(bg=bg_primary)
            
        def register():
            ent_username = self.ent_name.get()
            ent_password = self.ent_password.get()
            ent_confirm_password = self.ent_confirm_password.get()
            res = self.auth.register(ent_username, ent_password, ent_confirm_password)
                        
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.user = res["data"]
                print(self.user.username)
                
                self.auth_success(self.user)

        def go_login():
            self.master.switch_frame(
                LoginApp, 
                auth_success=self.master.auth_success
            )
                
        form_frame = tk.Frame(self, bg=bg_white)
        form_frame.pack(expand=True, ipadx=24)
            
        tk.Label(form_frame, text="Register to Hubble", font=("Poppins", 20), bg=bg_white).pack(pady=(20))
        
        tk.Label(form_frame, text="Username", font=("Poppins", 8), bg=bg_white).pack(anchor="w", padx=20)
        self.ent_name = tk.Entry(form_frame, width=45, bd=1, relief="solid")
        self.ent_name.pack(ipady=4)
        
        tk.Label(form_frame, text="Password", font=("Poppins", 8), bg=bg_white).pack(anchor="w", pady=(10, 0), padx=20)
        self.ent_password = tk.Entry(form_frame, show="*", width=45, bd=1, relief="solid")
        self.ent_password.pack(ipady=4)

        tk.Label(form_frame, text="Confirm Password", font=("Poppins", 8), bg=bg_white).pack(anchor="w", pady=(10, 0), padx=20)
        self.ent_confirm_password = tk.Entry(form_frame, show="*", width=45, bd=1, relief="solid")
        self.ent_confirm_password.pack(ipady=4)
        
        btn_login = tk.Button(form_frame, text="REGISTER", command=register, width=38, bg=bg_primary, foreground=bg_white, height=2, font=("Poppins", 9, "bold"))
        btn_login.pack(pady=(30))
        btn_login.bind("<Enter>", btn_on_enter)
        btn_login.bind("<Leave>", btn_on_leave)

        btn_change_login = tk.Button(form_frame, command=go_login, text="Login", relief="flat")
        btn_change_login.pack(pady=(0, 30))

        
# Home Frame   
class Home(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)        
             
        
        def go_home():
             self.master.switch_frame(
            Home,
            current_user=self.master.current_user
        )
             
        def go_activity():
             self.master.switch_frame(
            Comunity,
            current_user=self.master.current_user
        )
             
        def go_profile():
             self.master.switch_frame(
            User_profile,
            current_user=self.master.current_user
        )
             
        nav_items = [
            {
                "title": "Profile",
                "comand": go_profile,
                "active": False
            },
            {
                "title": "Home",
                "comand": go_home,
                "active": True
            },
            {
                "title": "Comunity",
                "comand": go_activity,
                "active": False
            }
        ]
             
        sidebar(self, current_user, nav_items)
        
        main_header(self, current_user, "Home")
        
# Comunity Frame
class Comunity(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        # Navigate to Home Screen
        def go_home():
             self.master.switch_frame(
            Home,
            current_user=self.master.current_user
        )
             
        # Navigate to Activity Screen
        def go_activity():
             self.master.switch_frame(
            Comunity,
            current_user=self.master.current_user
        )
             
        nav_items = [
            {
                "title": "Home",
                "comand": go_home,
                "active": False
            },
            {
                "title": "Comunity",
                "comand": go_activity,
                "active": True
            }
        ]
        
        sidebar(self, current_user, nav_items)
        main_header(self, current_user, "Activity Screen")
        
# Dashboard Moderator Frame
class Dashboard_moderator(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        def go_home():
             self.master.switch_frame(
            Home,
            current_user=self.master.current_user
        )
             
        # Navigate to Activity Screen
        def go_activity():
             self.master.switch_frame(
            Comunity,
            current_user=self.master.current_user
        )
        
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
        
        sidebar(self, current_user, nav_items)
        main_header(self, current_user, "Dashboard Moderator")
         
# Dashboard Admin Frame    
class Dashboard_admin(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        # Navigate to Home Screen
        def go_dashboard_admin():
             self.master.switch_frame(
            Dashboard_admin,
            current_user=self.master.current_user
        )
             
        # Navigate to Activity Screen
        def go_user_management():
             self.master.switch_frame(
            User_management,
            current_user=self.master.current_user
        )
             
        nav_items = [
            {
                "title": "Dashboard",
                "comand": go_dashboard_admin,
                "active": True
            },
            {
                "title": "User Management",
                "comand": go_user_management,
                "active": False
            }
        ]
        
        sidebar(self, current_user, nav_items)
        main_header(self,current_user, "Dashboard")  
        
# User Management Frame
class User_management(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
         # Navigate to Home Screen
        def go_dashboard_admin():
             self.master.switch_frame(
            Dashboard_admin,
            current_user=self.master.current_user
        )
             
        # Navigate to Activity Screen
        def go_user_management():
             self.master.switch_frame(
            User_management,
            current_user=self.master.current_user
        )
             
        nav_items = [
            {
                "title": "Dashboard",
                "comand": go_dashboard_admin,
                "active": False
            },
            {
                "title": "User Management",
                "comand": go_user_management,
                "active": True
            }
        ]
        
        sidebar(self, current_user, nav_items)
        main_header(self,current_user, "User Management")  

# User Profile Frame
class User_profile(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.config(bg=bg_main)
        self.change_user_profile = User_Profile()

        
        # 1. Navigasi Fungsi Sidebar
        def go_home():
            self.master.switch_frame(
                Home,
                current_user=self.master.current_user
            )
             
        def go_activity():
            self.master.switch_frame(
                Comunity,
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
                self.master.switch_frame(Dashboard_admin, current_user=current_user)
            elif current_user.role.lower() == "moderator":
                self.master.switch_frame(Dashboard_moderator, current_user=current_user)
            else:
                self.master.switch_frame(Home, current_user=current_user)

        def ganti():
            self.master.switch_frame(Change_Profile_Data, current_user=current_user)

        def hapus():
            res_user = messagebox.askyesno("Hapus Akun", "Apakah yakin anda ingin menghapus akun anda?")

            if res_user:
                user_id = current_user.id

                print(user_id)
                res = self.change_user_profile.delete_user(user_id)

                if res["status"] == "Error":
                    messagebox.showerror(res["message"][0], res["message"][1])
                    return
                
                if res["status"] == "Success":
                    messagebox.showinfo(res["message"][0], res["message"][1])
                    self.master.switch_frame(LoginApp, auth_success=self.master.auth_success)              

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

class Change_Profile_Data(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.config(bg=bg_main)
        self.change_user_profile = User_Profile()
        
        # 1. Navigasi Fungsi Sidebar
        def go_home():
            self.master.switch_frame(
                Home,
                current_user=self.master.current_user
            )
             
        def go_activity():
            self.master.switch_frame(
                Comunity,
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
            self.master.switch_frame(
                User_profile,
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
                self.master.switch_frame(Dashboard_admin, current_user=current_user)
            elif current_user.role.lower() == "moderator":
                self.master.switch_frame(Dashboard_moderator, current_user=current_user)
            else:
                self.master.switch_frame(Home, current_user=current_user)

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


