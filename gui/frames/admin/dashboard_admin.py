# GUI
import tkinter as tk
from tkinter import messagebox
from constrants import *

# Components
from gui.components.sidebar import sidebar
from gui.components.header import main_header

class DashboardAdminFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        # Navigate to Home Screen
        def go_dashboard_admin():
            self.master.switch_frame(
            DashboardAdminFrame,
            current_user=self.master.current_user
        )
             
        # Navigate to Activity Screen
        def go_user_management():
            from gui.frames.admin.user_management import UserManagementFrame

            self.master.switch_frame(
            UserManagementFrame,
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