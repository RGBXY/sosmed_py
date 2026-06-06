import tkinter as tk
from data import init_db, register_user_auth
from gui.frames.auth.login import LoginFrame
from gui.frames.home import HomeFrame
from gui.frames.admin.dashboard_admin import DashboardAdminFrame
from gui.frames.moderator.dashboard_moderator import DashboardModerator

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.title("Social Media")
        init_db()
        
        self.current_user = None
        self.current_frame = None
        self.open_login()
        
    # Roting Function
    def switch_frame(self, frame_class, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)
        
    # Login GUI Function
    def open_login(self):        
        self.switch_frame(LoginFrame, auth_success=self.auth_success)

    def logout(self):
        self.current_user = None
        self.switch_frame(LoginFrame, auth_success=self.auth_success)
                
    # Callback for Register and Login
    def auth_success(self, user):
        self.current_user = user

        if user.role == "user":
            self.switch_frame(HomeFrame, current_user=self.current_user)
            
        elif user.role == "moderator":
            self.switch_frame(DashboardModerator, current_user=self.current_user)

        elif user.role == "admin":
            self.switch_frame(DashboardAdminFrame, current_user=self.current_user)        

    
    register_user_auth("dodi", "haidsh")
Main().mainloop()