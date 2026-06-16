import tkinter as tk
from tkinter import messagebox
from constrants import *
from logic import User_Profile


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class FormUserPasswordPopup(tk.Toplevel):
    """Jendela popup modal untuk memfasilitasi pembaruan password mandiri oleh pengguna."""

    def __init__(self, parent, current_user, on_success_callback):
        """Menginisialisasi konfigurasi window modal, pengetengahan posisi, layout form, dan event bindings."""
        super().__init__(parent)
        self.current_user = current_user
        self.change_user_profile = User_Profile()
        self.on_success_callback = on_success_callback  
        
        # Konfigurasi Window Popup
        self.title("Ubah Password")
        self.config(bg=bg_white)
        self.resizable(False, False)
        
        # Membuat popup bersifat MODAL
        self.grab_set()
        
        # Ketengahkan Posisi Popup terhadap Window Induk
        self.geometry("540x450")  
        self.update_idletasks()
        parent_x = parent.winfo_toplevel().winfo_x()
        parent_y = parent.winfo_toplevel().winfo_y()
        parent_w = parent.winfo_toplevel().winfo_width()
        parent_h = parent.winfo_toplevel().winfo_height()
        x = parent_x + (parent_w // 2) - (540 // 2)
        y = parent_y + (parent_h // 2) - (450 // 2)
        self.geometry(f"+{x}+{y}")

        # State Tracker untuk Checkbutton Show Password
        self.var_show = tk.IntVar() 

        # --- UI LAYOUT CONTAINER ---
        profile_card = tk.Frame(self, bg=bg_white, padx=35, pady=35)
        profile_card.pack(fill="both", expand=True)
        
        # Judul Form
        tk.Label(
            profile_card, text="Ubah Password Akun", 
            font=("Poppins", 15, "bold"), bg=bg_white, fg=text_dark
        ).pack(anchor="w", pady=(0, 4))

        # Deskripsi Bantuan
        tk.Label(
            profile_card, text="Masukkan password lama Anda untuk verifikasi, kemudian ketik password baru Anda.", 
            font=("Poppins", 9), bg=bg_white, fg=text_muted, wraplength=460, justify="left"
        ).pack(anchor="w", pady=(0, 20))
        
        # Input Field 1: Password Lama
        tk.Label(
            profile_card, text="Password Lama Saat Ini", 
            font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark
        ).pack(anchor="w", pady=(0, 6))
        
        self.border_old_pass = tk.Frame(profile_card, bg=border_col, padx=1, pady=1)
        self.border_old_pass.pack(anchor="w", fill="x", pady=(0, 15))
        
        pad_old = tk.Frame(self.border_old_pass, bg=bg_white, padx=14, pady=8)
        pad_old.pack(fill="both", expand=True)
        
        tk.Label(pad_old, text="🔒", font=("Poppins", 10), bg=bg_white, fg=text_muted).pack(side="left", padx=(0, 8))

        self.ent_old_password = tk.Entry(
            pad_old, font=("Poppins", 10), bg=bg_white, fg=text_dark, bd=0, insertbackground=text_dark
        )
        self.ent_old_password.insert(0, "Password Lama")
        self.ent_old_password.pack(fill="x", expand=True)

        # Input Field 2: Password Baru
        tk.Label(
            profile_card, text="Password Baru", 
            font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark
        ).pack(anchor="w", pady=(0, 6))
        
        self.border_new_pass = tk.Frame(profile_card, bg=border_col, padx=1, pady=1)
        self.border_new_pass.pack(anchor="w", fill="x", pady=(0, 15))
        
        pad_new = tk.Frame(self.border_new_pass, bg=bg_white, padx=14, pady=8)
        pad_new.pack(fill="both", expand=True)
        
        tk.Label(pad_new, text="🔑", font=("Poppins", 10), bg=bg_white, fg=text_muted).pack(side="left", padx=(0, 8))

        self.ent_new_password = tk.Entry(
            pad_new, font=("Poppins", 10), bg=bg_white, fg=text_dark, bd=0, insertbackground=text_dark
        )
        self.ent_new_password.insert(0, "Password Baru")
        self.ent_new_password.pack(fill="x", expand=True)

        # Focus Bindings
        self.ent_old_password.bind("<FocusIn>", self.old_focus_in)
        self.ent_old_password.bind("<FocusOut>", self.old_focus_out)
        self.ent_new_password.bind("<FocusIn>", self.new_focus_in)
        self.ent_new_password.bind("<FocusOut>", self.new_focus_out)

        # Show Password Checkbutton
        chk_show = tk.Checkbutton(
            profile_card, text="Show password", variable=self.var_show, command=self.toggle_password,
            bg=bg_white, activebackground=bg_white, fg=text_muted, activeforeground=text_dark,
            font=("Poppins", 8), bd=0, cursor="hand2"
        )
        chk_show.pack(anchor="w", padx=2, pady=(0, 15))

        # Separator Line
        tk.Frame(profile_card, height=1, bg=border_col).pack(fill="x", pady=(0, 20))
        
        # Button Actions Container
        btn_container = tk.Frame(profile_card, bg=bg_white)
        btn_container.pack(anchor="w", fill="x")

        # Tombol Submit
        self.btn_submit = tk.Button(
            btn_container, text="🔒 Perbarui Password", command=self.change_password,
            bg=dark, fg=bg_white, font=("Poppins", 9, "bold"), relief="flat", padx=20, pady=10, cursor="hand2"
        )
        self.btn_submit.pack(side="left")
        
        # Tombol Batal
        self.btn_back = tk.Button(
            btn_container, text="Batal", command=self.destroy,
            bg="#F3F4F6", fg="#4B5563", font=("Poppins", 9, "bold"), relief="flat", padx=20, pady=10, cursor="hand2"
        )
        self.btn_back.pack(side="left", padx=(12, 0))

        # Event Hover Bindings
        self.btn_submit.bind("<Enter>", lambda e: self.btn_submit.config(bg=bg_secondary))
        self.btn_submit.bind("<Leave>", lambda e: self.btn_submit.config(bg=dark))
        self.btn_back.bind("<Enter>", lambda e: self.btn_back.config(bg="#E5E7EB", fg=text_dark))
        self.btn_back.bind("<Leave>", lambda e: self.btn_back.config(bg="#F3F4F6", fg="#4B5563"))

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================

    def toggle_password(self):
        """Menyembunyikan atau menampilkan teks karakter pada kedua field input berdasarkan state checkbutton."""
        if self.var_show.get() == 1:
            self.ent_old_password.config(show="")
            self.ent_new_password.config(show="")
        else:
            if self.ent_old_password.get() != "Password Lama":
                self.ent_old_password.config(show="*")
            if self.ent_new_password.get() != "Password Baru":
                self.ent_new_password.config(show="*")

    def old_focus_in(self, e):
        """Menghapus placeholder password lama dan menyalakan masking bintang saat mendapatkan fokus."""
        self.border_old_pass.config(bg=dark)
        if self.ent_old_password.get() == "Password Lama":
            self.ent_old_password.delete(0, 'end')
            if self.var_show.get() == 0:
                self.ent_old_password.config(show="*")

    def old_focus_out(self, e):
        """Mengembalikan placeholder password lama dan mematikan masking jika ditinggalkan kosong."""
        self.border_old_pass.config(bg=border_col)
        if self.ent_old_password.get() == "":
            self.ent_old_password.config(show="")
            self.ent_old_password.insert(0, "Password Lama")

    def new_focus_in(self, e):
        """Menghapus placeholder password baru dan menyalakan masking bintang saat mendapatkan fokus."""
        self.border_new_pass.config(bg=dark)
        if self.ent_new_password.get() == "Password Baru":
            self.ent_new_password.delete(0, 'end')
            if self.var_show.get() == 0:
                self.ent_new_password.config(show="*")

    def new_focus_out(self, e):
        """Mengembalikan placeholder password baru dan mematikan masking jika ditinggalkan kosong."""
        self.border_new_pass.config(bg=border_col)
        if self.ent_new_password.get() == "":
            self.ent_new_password.config(show="")
            self.ent_new_password.insert(0, "Password Baru")

    def change_password(self):
        """Memvalidasi keabsahan data form dan mengirimkan permintaan modifikasi password ke backend."""
        user_id = self.current_user.id
        old_password = self.ent_old_password.get().strip()
        new_password = self.ent_new_password.get().strip()

        if old_password == "Password Lama": old_password = ""
        if new_password == "Password Baru": new_password = ""

        if not old_password or not new_password:
            messagebox.showwarning("Input Kosong", "Semua kolom password wajib diisi!")
            return
            
        res = self.change_user_profile.change_password_logic(user_id, old_password, new_password)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            if self.on_success_callback:
                self.on_success_callback(self.current_user) 
            self.destroy()
