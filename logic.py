from model import User
from data import login_user_auth, register_user_auth, change_username, delete_user

class Auth:
    def login(self, username, password):        
        if not len(username) and not len(password):
            return {
                "status" : "Error",
                "message" : ("Error", "Username dan password tidak boleh kosong")
            }
            
        if len(password) < 8:
            return {
                "status" : "Error",
                "message" : ("Error", "Password harus 8 karakter")
            }
            
        res = login_user_auth(username)
        
        if not res:
            return {
                "status" : "Error",
                "message" : ("Error", "Username atau password salah")
            }

        user_data = User.convert(res)
            
        if user_data.password == password.lower():
            return {
                "status" : "Success",
                "message" : ("Success", "Login Berhasil"),
                "data" : user_data
            }
        else:
            return {
                "status" : "Error",
                "message" : ("Error", "Username atau password salah")
            }
        
    def register(self, username, password, confirm_password):
        if not len(username) and not len(password):
            return {
                "status" : "Error",
                "message" : ("Error", "Username dan password tidak boleh kosong")
            }
        
        if len(password) < 8:
            return {
                "status" : "Error",
                "message" : ("Error", "Password harus 8 karakter")
            }
        
        if not confirm_password == password :
            return {
                "status" : "Error",
                "message" : ("Error", "Confirm Password harus sama dengan password")
            }
        
        res = register_user_auth(username, password)

        if res == "username_exist":
            return {
                "status" : "Error",
                "message" : ("Error", f"Username {username} telah di ambil, silahkan pilih username lain")
            }
        
        user_data = User.convert(res)
        
        return {
            "status" : "Success",
            "message" : ("Success", "Register Berhasil"),
            "data" : user_data
        }
    
class User_Profile:
    def change_username(self, current_username, new_username):
        if not len(new_username):
            return{
                "status": "Error",
                "message": ("Error","Data username baru tidak boleh kosong")
            }
        
        res = change_username(current_username, new_username)
        
        if res == "username_exist":
            return{
                "status": "Error",
                "message": ("Error","Data username baru tidak telah diambil, silahkan pilih username lain")
            }
        
        user_data = User.convert(res)

        return{
            "status": "Success",
            "message": ("Success", "Username berhasil diganti"),
            "data": user_data
        }
     
    def delete_user(self, id):
        if not id:
            return{
                "status": "Error",
                "message": ("Error","Data user tidak dapat ditermukan")
            }
        
        res = delete_user(id)

        if res == True:
            return{
                "status": "Success",
                "message": ("Success", "Akun berhasil di hapus"),
            }
        else:
            return{
                "status": "Error",
                "message": ("Error","Akun gagal dihapus")
            }
        

     
       
        
        
        