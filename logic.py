from model import *
from data import *

class Auth:
    def login_logic(self, username, password):        
        if not len(username) or not len(password):
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
        
    def register_logic(self, username, password, confirm_password):
        if not len(username) or not len(password):
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
    def change_username_logic(self, current_username, new_username):
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
     
    def delete_user_logic(self, id):
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
        
    def get_user_by_id(id):
        pass
        
class Comunity_Logic:
    def create_comunity_logic(self, user_id, name, descripition):
        if not len(name) or not len(descripition):
            return{
                "status": "Error",
                "message": ("Error","Nama komunitas dan deskripsi tidak boleh kosong")
            }
        
        res = create_comunity(user_id, name, descripition)

        if res == "name_exist":
            return{
                "status": "Error",
                "message": ("Error","Nama komunitas sudah ada, silahakn cari nama lain")
            }
                
        return{
            "status": "Success",
            "message": ("Success", "Komunitas berhasil dibuat"),
        }
    
    def update_comunity_logic(self, user_id, name, descripition):
        if not len(name) or not len(descripition):
            return{
                "status": "Error",
                "message": ("Error","Nama komunitas dan deskripsi tidak boleh kosong")
            }
        
        res = update_comunity(user_id, name, descripition)

        if res == "name_exist":
            return{
                "status": "Error",
                "message": ("Error","Nama komunitas sudah ada, silahakn cari nama lain")
            }
                
        return{
            "status": "Success",
            "message": ("Success", "Komunitas berhasil diedit"),
        }
    
    def get_comunity_logic(self):
        res = get_comunity()

        data_comunity = [Comunity.convert(row) for row in res]

        return data_comunity
    
    def delete_comunity_logic(self, id):
        res = delete_comunity(id)

        if res == True:
            return{
                "status": "Success",
                "message": ("Success", "Data berhasil di hapus")
            }
        else:
            return{
                "status": "Error",
                "message": ("Error","Data gagal dihapus")
            }
        
class Post_Logic:
    def create_posts_logic(self, user_id, comunity_id, content):
        if not comunity_id or not content:
            return{
                "status": "Error",
                "message": ("Error","Nama komunitas dan deskripsi tidak boleh kosong")
            }
        
        res = create_post(user_id, comunity_id, content)

        if res == True:
            return{
                "status": "Success",
                "message": ("Success", "Post berhasil di buat")
            }
        else:
            return{
                "status": "Error",
                "message": ("Error","Post gagal dibuat")
            }
        
    def get_posts_logic(self, current_user_id):
        res = get_post(current_user_id)

        data_posts = [Post.convert(row) for row in res]

        return data_posts
    
    def delete_post_logic(self, id):
        res = delete_post(id)

        if res == True:
            return{
                "status": "Success",
                "message": ("Success", "Data berhasil di hapus")
            }
        else:
            return{
                "status": "Error",
                "message": ("Error","Data gagal dihapus")
            }
        
    def edit_post_logic(self, id, content, comunity_id):
        if not content or not comunity_id:
            return{
                "status": "Error",
                "message": ("Error","Data tidak boleh kosong")
            }
        
        res = update_post(id, content, comunity_id)

        if res == True:
            return{
                "status": "Success",
                "message": ("Success", "Data berhasil di update")
            }
        else:
            return{
                "status": "Error",
                "message": ("Error","Data gagal di update")
            }

class Like_Logic:
    def like_logic(self, user_id, post_id):
        res = like(user_id, post_id)
        
        if res == "like":
            return{
                "status": "like",
            }
        else:
            return{
                "status": "unlike",
            }
        