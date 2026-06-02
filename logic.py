from model import User
from data import login_user_auth

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
        
       
        
        
        