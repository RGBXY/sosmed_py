import tkinter as tk
from tkinter import messagebox
from constrants import *

# Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

# Logic
from logic import Notification_Logic


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class NotificationFrame(tk.Frame):
    """Frame halaman notifikasi untuk memantau info sistem dan memproses permintaan pertemanan (follow requests)."""

    def __init__(self, parent, current_user):
        """Menginisialisasi komponen backend, menyiapkan struktur layout utama, dan memicu pemuatan data notifikasi."""
        super().__init__(parent, bg=bg_main) 
        self.current_user = current_user
        
        # Setup Sidebar dan Header bawaan aplikasi kamu
        render_role_sidebar(self, current_user, "Notification")
        main_header(self, current_user, "Notifikasi")
        
        self.main_content = tk.Frame(self, bg=bg_main)
        self.main_content.pack(side="right", fill="both", expand=True)
        
        self.backend = Notification_Logic()
        
        self.create_scrollable_area()
        self.load_notifications()

    # =========================================================
    # METHOD LOGIC HANDLER
    # =========================================================

    def load_notifications(self):
        """Menarik record data notifikasi dari database dan mendistribusikan pembuatan kartu berdasarkan jenis tipenya."""
        # Bersihkan container sebelum render ulang
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        notifications_list = self.backend.get_notifications_logic(self.current_user.id)
            
        if not notifications_list:
            lbl_empty = tk.Label(
                self.scrollable_frame, 
                text="🔔 Belum ada notifikasi baru.", 
                font=("Poppins", 11, "italic"), 
                bg=bg_main, 
                fg=text_muted
            )
            lbl_empty.pack(pady=40, expand=True, fill="x")
            return

        # Loop data notifikasi untuk merender tipenya masing-masing
        for notif in notifications_list:
            if notif.type == "follow_request":
                self.render_follow_card(notif)
            else:
                self.render_system_card(notif)

    def handle_follow(self, notif_id, follows_id, action):
        """Mengeksekusi aksi penerimaan atau penolakan permintaan follow melalui business logic dan mereset UI feed."""
        res = self.backend.process_follow_action_logic(notif_id, follows_id, action)
        if res["status"] == "Success":
            messagebox.showinfo("Sukses", res["message"])
            self.load_notifications()  # Refresh UI
        else:
            messagebox.showerror("Gagal", res["message"])

    def handle_dismiss_info(self, notif_id):
        """Menghapus entri notifikasi informasi umum dari database setelah pengguna menekan tombol tutup."""
        self.backend.delete_notification(notif_id)
        self.load_notifications()  # Refresh UI

    def create_scrollable_area(self):
        """Membangun komponen view berpenghubung Canvas-Scrollbar dan mengunci sinkronisasi lebar koordinat dinamis window."""
        self.canvas = tk.Canvas(self.main_content, bg=bg_main, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_content, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_main)
        
        def update_scroll_region(event):
            content_height = self.scrollable_frame.winfo_reqheight()
            canvas_height = self.canvas.winfo_height()
            canvas_width = self.canvas.winfo_width()
            self.canvas.configure(scrollregion=(0, 0, canvas_width, content_height))
            
            if content_height <= canvas_height:
                self.scrollbar.pack_forget()
            else:
                self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame.bind("<Configure>", update_scroll_region)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind("<Configure>", on_canvas_configure)
        
        def on_mousewheel(event):
            content_height = self.scrollable_frame.winfo_reqheight()
            canvas_height = self.canvas.winfo_height()
            if content_height > canvas_height:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    def render_follow_card(self, notif):
        """Membangun boks kartu komponen interaktif khusus untuk permintaan pertemanan masuk lengkap dengan tombol aksi."""
        card = tk.Frame(self.scrollable_frame, bg=bg_white, highlightbackground=border_col, highlightthickness=1, padx=15, pady=15)
        card.pack(fill="x", pady=6, padx=10)
        
        left_frame = tk.Frame(card, bg=bg_white)
        left_frame.pack(side="left", fill="x", expand=True)
        
        avatar = tk.Frame(left_frame, bg="#1E88E5", width=35, height=35)
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)
        initial = notif.sender_username[0].upper() if notif.sender_username else "?"
        tk.Label(avatar, text=initial, fg=bg_white, bg="#1E88E5", font=("Poppins", 10, "bold")).pack(expand=True)
        
        lbl_msg = tk.Label(left_frame, text=notif.message, font=("Poppins", 10), bg=bg_white, fg=text_dark, justify="left", anchor="w")
        lbl_msg.pack(side="left", fill="x", expand=True)
        
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

    def render_system_card(self, notif):
        """Membangun boks kartu bergaya pasif berisikan informasi sistem atau siaran global dari administrator."""
        card = tk.Frame(self.scrollable_frame, bg="#F9FAFB", highlightbackground=border_col, highlightthickness=1, padx=15, pady=15)
        card.pack(fill="x", pady=6, padx=10)
        
        left_frame = tk.Frame(card, bg="#F9FAFB")
        left_frame.pack(side="left", fill="x", expand=True)
        
        avatar = tk.Frame(left_frame, bg="#E53935", width=35, height=35)
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)
        tk.Label(avatar, text="⚠️", fg=bg_white, bg="#E53935", font=("Poppins", 11)).pack(expand=True)
        
        lbl_msg = tk.Label(left_frame, text=notif.message, font=("Poppins", 10, "medium"), bg="#F9FAFB", fg=text_dark, justify="left", anchor="w", wraplength=400)
        lbl_msg.pack(side="left", fill="x", expand=True)
        
        btn_dismiss = tk.Button(
            card, text="✕", font=("Poppins", 10), bg="#F9FAFB", fg=text_muted,
            relief="flat", cursor="hand2", activebackground="#F9FAFB",
            command=lambda nid=notif.id: self.handle_dismiss_info(nid)
        )
        btn_dismiss.pack(side="right", padx=5)