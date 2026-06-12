import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from logic import Notification_Logic  # Import logic baru kita

class NotificationFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white) 
        self.current_user = current_user
        
        # Setup Sidebar dan Header bawaan aplikasi kamu
        render_role_sidebar(self, current_user, "Notification")
        main_header(self, current_user, "Notifikasi")
        
        self.main_content = tk.Frame(self, bg=bg_white)
        self.main_content.pack(side="right", fill="both", expand=True)
        
        self.backend = Notification_Logic()
        
        self.create_scrollable_area()
        self.load_notifications()

    def create_scrollable_area(self):
        self.canvas = tk.Canvas(self.main_content, bg=bg_white, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_content, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_white)
        
        def update_scroll_region(event):
            content_height = self.scrollable_frame.winfo_reqheight()
            canvas_height = self.canvas.winfo_height()
            self.canvas.configure(scrollregion=(0, 0, 650, content_height))
            
            if content_height <= canvas_height:
                self.scrollbar.pack_forget()
            else:
                self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Configure>", update_scroll_region)
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=650) 
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        def on_mousewheel(event):
            content_height = self.scrollable_frame.winfo_reqheight()
            canvas_height = self.canvas.winfo_height()
            if content_height > canvas_height:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def load_notifications(self):
        # Bersihkan container sebelum render ulang
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        notifications_list = self.backend.get_notifications_logic(self.current_user.id)
            
        if not notifications_list:
            lbl_empty = tk.Label(
                self.scrollable_frame, 
                text="🔔 Belum ada notifikasi baru.", 
                font=("Poppins", 11, "italic"), 
                bg=bg_white, 
                fg=text_muted
            )
            lbl_empty.pack(pady=40, expand=True)
            return

        # Loop data notifikasi untuk merender tipenya masing-masing
        for notif in notifications_list:
            if notif.type == "follow_request":
                self.render_follow_card(notif)
            else:
                self.render_system_card(notif)

    # =========================================================
    # TYPE CARD 1: FOLLOW REQUEST CARD (Ada Tombol Terima/Tolak)
    # =========================================================
    def render_follow_card(self, notif):
        card = tk.Frame(self.scrollable_frame, bg=bg_white, highlightbackground=border_col, highlightthickness=1, padx=15, pady=15)
        card.pack(fill="x", pady=6, padx=10)
        
        # Sektor Kiri (Avatar & Pesan)
        left_frame = tk.Frame(card, bg=bg_white)
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Mini Avatar Bulat/Kotak berdasar huruf depan pengirim
        avatar = tk.Frame(left_frame, bg="#1E88E5", width=35, height=35)
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)
        initial = notif.sender_username[0].upper() if notif.sender_username else "?"
        tk.Label(avatar, text=initial, fg=bg_white, bg="#1E88E5", font=("Poppins", 10, "bold")).pack(expand=True)
        
        lbl_msg = tk.Label(left_frame, text=notif.message, font=("Poppins", 10), bg=bg_white, fg=text_dark, justify="left", anchor="w")
        lbl_msg.pack(side="left", fill="x", expand=True)
        
        # Sektor Kanan (Tombol Aksi)
        right_frame = tk.Frame(card, bg=bg_white)
        right_frame.pack(side="right")
        
        btn_accept = tk.Button(
            right_frame, text="Terima", font=("Poppins", 9, "bold"), bg=bg_primary, fg=bg_white,
            relief="flat", cursor="hand2", padx=10,
            command=lambda nid=notif.id, fid=notif.related_id: self.handle_follow(nid, fid, "accept")
        )
        btn_accept.pack(side="left", padx=5)
        
        btn_reject = tk.Button(
            right_frame, text="Tolak", font=("Poppins", 9, "bold"), bg="#F3F4F6", fg="#FF4D4D",
            relief="flat", cursor="hand2", padx=10,
            command=lambda nid=notif.id, fid=notif.related_id: self.handle_follow(nid, fid, "reject")
        )
        btn_reject.pack(side="left", padx=5)

    # =========================================================
    # TYPE CARD 2: SYSTEM INFO CARD (Pemberitahuan Umum/Admin)
    # =========================================================
    def render_system_card(self, notif):
        card = tk.Frame(self.scrollable_frame, bg="#F9FAFB", highlightbackground=border_col, highlightthickness=1, padx=15, pady=15)
        card.pack(fill="x", pady=6, padx=10)
        
        left_frame = tk.Frame(card, bg="#F9FAFB")
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Icon/Avatar khusus info umum (Misal tanda seru/toa merah)
        avatar = tk.Frame(left_frame, bg="#E53935", width=35, height=35)
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)
        tk.Label(avatar, text="⚠️", fg=bg_white, bg="#E53935", font=("Poppins", 11)).pack(expand=True)
        
        # Teks Info
        lbl_msg = tk.Label(left_frame, text=notif.message, font=("Poppins", 10, "medium"), bg="#F9FAFB", fg=text_dark, justify="left", anchor="w", wraplength=400)
        lbl_msg.pack(side="left", fill="x", expand=True)
        
        # Tombol hapus/bersihkan notifikasi setelah dibaca
        btn_dismiss = tk.Button(
            card, text="✕", font=("Poppins", 10), bg="#F9FAFB", fg=text_muted,
            relief="flat", cursor="hand2", activebackground="#F9FAFB",
            command=lambda nid=notif.id: self.handle_dismiss_info(nid)
        )
        btn_dismiss.pack(side="right", padx=5)

    # =========================================================
    # CALLBACK HANDLER METHODS
    # =========================================================
    def handle_follow(self, notif_id, follows_id, action):
        res = self.backend.process_follow_action_logic(notif_id, follows_id, action)
        if res["status"] == "Success":
            messagebox.showinfo("Sukses", res["message"])
            self.load_notifications() # Refresh UI
        else:
            messagebox.showerror("Gagal", res["message"])

    def handle_dismiss_info(self, notif_id):
        self.backend.delete_notification(notif_id)
        self.load_notifications() # Refresh UI