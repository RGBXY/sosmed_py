import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.sidebar import sidebar
from gui.components.header import main_header

class HomeFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)        
        
        def go_home():
            self.master.switch_frame(
            HomeFrame,
            current_user=self.master.current_user
        )
             
        def go_activity():
            from gui.frames.comunity import ComunityFrame

            self.master.switch_frame(
            ComunityFrame,
            current_user=self.master.current_user
        )
             
        def go_profile():
            from gui.frames.user_profile import UserProfileFrame

            self.master.switch_frame(
            UserProfileFrame,
            current_user=self.master.current_user
        )
             
        nav_items = [
            {
                "title": "Profile",
                "comand": go_profile,
                "active": False,
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