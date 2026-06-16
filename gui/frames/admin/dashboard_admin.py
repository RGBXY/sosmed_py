import csv  
import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog  
from constrants import * # Components
from gui.utils.navigation import render_role_sidebar
from gui.components.header import main_header

# Import backend logic
from logic import (
    get_dashboard_metrics, 
    get_user_activity_summary,
    export_metrics_to_csv,
    User_Profile 
)


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class DashboardAdminFrame(tk.Frame):
    """Frame utama halaman dashboard administrator untuk memantau metrik dan aktivitas pengguna."""

    def __init__(self, parent, current_user):
        """Menginisialisasi komponen sidebar, header, dan container konten utama dashboard."""
        super().__init__(parent, bg=bg_white)
        
        self.user_profile_backend = User_Profile()
        self.current_user = current_user
        
        render_role_sidebar(self, current_user, "Dashboard_Admin")
        main_header(self, current_user, "Dashboard")  
        
        main_frame = tk.Frame(self, bg=bg_white)
        main_frame.pack(fill="both", expand=True)
        
        self.content_frame = tk.Frame(main_frame, bg=bg_white, pady=20)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=(20, 40))
        
        self.render_dashboard_view()

    def render_dashboard_view(self):
        """Memanggil fungsi pembuat kartu statistik dan tabel ringkasan aktivitas secara berurutan."""
        metrics = get_dashboard_metrics()
        
        self.create_stats_cards(metrics)
        
        tk.Frame(self.content_frame, bg=bg_white, height=25).pack()
        
        self.render_activity_table_section()

    def create_stats_cards(self, metrics):
        """Membuat dan menyusun kartu metrik ringkasan data statistik di bagian atas dashboard."""
        cards_data = [
            {"title": "Total Users", "value": metrics.get("total_users", 0), "color": "#3B82F6"},
            {"title": "Communities", "value": metrics.get("total_communities", 0), "color": "#10B981"},
            {"title": "Total Posts", "value": metrics.get("total_posts", 0), "color": "#F59E0B"},
            {"title": "Violations Log", "value": metrics.get("total_violations", 0), "color": "#EF4444"}
        ]
        
        cards_container = tk.Frame(self.content_frame, bg=bg_white)
        cards_container.pack(fill="x", pady=(0, 15))
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Poppins", 9), background=bg_white, foreground=text_dark, rowheight=32, fieldbackground=bg_white, borderwidth=0)
        style.map("Treeview", background=[("selected", dark)], foreground=[("selected", bg_white)])
        style.configure("Treeview.Heading", font=("Poppins", 9, "bold"), background=bg_main, foreground=text_dark, relief="flat", borderwidth=0)
        
        for i, card in enumerate(cards_data):
            card_frame = tk.Frame(cards_container, bg=bg_white, highlightthickness=1, highlightbackground=border_col)
            card_frame.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 16, 0))
            
            accent_bar = tk.Frame(card_frame, bg=card["color"], height=4)
            accent_bar.pack(fill="x", side="top")
            
            pad_inner = tk.Frame(card_frame, bg=bg_white, padx=20, pady=15)
            pad_inner.pack(fill="both", expand=True)
            
            lbl_title = tk.Label(pad_inner, text=card["title"].upper(), font=("Poppins", 9, "bold"), fg=text_muted, bg=bg_white)
            lbl_title.pack(anchor="w")
            
            lbl_value = tk.Label(pad_inner, text=f"{card['value']:,}", font=("Poppins", 22, "bold"), fg=text_dark, bg=bg_white)
            lbl_value.pack(anchor="w", pady=(6, 0))

    def render_activity_table_section(self):
        """Membuat tabel Treeview untuk menampilkan ringkasan akumulasi aktivitas seluruh pengguna."""
        section_frame = tk.Frame(self.content_frame, bg=bg_white)
        section_frame.pack(fill="both", expand=True)
        
        lbl_title = tk.Label(section_frame, text="👥 Ringkasan Aktivitas Kumulatif Seluruh Pengguna", font=("Poppins", 11, "bold"), fg=text_dark, bg=bg_white)
        lbl_title.pack(anchor="w", pady=(0, 12))

        activity_data = get_user_activity_summary()

        table_frame = tk.Frame(section_frame, bg=bg_white, highlightthickness=1, highlightbackground=border_col)
        table_frame.pack(fill="both", expand=True)

        columns = ("user_id", "username", "role", "posts", "likes_given", "comments_written", "violations")
        self.tree_act = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended", height=14)
        
        self.tree_act.heading("user_id", text="USER ID")
        self.tree_act.heading("username", text="USERNAME")
        self.tree_act.heading("role", text="ROLE")
        self.tree_act.heading("posts", text="TOTAL POSTS")
        self.tree_act.heading("likes_given", text="LIKES GIVEN")
        self.tree_act.heading("comments_written", text="COMMENTS WRITTEN")
        self.tree_act.heading("violations", text="TOTAL VIOLATIONS")

        self.tree_act.column("user_id", width=80, minwidth=60, anchor="center", stretch=True)
        self.tree_act.column("username", width=150, minwidth=100, anchor="w", stretch=True)
        self.tree_act.column("role", width=100, minwidth=80, anchor="center", stretch=True)
        self.tree_act.column("posts", width=120, minwidth=90, anchor="center", stretch=True)
        self.tree_act.column("likes_given", width=130, minwidth=100, anchor="center", stretch=True)
        self.tree_act.column("comments_written", width=160, minwidth=120, anchor="center", stretch=True)
        self.tree_act.column("violations", width=130, minwidth=100, anchor="center", stretch=True)

        for row in activity_data:
            if isinstance(row, dict):
                self.tree_act.insert("", "end", values=(row["user_id"], row["username"], row["role"], row["total_posts"], row["total_likes_given"], row["total_comments_written"], row["total_violations"]))
            else:
                self.tree_act.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_act.yview)
        self.tree_act.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        
        self.tree_act.pack(fill="both", expand=True, padx=1, pady=1)

        btn_container = tk.Frame(section_frame, bg=bg_white)
        btn_container.pack(fill="x", pady=(15, 0))

        btn_export_act = tk.Button(
            btn_container, text="📥   Export Semua Aktivitas Pengguna ke CSV", 
            font=("Poppins", 9, "bold"), bg=text_dark, fg=bg_white, 
            activebackground=dark, activeforeground=bg_white,
            relief="flat", bd=0, cursor="hand2", padx=20,
            command=lambda: self.export_metric_via_backend('activity', 'laporan_aktivitas_user.csv')
        )
        btn_export_act.pack(side="right", ipady=7)

    def export_metric_via_backend(self, metric_type, default_filename):
        """Membuka dialog penyimpanan berkas dan memicu logika backend untuk ekspor data CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default_filename,
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title=f"Simpan Laporan Metrik {metric_type.capitalize()}"
        )
        if not file_path:
            return
            
        res = export_metrics_to_csv(metric_type, file_path)
        if res:
            messagebox.showinfo("Ekspor Berhasil", f"Data metrik '{metric_type}' berhasil diekspor dan disimpan ke:\n{file_path}")
        else:
            messagebox.showerror("Ekspor Gagal", f"Terjadi kesalahan internal backend saat memproses berkas CSV.")

    def refresh_dashboard(self):
        """Membersihkan seluruh widget di dalam content frame dan memuat ulang data visual terbaru."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.render_dashboard_view()
        messagebox.showinfo("Sukses", "Semua data dashboard & laporan metrik berhasil diperbarui!")
