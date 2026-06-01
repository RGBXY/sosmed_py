from model import User
from data import get_user_auth

class Auth:
    def login(self, username, password):
        res = get_user_auth(username)
        
        if res:            
            data = User.convert(res)
            return {
                "status" : "Success",
                "message" : ("Success", "Login Berhasil"),
                "data" : data
            }
        
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
            
        if res and res.password == password.lower():
            return {
                "status" : "Success",
                "message" : ("Success", "Login Berhasil")
            }
        else:
            return {
                "status" : "Error",
                "message" : ("Error", "Username atau password salah")
            }
       
        
        
        