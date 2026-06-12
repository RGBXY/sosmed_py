# GUI
import tkinter as tk
from tkinter import messagebox
from constrants import *

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

class DashboardAdminFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        
        render_role_sidebar(self, current_user, "Dashboard_Admin")
        main_header(self,current_user, "Dashboard")  