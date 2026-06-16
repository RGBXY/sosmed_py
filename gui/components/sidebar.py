import tkinter as tk
from tkinter import messagebox
from constrants import *


# ============================================================
# SECTION: GUI COMPONENTS & FACTORIES
# ============================================================
def logout(parent):
    """Menampilkan konfirmasi pop-up sebelum menutup session dan keluar."""
    check = messagebox.askyesno("Keluar", "Apakah yakin ingin keluar?")
    if check:
        parent.master.logout()


def sidebar(parent, current_user, nav_items):
    """Membuat komponen sidebar navigasi menu utama beserta profil user."""
    sidebar_frame = tk.Frame(
        parent, width=280, bg=bg_white,  
        highlightbackground=border_col, highlightthickness=1, bd=0
    )
    sidebar_frame.pack(side="left", fill="y")
    sidebar_frame.pack_propagate(False)

    # Area Banner Profil User
    nav_header_frame = tk.Frame(sidebar_frame, bg=bg_white)
    nav_header_frame.pack(fill="x", padx=24, pady=(20, 10))
 
    # Mini Avatar Grafis
    avatar_mini = tk.Frame(nav_header_frame, bg=bg_main, width=36, height=36)
    avatar_mini.pack(side="left", anchor="n")
    avatar_mini.pack_propagate(False)
    
    initial_letter = current_user.username[0].upper() if current_user.username else "?"
    tk.Label(avatar_mini, text=initial_letter, fg=text_dark, bg=bg_main, font=("Poppins", 10, "bold")).pack(expand=True)

    # Data Detail Teks Profil
    user_info = tk.Frame(nav_header_frame, bg=bg_white)
    user_info.pack(side="left", fill="x", expand=True, padx=10)

    tk.Label(
        user_info, text=current_user.username.capitalize(),
        bg=bg_white, fg=text_dark, font=("Poppins", 10, "bold")
    ).pack(anchor="w")
    
    tk.Label(
        user_info, text=f"@{current_user.role.lower()}",  
        bg=bg_white, fg=text_muted, font=("Poppins", 8)
    ).pack(anchor="w", pady=(1, 0))
 
    # Garis Pembatas
    tk.Frame(sidebar_frame, height=1, bg=border_col).pack(fill="x", padx=24, pady=(10, 15))
    
    # Render Iterasi Menu Navigasi
    def make_hover(btn, is_active):
        """Mengatur perubahan warna background tombol menu saat disorot mouse."""
        if is_active:
            btn.bind("<Enter>", lambda e: btn.config(bg=dark))
            btn.bind("<Leave>", lambda e: btn.config(bg=text_dark))
        else:
            btn.bind("<Enter>", lambda e: btn.config(bg=bg_main))
            btn.bind("<Leave>", lambda e: btn.config(bg=bg_white))

    for i in nav_items:
        is_active = i.get("active", False)
        
        btn_menu = tk.Button(
            sidebar_frame, text=f"  {i['title']}",
            command=i["command"],
            bg=text_dark if is_active else bg_white,
            fg=bg_white if is_active else text_dark,
            activebackground=dark if is_active else bg_main,
            activeforeground=bg_white if is_active else text_dark,
            relief="flat", bd=0, font=("Poppins", 10, "bold" if is_active else "normal"),
            anchor="w", padx=16, cursor="hand2"
        )
        btn_menu.pack(fill="x", padx=16, pady=4, ipady=8)  
        make_hover(btn_menu, is_active)

    # Elemen Tombol Keluar / Logout
    btn_logout = tk.Button(
        sidebar_frame, text="  Keluar",
        command=lambda: logout(parent),
        bg=bg_white, fg="#E63946",  
        activebackground="#FAD2E1", activeforeground="#E63946",
        relief="flat", bd=0, font=("Poppins", 10, "bold"),
        anchor="w", padx=16, cursor="hand2"
    )
    btn_logout.pack(fill="x", padx=16, pady=24, ipady=8, side="bottom")
    
    btn_logout.bind("<Enter>", lambda e: btn_logout.config(bg="#FFE5EC"))
    btn_logout.bind("<Leave>", lambda e: btn_logout.config(bg=bg_white))
 
    return sidebar_frame