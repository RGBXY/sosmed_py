import tkinter as tk
from data import init_db
from gui import LoginApp, Home, Dashboard_admin, Dashboard_moderator

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Social Media")
        init_db()
        
        self.current_user = None
        self.open_login()
        
    def open_login(self):
        self.login = LoginApp(self, login_success=self.login_success)
        self.login.pack(fill="both", expand=True)
        
    def login_success(self, user):
        self.current_user = user
        
        if user.role == "user":
            Home(self, current_user=self.current_user).pack()
        elif user.role == "moderator":
            Dashboard_moderator(self, current_user=self.current_user).pack()
        elif user.role == "admin":
            Dashboard_admin(self, current_user=self.current_user).pack()
        
        self.login.destroy()
        
        
                    
Main().mainloop()