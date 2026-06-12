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
    
    def resgiter_admin_logic(self, username, password, role, confirm_password):
        if not len(username) or not len(password) or not len(role):
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
        
        res = register_admin(username, password, role)

        if res == "username_exist":
            return {
                "status" : "Error",
                "message" : ("Error", f"Username {username} telah di ambil, silahkan pilih username lain")
            }
                
        return {
            "status" : "Success",
            "message" : ("Success", "Register Berhasil"),
        }
    
    def edit_resgiter_admin_logic(self, id, username, password, role, confirm_password):
        # Validasi username dan role tetap wajib
        if not len(username) or not len(role):
            return {
                "status" : "Error",
                "message" : ("Error", "Username dan Role tidak boleh kosong")
            }
        
        # Validasi password HANYA berjalan jika admin mengetikkan sesuatu di kolom password
        if len(password) > 0:
            if len(password) < 8:
                return {
                    "status" : "Error",
                    "message" : ("Error", "Password baru harus minimal 8 karakter")
                }
            
            if not confirm_password == password:
                return {
                    "status" : "Error",
                    "message" : ("Error", "Confirm Password harus sama dengan password")
                }
        
        # Jalankan fungsi update database
        res = edit_user(id, username, password, role)

        if res == "username_exist":
            return {
                "status" : "Error",
                "message" : ("Error", f"Username {username} telah diambil, silahkan pilih username lain")
            }
                
        return {
            "status" : "Success",
            "message" : ("Success", "Edit user Berhasil"),
        }
    
    def get_user_logic(self):
        res = get_user()

        data_user = [User.convert(row) for row in res]

        return data_user

    
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
        
    def get_comunity_post_logic(self, id, current_user_id):
        res = get_comunity_post(id, current_user_id)

        return [Post.convert(row) for row in res]
        
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

class Comment_Logic:
    def comments_logic(self, user_id, post_id, content):
        res = comment(user_id, post_id, content)

        if res == True:
            return{
                "status": "Success",
                "message": ("Success", "Comment berhasil dibuat")
            }
        else:
            return{
                "status": "Error",
                "message": ("Error","Comment berhasil dibuat")
            }
        
    def get_comments_logic(self, post_id):
        res = get_comment(post_id)

        data_comments = [Comment.convert(row) for row in res]

        return data_comments
    
    def upadate_comment_logic(self, id, content):
        if not content:
            if not content:
                return{
                    "status": "Error",
                    "message": ("Error","Data tidak boleh kosong")
                }
            
        res = update_comment(id, content)

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
        
    def delete_comment_logic(self, id):
        res = delete_comment(id)

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
        
class Saved_Post_Logic:
    def saved_post_logic(self, user_id, post_id):
        res = saved_post(user_id, post_id)
        
        if res == "save":
            return{
                "status": "save",
            }
        else:
            return{
                "status": "unsave",
            }

    def get_saved_posts_logic(self, current_user_id):
        # Ambil data rows dari database
        res = get_saved_posts(current_user_id)

        # Konversi row database menjadi list object model Post
        data_posts = [Post.convert(row) for row in res]

        return data_posts
    
class Follow_Logic:
    def follow_user_logic(self, follower_id, following_id):
        # res sekarang akan berisi "inserted", "deleted", atau "error"
        res = follow_user(follower_id, following_id)

        if res == "inserted":
            return {
                "status": "Success",
                "message": ("Success", "Permintaan pertemanan berhasil terkirim")
            }
        elif res == "deleted":
            return {
                "status": "Unfollowed",
                "message": ("Success", "Berhasil berhenti mengikuti / membatalkan permintaan")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error", "Gagal memproses permintaan, silakan coba lagi.")
            }
        
    def get_follower_count_logic(self, user_id):
       res = get_follower_count(user_id)
       return res

    def get_following_count_logic(self, user_id):
        res = get_following_count(user_id)
        return res
        
class Notification_Logic:
    def get_notifications_logic(self, user_id):
        res = get_notifications(user_id)
        return [NotificationData.convert(row) for row in res]

    def process_follow_action_logic(self, notification_id, follows_id, action):
        res = process_follow_action(notification_id, follows_id, action)

        if res == "accept":
            return {
                "status": "Success",
                "message": ("Success", "Berhasil diterima")
            }
        elif res == "decline":
            return {
                "status": "Success",
                "message": ("Success", "Berhasil ditolak")
            }

    def delete_notification(self, notification_id):
        # Untuk menghapus info umum setelah dibaca oleh user
        conn = get_db()
        conn.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()
        return {"status": "Success"}
    
