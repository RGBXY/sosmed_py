import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.sidebar import sidebar
from gui.components.header import main_header

class ComunityFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        # Navigate to Home Screen
        def go_home():
            from gui.frames.home import HomeFrame

            self.master.switch_frame(
            HomeFrame,
            current_user=self.master.current_user
        )
             
        # Navigate to Activity Screen
        def go_activity():
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
                "active": True
            }
        ]
        
        sidebar(self, current_user, nav_items)
        main_header(self, current_user, "Activity Screen")