import tkinter as tk
from tkinter import messagebox
from constrants import *

def logout(parent):
    cheack = messagebox.askyesno("Keluar", "Apakah yakin ingin keluar?")
    
    if cheack:
        parent.master.logout()
    else:
        return

def sidebar(parent, current_user, nav_items):
    sidebar_frame = tk.Frame(parent, width=320, bg=bg_white,
                             highlightbackground=border_col, highlightthickness=1)
    sidebar_frame.pack(side="left", fill="y")
    sidebar_frame.pack_propagate(False)
 
    nav_header_frame = tk.Frame(sidebar_frame, padx=20, pady=20, bg=bg_white)
    nav_header_frame.pack(fill="x")
 
    # Sidebar Header
    tk.Label(nav_header_frame, text=current_user.username,
             bg=bg_white, fg=text_dark, font=("Poppins", 12, "bold")).pack(anchor="w")
    tk.Label(nav_header_frame, text=current_user.role,
             bg=bg_white, fg=text_muted, font=("Poppins", 8)).pack(anchor="w")
 
    tk.Frame(sidebar_frame, height=1, bg=border_col).pack(fill="both", padx=16, pady=4)
    
    for i in nav_items:
        is_active = i.get("active", False)
        tk.Button(sidebar_frame, text=f"  {i['title']}",
                  command=i["comand"],
                  bg=bg_primary if is_active else bg_white,
                  fg=bg_white   if is_active else text_dark,
                  relief="flat", font=("Poppins", 9),
                  anchor="w", padx=12, pady=8, cursor="hand2"
        ).pack(fill="x", padx=12, pady=2)

    tk.Button(sidebar_frame, text=" LOGOUT",
                  command=lambda:logout(parent),
                  bg=bg_primary, fg=bg_white,
                  relief="flat", font=("Poppins", 9),
                  anchor="w", padx=12, pady=8, cursor="hand2"
        ).pack(fill="x", padx=12, pady=10, anchor="s", side="bottom")
 
    return sidebar_frame