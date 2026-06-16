import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from logic import Community_Logic, Post_Logic, Sensor_Logic


# ============================================================
# SECTION: GUI CLASSES & DIALOGS
# ============================================================
class PostFormWindow(tk.Toplevel):
    """Pop-up Modal Jendela Pembuatan / Pengeditan Postingan bergaya Media Sosial."""
    
    def __init__(self, parent_frame, current_user, edit_post_data=None, forced_community_id=None, on_submit_callback=None):
        """Menginisialisasi layout form postingan, dropdown komunitas, dan text area."""
        super().__init__(parent_frame)
        self.parent_frame = parent_frame
        self.current_user = current_user
        self.edit_post_data = edit_post_data
        self.forced_community_id = forced_community_id
        self.on_submit_callback = on_submit_callback

        # Inisialisasi Logic
        self.comunities = Community_Logic()
        self.posts = Post_Logic()
        self.sensor = Sensor_Logic()
        self.selected_post_id = edit_post_data.id if edit_post_data else None

        # Konfigurasi Window Pop-up
        window_title = "✏️ Edit Postingan" if edit_post_data else "✍️ Buat Postingan Baru"
        self.title(window_title)
        self.configure(bg=bg_white)
        self.resizable(False, False)
        self.grab_set()  # Mengunci fokus agar user menyelesaikan pop-up ini dahulu

        # Penentuan posisi tengah layar (Tinggi 380 sudah cukup pas)
        width, height = 480, 380
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Container Utama (Padding Dalam)
        container = tk.Frame(self, bg=bg_white, padx=25, pady=20)
        container.pack(fill="both", expand=True)

        # Header Title di dalam Pop-up
        lbl_form_title = tk.Label(container, text=window_title, font=("Poppins", 12, "bold"), bg=bg_white, fg=text_dark)
        lbl_form_title.pack(anchor="w", pady=(0, 15))

        # DROPDOWN PILIH KOMUNITAS 
        tk.Label(container, text="Pilih Komunitas Tujuan", font=("Poppins", 8, "bold"), bg=bg_white, fg=text_muted).pack(anchor="w", pady=(0, 2))
        
        # Ambil daftar semua komunitas
        data_comunity = self.comunities.get_comunity_logic()
        self.comunity_map = {row.name: row.id for row in data_comunity}
        data_comunity_name = list(self.comunity_map.keys())

        style = ttk.Style()
        style.configure("PopUp.TCombobox", fieldbackground=bg_main, background=bg_main, bordercolor=border_col, arrowcolor=text_dark)

        self.combo_comunity = ttk.Combobox(container, state="readonly", values=data_comunity_name, font=("Poppins", 10), style="PopUp.TCombobox")
        self.combo_comunity.pack(fill="x", pady=(0, 15))

        # CONTAINER ACCELERATOR BUTTONS (PACK LEBIH AWAL KE BAWAH)
        btn_frame = tk.Frame(container, bg=bg_white)
        btn_frame.pack(fill="x", side="bottom", pady=(10, 0))

        # Tombol Kirim / Submit
        submit_text = "Simpan Perubahan" if edit_post_data else "Bagikan Kiriman"
        submit_command = self.edit_post if edit_post_data else self.tambah_post

        self.btn_submit = tk.Button(btn_frame, text=submit_text, command=submit_command, font=("Poppins", 9, "bold"), bg=dark, fg=bg_white, relief="flat", padx=18, pady=8, cursor="hand2")
        self.btn_submit.pack(side="right", padx=(10, 0))

        # Tombol Keluar / Batal
        btn_cancel = tk.Button(btn_frame, text="Batal", command=self.destroy, font=("Poppins", 9), bg=bg_main, fg=text_dark, relief="flat", padx=15, pady=8, cursor="hand2")
        btn_cancel.pack(side="right")

        # TEXT AREA CONTENT (PACK TERAKHIR BIAR MENGISI SISA RUANG) 
        tk.Label(container, text="Apa yang ingin Anda bagikan?", font=("Poppins", 8, "bold"), bg=bg_white, fg=text_muted).pack(anchor="w")
        
        self.text_border = tk.Frame(container, bg=border_col, highlightbackground=border_col, highlightthickness=1)
        self.text_border.pack(fill="both", expand=True, pady=(0, 5))

        self.ent_contents = tk.Text(self.text_border, font=("Poppins", 10), bg=bg_main, fg=text_dark, relief="flat", wrap="word", padx=12, pady=12, insertbackground=text_dark)
        self.ent_contents.pack(fill="both", expand=True)

        # Efek Animasi Focus Border Box
        self.ent_contents.bind("<FocusIn>", lambda e: [self.text_border.config(bg=text_dark), self.ent_contents.config(bg=bg_white)])
        self.ent_contents.bind("<FocusOut>", lambda e: [self.text_border.config(bg=border_col), self.ent_contents.config(bg=bg_main)])

        # LOGIKA KONDISIONAL AWALAN DATA 
        if edit_post_data:
            self.ent_contents.insert("1.0", edit_post_data.content)
            self.combo_comunity.set(edit_post_data.comunity_name)
        if forced_community_id:
            for name, c_id in self.comunity_map.items():
                if c_id == forced_community_id:
                    self.combo_comunity.set(name)
                    self.combo_comunity.config(state="disabled")
                    break

    def get_selected_community_id(self):
        """Mengambil ID komunitas berdasarkan nama yang dipilih di dropdown."""
        selected_name = self.combo_comunity.get()
        return self.comunity_map.get(selected_name)

    def tambah_post(self):
        """Menyensor konten teks dan membuat postingan baru di database."""
        user_id = self.current_user.id
        community_id = self.get_selected_community_id()

        if not community_id:
            messagebox.showwarning("Peringatan", "Silakan tentukan komunitas tujuan terlebih dahulu!", parent=self)
            return

        raw_content = self.ent_contents.get("1.0", tk.END).strip()
        if not raw_content:
            messagebox.showwarning("Peringatan", "Konten kiriman tidak boleh kosong!", parent=self)
            return

        content = self.sensor.sensor_teks(raw_content, user_id)
        res = self.posts.create_posts_logic(user_id, community_id, content)

        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1], parent=self)
            if self.on_submit_callback: self.on_submit_callback()
            self.destroy() 
        else:
            messagebox.showerror(res["message"][0], res["message"][1], parent=self)

    def edit_post(self):
        """Menyimpan modifikasi teks postingan lama setelah disaring sensor."""
        community_id = self.get_selected_community_id()
        raw_content = self.ent_contents.get("1.0", tk.END).strip()

        if not community_id or not raw_content:
            messagebox.showwarning("Peringatan", "Data tidak boleh kosong!", parent=self)
            return

        content = self.sensor.sensor_teks(raw_content, self.current_user.id)
        res = self.posts.edit_post_logic(self.selected_post_id, content, community_id)

        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1], parent=self)
            if self.on_submit_callback: self.on_submit_callback()
            self.destroy()
        else:
            messagebox.showerror(res["message"][0], res["message"][1], parent=self)
