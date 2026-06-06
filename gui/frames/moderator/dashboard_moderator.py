import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.sidebar import sidebar
from gui.components.header import main_header

class DashboardModerator(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        def go_home():
            from gui.frames.home import HomeFrame

            self.master.switch_frame(
            HomeFrame,
            current_user=self.master.current_user
        )
             
        # Navigate to Activity Screen
        def go_activity():
            from gui.frames.comunity import ComunityFrame
            self.master.switch_frame(
            ComunityFrame,
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