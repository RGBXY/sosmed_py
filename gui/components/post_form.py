import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from logic import Comunity_Logic, Post_Logic, Sensor_Logic

def PostForm(parent, current_user, edit_post_data, on_submit):    
    # Inisialisasi Backend & Utilitas
    comunities = Comunity_Logic()
    posts = Post_Logic()
    sensor = Sensor_Logic()
    
    # State ID untuk mode edit (jika ada)
    selected_post_id = edit_post_data.id if edit_post_data else None

    # Main Card Container (Disamakan dengan form_card milik ComunityFrame)
    form_card = tk.Frame(
        parent, 
        bg=bg_white, 
        highlightbackground=border_col, 
        highlightthickness=1,
        padx=20,
        pady=20
    )
    form_card.pack(fill="x", padx=20, pady=15)
    
    # Title Form Dinamis sesuai Mode
    lbl_form_title = tk.Label(
        form_card, 
        text="Edit Postingan Konten" if edit_post_data else "Buat Postingan Baru", 
        font=("Poppins", 11, "bold"), 
        bg=bg_white, 
        fg=bg_primary
    )
    lbl_form_title.pack(anchor="w", pady=(0, 15))
    
    # Input Grid Container
    input_grid = tk.Frame(form_card, bg=bg_white)
    input_grid.pack(fill="x")
    
    # Row 0: Pilihan Komunitas (Combobox)
    tk.Label(input_grid, text="Pilih Komunitas", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark).grid(row=0, column=0, sticky="w", pady=5)
    
    # Ambil data mapping komunitas untuk dropdown
    data_comunity = comunities.get_comunity_logic()
    comunity_map = {row.name: row.id for row in data_comunity}
    data_comunity_name = list(comunity_map.keys())
    
    combo_comunity = ttk.Combobox(input_grid, state="readonly", values=data_comunity_name, font=("Poppins", 10))
    combo_comunity.grid(row=0, column=1, sticky="ew", padx=(15, 0), pady=5)
    
    # Row 1: Konten Postingan (Text Widget dengan border modis bawaan Tkinter)
    tk.Label(input_grid, text="Isi Postingan", font=("Poppins", 9, "bold"), bg=bg_white, fg=text_dark).grid(row=1, column=0, sticky="nw", pady=8)
    
    # Text widget dibungkus frame agar border highlightthickness-nya identik dengan Entry
    text_border = tk.Frame(input_grid, bg=border_col, highlightbackground=border_col, highlightthickness=1)
    text_border.grid(row=1, column=1, sticky="ew", padx=(15, 0), pady=5)
    
    ent_contents = tk.Text(text_border, height=4, font=("Poppins", 10), bg=bg_main, relief="flat", wrap="word")
    ent_contents.pack(fill="x", padx=1, pady=1)
    
    # Membuat kolom input melebar secara fleksibel
    input_grid.columnconfigure(1, weight=1)
    
    # Helper get ID Komunitas
    def get_comunity_id():
        selected_name = combo_comunity.get()
        if not selected_name:
            return None
        return comunity_map[selected_name]

    # Fungsi Reset / Clear Form
    def clear_post():
        ent_contents.delete("1.0", tk.END)
        combo_comunity.set("")
        on_submit() # Memicu reload feed pada HomeFrame

    # Fungsi Tambah Post Baru
    def tambah_post():
        user_id = current_user.id
        comunity_id = get_comunity_id()
        
        if not comunity_id:
            messagebox.showwarning("Peringatan", "Silakan pilih komunitas terlebih dahulu!")
            return
            
        raw_content = ent_contents.get("1.0", tk.END).strip()
        if not raw_content:
            messagebox.showwarning("Peringatan", "Konten postingan tidak boleh kosong!")
            return
            
        content = sensor.sensor_teks(raw_content, user_id)
        res = posts.create_posts_logic(user_id, comunity_id, content)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            clear_post()

    # Fungsi Simpan Update Edit Post
    def edit_post():
        if not selected_post_id:
            messagebox.showerror("Error", "ID postingan tidak valid.")
            return
            
        comunity_id = get_comunity_id()
        if not comunity_id:
            messagebox.showwarning("Peringatan", "Silakan pilih komunitas terlebih dahulu!")
            return
            
        raw_content = ent_contents.get("1.0", tk.END).strip()
        if not raw_content:
            messagebox.showwarning("Peringatan", "Konten postingan tidak boleh kosong!")
            return

        content = sensor.sensor_teks(raw_content, current_user.id)   
        res = posts.edit_post_logic(selected_post_id, content, comunity_id)

        if res["status"] == "Error":
            messagebox.showerror(res["message"][0], res["message"][1])
            return
        
        if res["status"] == "Success":
            messagebox.showinfo(res["message"][0], res["message"][1])
            clear_post()

    # --- BTN CONTAINER ACTION ---
    btn_frame = tk.Frame(form_card, bg=bg_white)
    btn_frame.pack(fill="x", pady=(15, 0))

    if edit_post_data:
        # Tampilan Tombol saat Mode Edit Terdeteksi
        btn_submit = tk.Button(
            btn_frame, text="Simpan Perubahan", command=edit_post,
            font=("Poppins", 9, "bold"), bg="#4D65FF", fg=bg_white, relief="flat", padx=15, pady=5, cursor="hand2"
        )
        btn_submit.pack(side="left", padx=(0, 10))

        btn_clear = tk.Button(
            btn_frame, text="Batal / Cancel", command=clear_post,
            font=("Poppins", 9), bg=border_col, fg=text_dark, relief="flat", padx=15, pady=5, cursor="hand2"
        )
        btn_clear.pack(side="left")
        
        # Mengisi otomatis nilai lama ke dalam form input edit
        ent_contents.insert("1.0", edit_post_data.content)
        combo_comunity.set(edit_post_data.comunity_name)
    else:
        # Tampilan Tombol saat Mode Create Normal
        btn_submit = tk.Button(
            btn_frame, text="Post Konten", command=tambah_post,
            font=("Poppins", 9, "bold"), bg=bg_primary, fg=bg_white, relief="flat", padx=15, pady=5, cursor="hand2"
        )
        btn_submit.pack(side="left", padx=(0, 10))

        btn_clear = tk.Button(
            btn_frame, text="Clear", command=clear_post,
            font=("Poppins", 9), bg=border_col, fg=text_dark, relief="flat", padx=15, pady=5, cursor="hand2"
        )
        btn_clear.pack(side="left")
            
    return form_card