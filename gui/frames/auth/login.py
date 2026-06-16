import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
from constrants import *
from logic import Auth


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class LoginFrame(tk.Frame):
    """Frame panel autentikasi masuk (login) ke dalam sistem."""

    def __init__(self, parent, auth_success):
        """Menginisialisasi layout komponen kartu login, field input placeholder, dan tombol aksi."""
        super().__init__(parent)   
        self.auth = Auth() 
        self.user = None
        self.auth_success = auth_success
        self.config(bg=bg_main)
        
        # Mengunci ukuran card wrapper utama (380x500) agar stabil
        card_frame = tk.Frame(self, bg=bg_white, highlightbackground=border_col, highlightthickness=1, bd=0, width=380, height=500)
        card_frame.pack_propagate(False) 
        card_frame.pack(expand=True)
            
        # Kontainer internal untuk menyelaraskan lebar seluruh widget di dalam
        form_frame = tk.Frame(card_frame, bg=bg_white, width=320)
        form_frame.pack_propagate(False)
        form_frame.pack(expand=True, fill="both", padx=30, pady=20)

        # 1. Top Logo Icon Box
        logo_box = tk.Frame(form_frame, bg=bg_white, highlightbackground=border_col, highlightthickness=1, bd=0, width=48, height=48)
        logo_box.pack_propagate(False)
        logo_box.pack(pady=(10, 15))
        
        try:
            raw_logo = Image.open("./image/logo.png")
            resized_logo = raw_logo.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(resized_logo)
            
            lbl_logo_img = tk.Label(logo_box, image=self.logo_img, bg=bg_white)
            lbl_logo_img.pack(expand=True)
            
        except Exception as e:
            print(f"Gagal memuat gambar logo, beralih ke teks: {e}")
            tk.Label(logo_box, text="✦", font=("Poppins", 16), fg=bg_primary, bg=bg_white).pack(expand=True)

        # 2. Title & Subtitle
        tk.Label(form_frame, text="Selamat datang kembali!", font=("Poppins", 16, "bold"), bg=bg_white, fg=text_dark).pack()
        desc_text = "Masuk untuk melihat apa yang baru\ndan tetap terhubung dengan lingkaranmu."
        tk.Label(form_frame, text=desc_text, font=("Poppins", 8), bg=bg_white, fg=text_muted, justify="center").pack(pady=(5, 20))

        # 3. Input Username
        f_name = tk.Frame(form_frame, bg=bg_main, highlightbackground=border_col, highlightthickness=1, bd=0)
        f_name.pack(fill="x", pady=6)
        
        self.ent_name = tk.Entry(
            f_name, bd=0, bg=bg_main, font=("Poppins", 10), 
            fg=text_dark, insertbackground=text_dark
        )
        self.ent_name.insert(0, "Username")
        self.ent_name.pack(fill="x", padx=10, ipady=8) 

        self.ent_name.bind("<FocusIn>", self._name_on_focus_in)
        self.ent_name.bind("<FocusOut>", self._name_on_focus_out)

        # 4. Input Password
        f_password = tk.Frame(form_frame, bg=bg_main, highlightbackground=border_col, highlightthickness=1, bd=0)
        f_password.pack(fill="x", pady=6)

        self.ent_password = tk.Entry(
            f_password, bd=0, bg=bg_main, font=("Poppins", 10), 
            fg=text_dark, insertbackground=text_dark
        )
        self.ent_password.insert(0, "Password")
        self.ent_password.pack(fill="x", padx=10, ipady=8)       

        self.ent_password.bind("<FocusIn>", self._pw_on_focus_in)
        self.ent_password.bind("<FocusOut>", self._pw_on_focus_out)

        # 5. Show Password Checkbutton
        self.var_show = tk.IntVar() 
        chk_show = tk.Checkbutton(
            form_frame, text="Show password", variable=self.var_show, command=self._toggle_password,
            bg=bg_white, activebackground=bg_white, fg=text_muted, activeforeground=text_dark,
            font=("Poppins", 8), bd=0, cursor="hand2"
        )
        chk_show.pack(anchor="w", padx=2, pady=(2, 15))
        
        # 6. Tombol Login Utama
        self.btn_login = tk.Button(
            form_frame, text="Masuk", command=self._login,
            bg=text_dark, foreground=bg_white, bd=0, relief="flat",
            activebackground="#2D3142", activeforeground=bg_white, font=("Poppins", 10, "bold")
        )
        self.btn_login.pack(fill="x", ipady=8, pady=(15))
        self.btn_login.bind("<Enter>", self._btn_on_enter)
        self.btn_login.bind("<Leave>", self._btn_on_leave)

        # 7. Footer Pindah Halaman
        footer_frame = tk.Frame(form_frame, bg=bg_white)
        footer_frame.pack(pady=(10, 0))
        tk.Label(footer_frame, text="Belum punya akun?", font=("Poppins", 8), bg=bg_white, fg=text_muted).pack(side="left")
        
        btn_change_register = tk.Button(
            footer_frame, command=self._go_register, text="Daftar", relief="flat", bd=0,
            bg=bg_white, fg=bg_primary, activebackground=bg_white, activeforeground=bg_secondary,
            font=("Poppins", 8, "bold"), cursor="hand2"
        )
        btn_change_register.pack(side="left", padx=(4, 0))

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================
    def _btn_on_enter(self, e):
        """Mengubah warna latar tombol login saat disorot kursor mouse."""
        self.btn_login.config(bg=dark, cursor="hand2")
            
    def _btn_on_leave(self, e):
        """Mengembalikan warna latar tombol login saat kursor mouse keluar."""
        self.btn_login.config(bg=text_dark)
            
    def _name_on_focus_in(self, e):
        """Menghapus teks placeholder username saat field mulai dimasuki fokus input."""
        if self.ent_name.get() == "Username":
            self.ent_name.delete(0, 'end')

    def _name_on_focus_out(self, e):
        """Mengembalikan teks placeholder username jika field ditinggalkan dalam keadaan kosong."""
        if self.ent_name.get() == "":
            self.ent_name.insert(0, "Username")

    def _pw_on_focus_in(self, e):
        """Menghapus placeholder password dan mengaktifkan karakter masking bintang (*)."""
        if self.ent_password.get() == "Password":
            self.ent_password.delete(0, 'end')
            self.ent_password.config(show="*")

    def _pw_on_focus_out(self, e):
        """Mengembalikan placeholder password dan menonaktifkan masking jika field kosong."""
        if self.ent_password.get() == "":
            self.ent_password.config(show="")
            self.ent_password.insert(0, "Password")

    def _login(self):
        """Memvalidasi input kredensial pengguna dan memicu request verifikasi login ke backend."""
        ent_username = self.ent_name.get()
        ent_password = self.ent_password.get()

        if ent_username == "Username":
            ent_username = ""
                
        if ent_password == "Password":
            ent_password = ""

        res = self.auth.login_logic(ent_username, ent_password)
                        
        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
            
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            self.user = res["data"]
            self.auth_success(self.user)

    def _go_register(self):
        """Mengalihkan tampilan frame jendela utama menuju halaman pendaftaran (register)."""
        from gui.frames.auth.register import RegisterFrame
        self.master.switch_frame(
            RegisterFrame, 
            auth_success=self.master.auth_success
        )
            
    def _toggle_password(self):
        """Menyembunyikan atau menampilkan karakter password asli berdasarkan state checkbutton."""
        if self.var_show.get() == 1:
            self.ent_password.config(show="")
        else:
            if self.ent_password.get() != "Password":
                self.ent_password.config(show="*")

