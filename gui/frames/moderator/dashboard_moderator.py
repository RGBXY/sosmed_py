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
             
        def go_dashboard():
            from gui.frames.moderator.dashboard_moderator import DashboardModerator

            self.master.switch_frame(
                DashboardModerator,
                current_user=self.master.current_user
            )

        def go_comunity():
            from gui.frames.moderator.comunity import CommunityFrame

            self.master.switch_frame(
                CommunityFrame,
                current_user=current_user
            )
        
        nav_items = [
            {
                "title": "Home",
                "comand": go_home,
                "active": False
            },
            {
                "title": "Dashboard",
                "comand": go_dashboard,
                "active": True
            },
            {
                "title": "Comunity",
                "comand": go_comunity,
                "active": False
            }
        ]
        
        sidebar(self, current_user, nav_items)
        main_header(self, current_user, "Dashboard Moderator")