import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.components.post_form import PostForm
from gui.components.header import main_header
from gui.components.post_card import CreatePostCard
from gui.utils.navigation import render_role_sidebar
from logic import Post_Logic

class HomeFrame(tk.Frame):
    def __init__(self, parent, current_user, data_edit=None):
        super().__init__(parent)
        self.current_user = current_user
        self.post = Post_Logic()
        self.post_data_edit = None 

        if data_edit:
            self.post_data_edit = data_edit 

        # Setup Sidebar and Header
        render_role_sidebar(self, current_user, "Home")

        right_container = tk.Frame(self, bg=bg_main)
        right_container.pack(side="left", fill="both", expand=True)
        
        main_header(right_container, current_user, "Home")

        self.feed_area = tk.Frame(right_container, bg=bg_main, padx=20, pady=20)
        self.feed_area.pack(fill="both", expand=True, side="left")

        self.form_container = tk.Frame(self.feed_area, bg=bg_main)
        self.form_container.pack(fill="x", anchor="n")

        self.render_post_form()

        # Setup Scrollbar
        scroll_container = tk.Frame(self.feed_area, bg=bg_main)
        scroll_container.pack(fill="both", expand=True, pady=(15, 0))

        self.canvas = tk.Canvas(scroll_container, bg=bg_main, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.container_posts = tk.Frame(self.canvas, bg=bg_main)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container_posts, anchor="nw")

        self.has_scroll = False

        self.container_posts.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        self.load_data()

    def render_post_form(self):
        for item in self.form_container.winfo_children():
            item.destroy()
            
        PostForm(
            self.form_container, 
            self.current_user, 
            self.post_data_edit, 
            on_submit=self.handle_form_success
        )

    def update_to_edit_mode(self, post_data):
        self.post_data_edit = post_data
        self.render_post_form()
        self.canvas.yview_moveto(0)

    def handle_form_success(self):
        self.post_data_edit = None 
        self.render_post_form()
        self.load_data()         

    def load_data(self):
        for item in self.container_posts.winfo_children():
            item.destroy()
            
        post_data = self.post.get_posts_logic(self.current_user.id)
       
        for post in post_data:
            CreatePostCard(
                self.container_posts, 
                post, 
                self.current_user, 
                on_delete_callback=self.on_delete,
                edit_callback=self.update_to_edit_mode, 
                on_liked=self.load_data,
            )

    # HELPER SYSTEM SCROLLBAR 
    def on_frame_configure(self, event):
        bbox = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=bbox)
        content_height = bbox[3] - bbox[1]
        canvas_height = self.canvas.winfo_height()
        
        if content_height <= canvas_height:
            self.scrollbar.pack_forget() 
            self.has_scroll = False     
        else:
            self.scrollbar.pack(side="right", fill="y") 
            self.has_scroll = True

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_mousewheel(self, event):
        if self.canvas.winfo_exists() and getattr(self, 'has_scroll', False):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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