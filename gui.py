import tkinter as tk
from tkinter import messagebox, ttk
from logic import Auth
# Color
bg_main = "#EFF2F7"
bg_primary = "#6C6FF1"
bg_secondary = "#5759BB"
bg_white = "#ffffff"

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
        
class Home(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        tk.Label(self, text=f"Welcome to Home screen {current_user.username}").pack()
        
class Dashboard_moderator(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        tk.Label(self, text=f"Welcome to Dashboard Moderator Screen {current_user.username}").pack()
        
class Dashboard_admin(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        tk.Label(self, text=f"Welcome to Dashboard Admin Screen {current_user.username}").pack()