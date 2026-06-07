# gui/utils/navigation.py
from gui.components.sidebar import sidebar

def render_role_sidebar(current_frame, current_user, active_title="Home"):
    """
    Fungsi sentral untuk merakit dan menampilkan sidebar secara otomatis
    berdasarkan role user dan menandai halaman yang sedang aktif.
    """
    master = current_frame.master  # Mengakses Main (tk.Tk) untuk switch_frame

    # --- DEFINISI NAVIGASI (Hanya ditulis sekali di sini!) ---
    def go_home():
        from gui.frames.home import HomeFrame
        master.switch_frame(HomeFrame, current_user=current_user)
         
    def go_activity():
        from gui.frames.comunity import ComunityFrame
        master.switch_frame(ComunityFrame, current_user=current_user)
        
    def go_dashboard_moderator():
        from gui.frames.moderator.dashboard_moderator import DashboardModerator
        master.switch_frame(DashboardModerator, current_user=current_user)
        
    def go_dashboard_admin():
        from gui.frames.admin.dashboard_admin import DashboardAdminFrame
        master.switch_frame(DashboardAdminFrame, current_user=current_user)

    # --- RAKIT MENU DEFAULT (User Biasa) ---
    nav_items = [
        {"title": "Home", "comand": go_home, "active": active_title == "Home"},
        {"title": "Comunity", "comand": go_activity, "active": active_title == "Comunity"}
    ]
    
    # --- KONDISI DINAMIS BERDASARKAN ROLE ---
    if current_user.role == "moderator":            
        nav_items.insert(0, {
            "title": "Dashboard", 
            "comand": go_dashboard_moderator, 
            "active": active_title == "Dashboard_Moderator"
        })
    elif current_user.role == "admin":
        nav_items.insert(0, {
            "title": "Dashboard", 
            "comand": go_dashboard_admin, 
            "active": active_title == "Dashboard_Admin"
        }) 

    # Render sidebar bawaan kamu
    sidebar(current_frame, current_user, nav_items)