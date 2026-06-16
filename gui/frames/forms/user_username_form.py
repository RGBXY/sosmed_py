import tkinter as tk
from tkinter import messagebox, ttk
from constrants import *
from logic import User_Profile


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class FormUserUsernamePopup(tk.Toplevel):
    """Jendela popup modal untuk memfasilitasi pembaruan nama pengguna (username) baru."""

    def __init__(self, parent, current_user, on_success_callback):
        """Menginisialisasi konfigurasi window modal, pengetengahan posisi, layout form, dan event bindings."""
        super().__init__(parent)
        self.current_user = current_user
        self.change_user_profile = User_Profile()
        self.on_success_callback = on_success_callback 
        
        # Konfigurasi Window Popup
        self.title("Pengaturan Akun")
        self.config(bg=bg_white)
        self.resizable(False, False)
        
        # Membuat popup bersifat MODAL
        self.grab_set()
        
        # Ketengahkan Posisi Popup terhadap Window Induk
        self.geometry("540x360")
        self.update_idletasks()
        parent_x = parent.winfo_toplevel().winfo_x()
        parent_y = parent.winfo_toplevel().winfo_y()
        parent_w = parent.winfo_toplevel().winfo_width()
        parent_h = parent.winfo_toplevel().winfo_height()
        x = parent_x + (parent_w // 2) - (540 // 2)
        y = parent_y + (parent_h // 2) - (360 // 2)
        self.geometry(f"+{x}+{y}")

        # --- UI LAYOUT CONTAINER ---
        profile_card = tk.Frame(self, bg=bg_white, padx=35, pady=35)
        profile_card.pack(fill="both", expand=True)
        
        # Judul Form
        tk.Label(
            profile_card, 
            text="Pengaturan Akun", 
            font=("Poppins", 15, "bold"), 
            bg=bg_white, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 4))

        # Deskripsi Bantuan
        tk.Label(
            profile_card, 
            text="Perbarui informasi profil Anda untuk menjaga kredensial akun tetap segar.", 
            font=("Poppins", 9), 
            bg=bg_white, 
            fg=text_muted,
            wraplength=460,
            justify="left"
        ).pack(anchor="w", pady=(0, 25))
        
        # Input Field: Username Baru
        tk.Label(
            profile_card, 
            text="Username Baru", 
            font=("Poppins", 9, "bold"), 
            bg=bg_white, 
            fg=text_dark
        ).pack(anchor="w", pady=(0, 8))
        
        self.entry_border = tk.Frame(profile_card, bg=border_col, padx=1, pady=1)
        self.entry_border.pack(anchor="w", fill="x", pady=(0, 25))
        
        entry_padding_bg = tk.Frame(self.entry_border, bg=bg_white, padx=14, pady=8)
        entry_padding_bg.pack(fill="both", expand=True)
        
        lbl_icon = tk.Label(entry_padding_bg, text="👤", font=("Poppins", 10), bg=bg_white, fg=text_muted)
        lbl_icon.pack(side="left", padx=(0, 8))

        self.ent_new_username = tk.Entry(
            entry_padding_bg, 
            font=("Poppins", 10), 
            bg=bg_white, 
            fg=text_dark,
            bd=0,
            insertbackground=text_dark
        )
        self.ent_new_username.pack(side="left", fill="both", expand=True)
        self.ent_new_username.insert(0, self.current_user.username) 

        # Focus Bindings
        self.ent_new_username.bind("<FocusIn>", self.entry_on_focus_in)
        self.ent_new_username.bind("<FocusOut>", self.entry_on_focus_out)

        # Separator Line
        tk.Frame(profile_card, height=1, bg=border_col).pack(fill="x", pady=(0, 20))
        
        # Button Actions Container
        btn_container = tk.Frame(profile_card, bg=bg_white)
        btn_container.pack(anchor="w", fill="x")

        # Tombol Submit
        self.btn_submit = tk.Button(
            btn_container, 
            text="💾 Simpan", 
            command=self.change_username,
            bg=dark, 
            fg=bg_white, 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_submit.pack(side="left")
        
        # Tombol Batal
        self.btn_back = tk.Button(
            btn_container, 
            text="Batal", 
            command=self.destroy, 
            bg="#F3F4F6", 
            fg="#4B5563", 
            font=("Poppins", 9, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.btn_back.pack(side="left", padx=(12, 0))

        # Event Hover Bindings
        self.btn_submit.bind("<Enter>", self.btn_submit_on_enter)
        self.btn_submit.bind("<Leave>", self.btn_submit_on_leave)
        self.btn_back.bind("<Enter>", self.btn_back_on_enter)
        self.btn_back.bind("<Leave>", self.btn_back_on_leave)

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================
    def entry_on_focus_in(self, e):
        """Mengubah warna border input menjadi gelap saat kolom teks mulai difokuskan."""
        self.entry_border.config(bg=dark)

    def entry_on_focus_out(self, e):
        """Mengembalikan warna asli border input saat fokus meninggalkan kolom teks."""
        self.entry_border.config(bg=text_dark)

    def btn_submit_on_enter(self, e):
        """Mengubah warna latar tombol simpan saat disorot kursor mouse."""
        self.btn_submit.config(bg=bg_secondary)

    def btn_submit_on_leave(self, e):
        """Mengembalikan warna latar tombol simpan saat kursor mouse keluar."""
        self.btn_submit.config(bg=dark)

    def btn_back_on_enter(self, e):
        """Mengubah warna latar tombol batal saat disorot kursor mouse."""
        self.btn_back.config(bg="#E5E7EB", fg=text_dark)

    def btn_back_on_leave(self, e):
        """Mengembalikan warna latar tombol batal saat kursor mouse keluar."""
        self.btn_back.config(bg="#F3F4F6", fg="#4B5563")

    def change_username(self):
        """Memvalidasi input nama baru dan mengirimkan request pembaruan profile ke backend."""
        current_username = self.current_user.username
        new_username = self.ent_new_username.get().strip()

        if not new_username:
            messagebox.showwarning("Input Kosong", "Username baru tidak boleh kosong!")
            return
        
        res = self.change_user_profile.change_username_logic(current_username, new_username)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.on_success_callback(res["data"]) 
            self.destroy() 

