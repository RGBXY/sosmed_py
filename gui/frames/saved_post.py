import tkinter as tk
from tkinter import messagebox
from constrants import *
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header
from gui.components.post_card import CreatePostCard  
from logic import Saved_Post_Logic  

class SavedPostFrame(tk.Frame):
    def __init__(self, parent, current_user):
        super().__init__(parent, bg=bg_white) 
        self.current_user = current_user
        
        # Setup Sidebar and Header
        render_role_sidebar(self, current_user, "Saved_Post")
        main_header(self, current_user, "Saved Post")
        
        self.main_content = tk.Frame(self, bg=bg_white)
        self.main_content.pack(side="right", fill="both", expand=True)
        
        self.create_scrollable_area()
        
        self.load_saved_posts()

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

    def load_saved_posts(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        try:
            saved_backend = Saved_Post_Logic()
            saved_posts_list = saved_backend.get_saved_posts_logic(self.current_user.id)
        except Exception as e:
            print(f"Error saat mengambil data saved posts: {e}")
            saved_posts_list = []
            
        if not saved_posts_list:
            lbl_empty = tk.Label(
                self.scrollable_frame, 
                text="🗂️ Belum ada postingan yang disimpan.", 
                font=("Poppins", 11, "italic"), 
                bg=bg_white, 
                fg=text_muted
            )
            lbl_empty.pack(pady=40, expand=True)
            return

        for post in saved_posts_list:
            setattr(post, 'is_saved_by_me', True)
            
            CreatePostCard(
                parent=self.scrollable_frame,
                post_data=post,
                current_user=self.current_user,
                on_delete_callback=self.handle_delete_post,
                edit_callback=self.handle_edit_post,
                on_liked=self.handle_refresh_likes,
            )
            
    def handle_delete_post(self, post_id):
        if messagebox.askyesno("Konfirmasi", "Hapus postingan ini secara permanen?"):
            from logic import Post_Logic
            post_backend = Post_Logic()
            res = post_backend.delete_post_logic(post_id)
            
            if res.get("status") == "Success":
                messagebox.showinfo("Sukses", res.get("message")[1])
                self.load_saved_posts()  
            else:
                messagebox.showerror("Gagal", res.get("message")[1])
            
    def handle_edit_post(self, post_data):
        from gui.frames.home import HomeFrame
        self.master.switch_frame(HomeFrame, data_edit=post_data, current_user=self.current_user)
        
    def handle_refresh_likes(self):
        self.load_saved_posts()