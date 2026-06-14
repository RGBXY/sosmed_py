import tkinter as tk
from tkinter import messagebox
from constrants import *
from logic import Auth

class RegisterFrame(tk.Frame):
    def __init__(self, parent, auth_success):
        super().__init__(parent)

        self.auth = Auth() 
        self.user = None
        self.auth_success = auth_success
        self.config(bg=bg_main)
        
        def btn_on_enter(e):
            btn_login.config(bg=bg_secondary)
            
        def btn_on_leave(e):
            btn_login.config(bg=bg_primary)
            
        def register():
            ent_username = self.ent_name.get()
            ent_password = self.ent_password.get()
            ent_confirm_password = self.ent_confirm_password.get()
            res = self.auth.register_logic(ent_username, ent_password, ent_confirm_password)
                        
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.user = res["data"]
                print(self.user.username)
                
                self.auth_success(self.user)

        def go_login():
            from gui.frames.auth.login import LoginFrame
            self.master.switch_frame(
                LoginFrame, 
                auth_success=self.master.auth_success
            )
            
        def toggle_password():
            if var_show.get() == 1:
                self.ent_password.config(show="")
                self.ent_confirm_password.config(show="")
            else:
                self.ent_password.config(show="*")
                self.ent_confirm_password.config(show="*")
                
        form_frame = tk.Frame(self, bg=bg_white)
        form_frame.pack(expand=True, ipadx=24)
            
        tk.Label(form_frame, text="Register to Hubble", font=("Poppins", 20), bg=bg_white).pack(pady=(20))
        
        tk.Label(form_frame, text="Username", font=("Poppins", 8), bg=bg_white).pack(anchor="w", padx=20)
        self.ent_name = tk.Entry(form_frame, width=45, bd=1, relief="solid")
        self.ent_name.pack(ipady=4)
        
        tk.Label(form_frame, text="Password", font=("Poppins", 8), bg=bg_white).pack(anchor="w", pady=(10, 0), padx=20)
        self.ent_password = tk.Entry(form_frame, show="*", width=45, bd=1, relief="solid")
        self.ent_password.pack(ipady=4)

        tk.Label(form_frame, text="Confirm Password", font=("Poppins", 8), bg=bg_white).pack(anchor="w", pady=(10, 0), padx=20)
        self.ent_confirm_password = tk.Entry(form_frame, show="*", width=45, bd=1, relief="solid")
        self.ent_confirm_password.pack(ipady=4)
        
        var_show = tk.IntVar() 
        chk_show = tk.Checkbutton(
            form_frame, 
            text="Show Password", 
            variable=var_show, 
            command=toggle_password,
            bg=bg_white,
            activebackground=bg_white,
            font=("Poppins", 8)
        )
        chk_show.pack(anchor="w", padx=20, pady=(5, 0))
        
        btn_login = tk.Button(form_frame, text="REGISTER", command=register, width=38, bg=bg_primary, foreground=bg_white, height=2, font=("Poppins", 9, "bold"))
        btn_login.pack(pady=(20)) # Mengurangi sedikit pady agar pas karena ada checkbutton
        btn_login.bind("<Enter>", btn_on_enter)
        btn_login.bind("<Leave>", btn_on_leave)

        btn_change_login = tk.Button(form_frame, command=go_login, text="Login", relief="flat")
        btn_change_login.pack(pady=(0, 30))