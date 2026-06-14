import tkinter as tk
from data import init_db
from logic import Sensor_Logic
from gui.frames.auth.login import LoginFrame
from gui.frames.home import HomeFrame
from gui.frames.admin.dashboard_admin import DashboardAdminFrame
from gui.frames.moderator.dashboard_moderator import DashboardModeratorFrame

class Main(tk.Tk):
    """Kelas utama aplikasi Hubble yang mengatur navigasi antar halaman (frame) dan state pengguna."""

    def __init__(self):
        """Menginisialisasi window utama, database, logika sensor, dan menampilkan halaman login awal."""
        super().__init__()
        self.state("zoomed")
        self.title("Hubble")
        init_db()

        self.sensor = Sensor_Logic()

        self.current_user = None
        self.current_frame = None

        self.open_login()
        self.sensor.get_badwords_sensor_logic()
        
    # Routing Function
    def switch_frame(self, frame_class, **kwargs):
        """Menghancurkan frame yang aktif saat ini dan menggantinya dengan frame yang baru."""
        # Logika pergantian frame: Hapus instance lama dari memori untuk mencegah memory leak
        if self.current_frame:
            self.current_frame.destroy()

        # Inisialisasi frame baru dengan melempar 'self' sebagai parent window dan argumen tambahan (**kwargs)
        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)
        
    # Login GUI Function
    def open_login(self):        
        """Membuka halaman login dan mendaftarkan callback jika autentikasi berhasil."""
        self.switch_frame(LoginFrame, auth_success=self.auth_success)

    def logout(self):
        """Menghapus data session user yang aktif dan mengembalikan tampilan ke halaman login."""
        self.current_user = None
        self.switch_frame(LoginFrame, auth_success=self.auth_success)
                
    # Callback for Register and Login
    def auth_success(self, user):
        """Fungsi callback yang menangani pengalihan halaman dashboard berdasarkan role user yang berhasil login."""
        self.current_user = user

        # Logika Routing Berbasis Role (Role-Based Access Control):
        # Mengarahkan user ke halaman yang sesuai dengan hak akses (role) masing-masing
        if user.role == "user":
            self.switch_frame(HomeFrame, current_user=self.current_user)
            
        elif user.role == "moderator":
            self.switch_frame(DashboardModeratorFrame, current_user=self.current_user)

        elif user.role == "admin":
            self.switch_frame(DashboardAdminFrame, current_user=self.current_user)        

if __name__ == "__main__":
    Main().mainloop()