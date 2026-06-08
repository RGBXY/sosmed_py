import tkinter as tk
from tkinter import messagebox
from constrants import *

def main_header(parent, current_user, screen_name):
    # Main container untuk seluruh header
    main_frame = tk.Frame(parent, bg=bg_main)
    main_frame.pack(side="top", fill="x", anchor="n") 

    content_frame = tk.Frame(main_frame, bg=bg_white)
    content_frame.pack(fill="x", side="top")

    def go_profile():
        from gui.frames.user_profile import UserProfileFrame

        window_parent = parent.winfo_toplevel()
        
        window_parent.switch_frame(
            UserProfileFrame,
            current_user=current_user
        )

    # Label Header
    tk.Label(
        content_frame, 
        text=f"{screen_name}", 
        font=("Poppins", 14, "bold"), 
        bg=bg_white, 
        fg=text_dark, 
        height=4, 
        padx=20
    ).pack(side="left")

    # Profile Button
    tk.Button(
        content_frame, 
        text="Profile", 
        font=("Poppins", 11), 
        bg=bg_white, 
        fg=text_dark,
        padx=20,
        relief="flat",
        command=go_profile
    ).pack(side="right") 

    # Garis
    tk.Frame(main_frame, height=2, bg=bg_primary).pack(fill="x", side="top")
 
    return main_frame