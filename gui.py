import tkinter as tk
from tkinter import messagebox, ttk
from logic import Auth

# Color
bg_main      = "#EFF2F7"
bg_          = "#EFF2F7"
bg_primary   = "#6C6FF1"
bg_secondary = "#5759BB"
bg_white     = "#ffffff"
text_muted   = "#9496B0"
text_dark    = "#1C1D3A"
border_col   = "#E2E5F5"
 
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
 
    return sidebar_frame
 
# Main Header
def main_header(parent, current_user, screen_name):
    main_frame = tk.Frame(parent, bg=bg_main)
    main_frame.pack(side="left", expand=True, fill="both")
 
    tk.Label(main_frame, text=f"Welcome to {screen_name} {current_user.username}", font=("Poppins", 14, "bold"), bg=bg_white, fg=text_dark, height=4, padx=20).pack(fill="x")
    tk.Frame(main_frame, height=2, bg=bg_primary).pack(fill="x")
 
    return main_frame
# Login Frame
class LoginApp(tk.Frame):
    def __init__(self, parent, login_success):
        super().__init__(parent)   
        self.auth = Auth() 
        self.user = None
        self.login_success = login_success
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
                
                self.login_success(self.user)
                
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
             
        nav_items = [
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
        
        main_header(self, current_user, "Home Screen")
        
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