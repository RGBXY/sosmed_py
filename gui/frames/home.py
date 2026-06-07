import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.post_form import PostForm
from gui.components.header import main_header
from gui.components.post_card import CreatePostCard
from gui.utils.navigation import render_role_sidebar

class HomeFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent)        
        self.post_data = {"id": 1, "username": "derre", "role": "admin", "content": "Halo...", "timestamp": "2 jam yang lalu"}

        render_role_sidebar(self, current_user, "Home")

        right_container = tk.Frame(self, bg=bg_main)
        right_container.pack(side="left", fill="both", expand=True)
        
        main_header(right_container, current_user, "Home")

        feed_area = tk.Frame(right_container, bg=bg_main, padx=20, pady=20)
        feed_area.pack(fill="both", expand=True, side="left")

        side_content = tk.Frame(right_container, bg=bg_main, padx=20, pady=20)
        side_content.pack(fill="both", expand=True, side="left")

        tk.Label(side_content, text="galo").pack()

        PostForm(feed_area, current_user)

        CreatePostCard(feed_area, self.post_data, current_user, on_delete_callback=None)