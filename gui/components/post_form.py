import tkinter as tk
from tkinter import ttk, messagebox
from constrants import *
from logic import Community_Logic, Post_Logic, Sensor_Logic


# ============================================================
# SECTION: GUI COMPONENTS & FACTORIES
# ============================================================
def PostForm(parent, current_user, edit_post_data, on_submit):    
    """Membuat form kartu pembuatan dan pengeditan postingan komunitas."""
    # Inisialisasi Backend & Utilitas
    comunities = Community_Logic()
    posts = Post_Logic()
    sensor = Sensor_Logic()
    
    # State ID untuk mode edit (jika ada)
    selected_post_id = edit_post_data.id if edit_post_data else None

    # Main Card Container Minimalis & Elegan
    form_card = tk.Frame(
        parent, 
        bg=bg_white, 
        highlightbackground=border_col, 
        highlightthickness=1,
        padx=20,
        pady=18
    )
    form_card.pack(fill="x", padx=20, pady=(10, 15))
    
    # Header Status Form
    lbl_form_title = tk.Label(
        form_card, 
        text="✏️  Edit Post" if edit_post_data else "Buat Post", 
        font=("Poppins", 11, "bold"), 
        bg=bg_white, 
        fg=text_dark
    )
    lbl_form_title.pack(anchor="w", pady=(0, 12))
    
    # DROPDOWN PILIH KOMUNITAS
    dropdown_label = tk.Label(form_card, text="Pilih Komunitas", font=("Poppins", 8, "bold"), bg=bg_white, fg=text_muted)
    dropdown_label.pack(anchor="w", pady=(0, 2))
    
    # Ambil seluruh data komunitas dari database
    data_comunity = comunities.get_comunity_logic()
    
    # Filter: Hanya masukkan jika namanya 'Global Feed' ATAU user terdaftar sebagai member
    comunity_map = {}
    for row in data_comunity:
        if row.name == "Global Feed" or comunities.check_membership_logic(row.id, current_user.id):
            comunity_map[row.name] = row.id
            
    data_comunity_name = list(comunity_map.keys())
    
    # Styling Tkinter Combobox via Ttk Theme
    style = ttk.Style()
    style.configure("TCombobox", 
                    fieldbackground=bg_main, 
                    background=bg_main, 
                    bordercolor=border_col, 
                    lightcolor=border_col, 
                    darkcolor=border_col,
                    arrowcolor=text_dark)
    
    combo_comunity = ttk.Combobox(
        form_card, state="readonly", values=data_comunity_name, 
        font=("Poppins", 9), style="TCombobox"
    )
    combo_comunity.pack(fill="x", pady=(0, 14))
    
    # SET DEFAULT VALUE KE 'Global Feed' JIKA BUKAN MODE EDIT
    if edit_post_data:
        # Jika sedang mengedit, tampilkan komunitas lama bawaan postingan tersebut
        combo_comunity.set(edit_post_data.comunity_name)
    else:
        # Jika buat postingan baru, otomatis arahkan ke Global Feed
        if "Global Feed" in comunity_map:
            combo_comunity.set("Global Feed")
    
    # TEXT AREA POSTINGAN WITH INTERACTIVE FOCUS 
    text_label = tk.Label(form_card, text="Isi Post", font=("Poppins", 8, "bold"), bg=bg_white, fg=text_muted)
    text_label.pack(anchor="w")
    text_border = tk.Frame(form_card, bg=border_col, highlightbackground=border_col, highlightthickness=1)
    text_border.pack(fill="x", pady=(0, 12))
    
    ent_contents = tk.Text(
        text_border, height=4, font=("Poppins", 10), 
        bg=bg_main, fg=text_dark, relief="flat", wrap="word",
        padx=10, pady=10, insertbackground=text_dark
    )
    ent_contents.pack(fill="x")
    
    # --- Fungsi Logika Internal ---
    def on_focus_in(e):
        """Mengubah warna border frame dan background teks saat elemen mendapat fokus."""
        text_border.config(bg=text_dark, highlightbackground=text_dark)
        ent_contents.config(bg=bg_white) 

    def on_focus_out(e):
        """Mengembalikan warna border dan background teks ke default saat kehilangan fokus."""
        text_border.config(bg=border_col, highlightbackground=border_col)
        ent_contents.config(bg=bg_main)

    ent_contents.bind("<FocusIn>", on_focus_in)
    ent_contents.bind("<FocusOut>", on_focus_out)
    
    def get_comunity_id():
        """Mengambil ID komunitas yang sedang dipilih pada elemen combobox."""
        selected_name = combo_comunity.get()
        if not selected_name:
            return None
        return comunity_map[selected_name]

    def clear_post():
        """Mengosongkan isian text area, dropdown komunitas, dan memicu fungsi submit."""
        ent_contents.delete("1.0", tk.END)
        combo_comunity.set("")
        on_submit()

    def tambah_post():
        """Memproses penyaringan kata kasar dan mengunggah postingan baru ke database."""
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

    def edit_post():
        """Menyimpan pembaruan teks postingan lama ke database setelah disensor."""
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

    # BOTTOM ACTION BUTTONS CONTAINER
    btn_frame = tk.Frame(form_card, bg=bg_white)
    btn_frame.pack(fill="x", side="top")

    if edit_post_data:
        # Tombol aksi mode edit 
        btn_submit = tk.Button(
            btn_frame, text="Simpan Perubahan", command=edit_post,
            font=("Poppins", 9, "bold"), bg=text_dark, fg=bg_white, 
            relief="flat", bd=0, padx=18, pady=6, cursor="hand2"
        )
        btn_submit.pack(side="right")

        btn_clear = tk.Button(
            btn_frame, text="Batal", command=clear_post,
            font=("Poppins", 9), bg=bg_main, fg=text_dark, 
            relief="flat", bd=0, padx=18, pady=6, cursor="hand2"
        )
        btn_clear.pack(side="right", padx=8)
        
        # Isian awal mode edit
        ent_contents.insert("1.0", edit_post_data.content)
        combo_comunity.set(edit_post_data.comunity_name)
    else:
        # Tombol aksi mode publish normal
        btn_submit = tk.Button(
            btn_frame, text="Buat Post", command=tambah_post,
            font=("Poppins", 9, "bold"), bg=text_dark, fg=bg_white, 
            relief="flat", bd=0, padx=18, pady=6, cursor="hand2"
        )
        btn_submit.pack(side="right")

        btn_clear = tk.Button(
            btn_frame, text="Reset", command=clear_post,
            font=("Poppins", 9), bg=bg_white, fg=text_muted, 
            relief="flat", bd=0, padx=12, pady=6, cursor="hand2"
        )
        btn_clear.pack(side="right", padx=6)
            
    return form_card