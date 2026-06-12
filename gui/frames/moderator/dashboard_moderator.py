import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.sidebar import sidebar
from gui.components.header import main_header
from gui.utils.navigation import render_role_sidebar

class DashboardModerator(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        render_role_sidebar(self, current_user, "Dashboard_Moderator")
        main_header(self, current_user, "Dashboard Moderator")