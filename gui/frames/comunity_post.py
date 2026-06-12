import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from gui.components.post_card import CreatePostCard
from logic import Comunity_Logic 

class ComunityPostFrame(tk.Frame):
    def __init__(self, parent, current_user, comunity_id):
        super().__init__(parent, bg=bg_white)
        self.comunities = Comunity_Logic()
        self.current_user = current_user
        self.selected_community_id = None 
        self.comunity_id = comunity_id

        # Setup Sidebar Main Header
        render_role_sidebar(self, current_user, "Comunity Post")
        main_header(self, current_user, "Komunitas Post")

        # Main Container
        self.main_content = tk.Frame(self, bg=bg_main)
        self.main_content.pack(side="right", fill="both", expand=True)

        tk.Frame(self.main_content, height=2, bg=border_col).pack(fill="x", padx=20, pady=10)

        self.render_scrollable_area()
        
        self.refresh_page_data()

    def render_scrollable_area(self):
        scroll_container = tk.Frame(self.main_content, bg=bg_main)
        scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.canvas = tk.Canvas(scroll_container, bg=bg_main, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Card Container
        self.card_container = tk.Frame(self.canvas, bg=bg_main)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.card_container, anchor="nw")

        # Scroll Event
        self.card_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.canvas_window, width=event.width))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") if self.canvas.winfo_exists() else None)

    def load_cards(self, data):
        for widget in self.card_container.winfo_children():
            widget.destroy()

        if not data:
            tk.Label(
                self.card_container, text="📭 Belum ada komunitas yang dibuat.",
                font=("Poppins", 10, "italic"), bg=bg_main, fg=text_muted
            ).pack(pady=30)
            return

        # Card 
        for post in data:
            CreatePostCard(
                parent=self.card_container,
                post_data=post,
                current_user=self.current_user,
                on_delete_callback=self.on_delete,
                edit_callback=self.handle_edit_post,
                on_liked=self.handle_refresh_likes
            )

    # Update Logic
    def refresh_page_data(self):
        comunity_id = self.comunity_id
        current_user_id = self.current_user.id

        data = self.comunities.get_comunity_post_logic(comunity_id, current_user_id)
        self.load_cards(data)

    def handle_edit_post(self, post_data):
        from gui.frames.home import HomeFrame
        self.master.switch_frame(HomeFrame, data_edit=post_data, current_user=self.current_user)

    def on_delete(self, id):
        res_user = messagebox.askyesno("Delete Post", "Yakin anda ingin menghapus data?")
        if res_user:
            res = self.post.delete_post_logic(id)
            if res["status"] == "Error":
                messagebox.showerror(res["message"][0], res["message"][1])
                return
            if res["status"] == "Success":
                messagebox.showinfo(res["message"][0], res["message"][1])
                self.handle_form_success() 

    def handle_refresh_likes(self):
        comunity_id = self.comunity_id
        current_user_id = self.current_user.id

        data = self.comunities.get_comunity_post_logic(comunity_id, current_user_id)

        self.load_cards(data)