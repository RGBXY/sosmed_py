import tkinter as tk
from data import init_db
from gui import LoginApp

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Social Media")
        init_db()
        
        self.current_user = None
        self.login()
        
    def login(self):
        login = LoginApp(self)
        login.pack(fill="both", expand=True)
            
Main().mainloop()