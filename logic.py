from model import *
from data import *

class Auth:
    def login_logic(self, username, password):        
        if not username or not password:
            return {
                "status" : "Error",
                "message" : ("Error", "Username dan password tidak boleh kosong")
            }
            
        if len(password) < 8:
            return {
                "status" : "Error",
                "message" : ("Error", "Password harus minimal 8 karakter")
            }
            
        res = login_user_auth(username, password)
        
        if not res:
            return {
                "status" : "Error",
                "message" : ("Error", "Username atau password salah")
            }

        user_data = User.convert(res)
            
        return {
            "status" : "Success",
            "message" : ("Success", "Login Berhasil"),
            "data" : user_data
        }
        
    def register_logic(self, username, password, confirm_password):
        if not username or not password:
            return {
                "status" : "Error",
                "message" : ("Error", "Username dan password tidak boleh kosong")
            }
        
        if len(password) < 8:
            return {
                "status" : "Error",
                "message" : ("Error", "Password harus minimal 8 karakter")
            }
        
        if confirm_password != password:
            return {
                "status" : "Error",
                "message" : ("Error", "Confirm Password harus sama dengan password")
            }
        
        res = register_user_auth(username, password)

        if res == "username_exist":
            return {
                "status" : "Error",
                "message" : ("Error", f"Username {username} telah diambil, silahkan pilih username lain")
            }
        
        user_data = User.convert(res)
        
        return {
            "status" : "Success",
            "message" : ("Success", "Register Berhasil"),
            "data" : user_data
        }
    
    # Perbaikan typo: resgiter -> register
    def register_admin_logic(self, username, password, role, confirm_password):
        if not username or not password or not role:
            return {
                "status" : "Error",
                "message" : ("Error", "Username, password, dan role tidak boleh kosong")
            }
        
        if len(password) < 8:
            return {
                "status" : "Error",
                "message" : ("Error", "Password harus minimal 8 karakter")
            }
        
        if confirm_password != password:
            return {
                "status" : "Error",
                "message" : ("Error", "Confirm Password harus sama dengan password")
            }
        
        res = register_admin(username, password, role)

        if res == "username_exist":
            return {
                "status" : "Error",
                "message" : ("Error", f"Username {username} telah diambil, silahkan pilih username lain")
            }
                
        return {
            "status" : "Success",
            "message" : ("Success", "Register Admin Berhasil"),
        }
    
    # Perbaikan typo: edit_resgiter -> edit_register
    def edit_register_admin_logic(self, id, username, password, role, confirm_password):
        if not username or not role:
            return {
                "status" : "Error",
                "message" : ("Error", "Username dan Role tidak boleh kosong")
            }
        
        if len(password) > 0:
            if len(password) < 8:
                return {
                    "status" : "Error",
                    "message" : ("Error", "Password baru harus minimal 8 karakter")
                }
            
            if confirm_password != password:
                return {
                    "status" : "Error",
                    "message" : ("Error", "Confirm Password harus sama dengan password")
                }
        
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
        res = get_users_paginated()
        return [User.convert(row) for row in res]

    
class User_Profile:
    def change_username_logic(self, current_username, new_username):
        if not new_username:
            return {
                "status": "Error",
                "message": ("Error","Data username baru tidak boleh kosong")
            }
        
        res = change_username(current_username, new_username)
        
        if res == "username_exist":
            return {
                "status": "Error",
                "message": ("Error","Data username baru telah diambil, silahkan pilih username lain")
            }
        
        user_data = User.convert(res)

        return {
            "status": "Success",
            "message": ("Success", "Username berhasil diganti"),
            "data": user_data
        }
     
    def change_password_logic(self, user_id, current_password, new_password):
        current_password = current_password.strip()
        new_password = new_password.strip()

        if not current_password or not new_password:
            return {
                "status": "Error",
                "message": ("Error", "Password lama dan password baru tidak boleh kosong!")
            }
            
        if len(new_password) < 8:
            return {
                "status": "Error",
                "message": ("Error", "Password baru minimal harus 8 karakter!")
            }

        res = change_password(user_id, current_password, new_password)
        
        if res == "wrong_password":
            return {
                "status": "Error",
                "message": ("Gagal", "Password lama yang Anda masukkan salah!")
            }
            
        if res == "user_not_found":
            return {
                "status": "Error",
                "message": ("Gagal", "Pengguna tidak ditemukan!")
            }
            
        if res == "db_error":
            return {
                "status": "Error",
                "message": ("Error", "Gagal memperbarui database. Silakan coba lagi.")
            }

        return {
            "status": "Success",
            "message": ("Sukses", "Password berhasil diganti!"),
            "data": None
        }
     
    def delete_user_logic(self, id):
        if not id:
            return {
                "status": "Error",
                "message": ("Error","Data user tidak dapat ditemukan")
            }
        
        res = delete_user(id)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Akun berhasil dihapus"),
            }
        else:
            return {
                "status": "Error",
                "message": ("Error","Akun gagal dihapus")
            }
        
# Perbaikan typo: Comunity -> Community
class Community_Logic:
    def create_comunity_logic(self, user_id, name, descripition):
        if not name or not descripition:
            return {
                "status": "Error",
                "message": ("Error","Nama komunitas dan deskripsi tidak boleh kosong")
            }
        
        res = create_community(user_id, name, descripition)

        if res == "name_exist":
            return {
                "status": "Error",
                "message": ("Error","Nama komunitas sudah ada, silahkan cari nama lain")
            }
                
        return {
            "status": "Success",
            "message": ("Success", "Komunitas berhasil dibuat"),
        }
    
    def get_community_detail_logic(self, comunity_id):
        res = get_comunity_detail(comunity_id)
        return Comunity.convert(res)
    
    def update_comunity_logic(self, user_id, name, descripition):
        if not name or not descripition:
            return {
                "status": "Error",
                "message": ("Error","Nama komunitas dan deskripsi tidak boleh kosong")
            }
        
        res = update_community(user_id, name, descripition)

        if res == "name_exist":
            return {
                "status": "Error",
                "message": ("Error","Nama komunitas sudah ada, silahkan cari nama lain")
            }
                
        return {
            "status": "Success",
            "message": ("Success", "Komunitas berhasil diedit"),
        }
    
    def get_comunity_logic(self):
        res = get_comunities()
        return [Comunity.convert(row) for row in res]
    
    def delete_comunity_logic(self, id):
        res = delete_community(id)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Data berhasil dihapus")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error","Data gagal dihapus")
            }
        
    def get_comunity_post_logic(self, id, current_user_id):
        res = get_community_post(id, current_user_id)
        return [Post.convert(row) for row in res]    
    
    def join_community_logic(self, community_id, user_id):
        if not community_id or not user_id:
            return {
                "status": "Error",
                "message": ("Gagal", "Parameter data tidak valid.")
            }
            
        is_member = check_membership_status(community_id, user_id)
        if is_member:
            return {
                "status": "Error",
                "message": ("Pemberitahuan", "Anda sudah bergabung dengan komunitas ini.")
            }
            
        res = join_community(community_id, user_id)
        if res:
            return {
                "status": "Success",
                "message": ("Berhasil", "Selamat! Anda berhasil bergabung ke komunitas.")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error", "Terjadi kesalahan sistem database saat mencoba bergabung.")
            }

    def leave_community_logic(self, community_id, user_id):
        if not community_id or not user_id:
            return {
                "status": "Error",
                "message": ("Gagal", "Parameter data tidak valid.")
            }

        res = leave_community(community_id, user_id)
        if res:
            return {
                "status": "Success",
                "message": ("Berhasil", "Anda telah keluar dari komunitas ini.")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error", "Gagal keluar. Anda mungkin memang belum bergabung di grup ini.")
            }

    def check_membership_logic(self, community_id, user_id):
        return check_membership_status(community_id, user_id)

    def get_community_members_logic(self, community_id):
        res = get_community_members(community_id)
        return [Comunity_Member.convert(row) for row in res]    
        
class Post_Logic:
    def create_posts_logic(self, user_id, comunity_id, content):
        if not comunity_id or not content:
            return {
                "status": "Error",
                "message": ("Error","Nama komunitas dan konten tidak boleh kosong")
            }
        
        res = create_post(user_id, comunity_id, content)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Post berhasil dibuat")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error","Post gagal dibuat")
            }
        
    def get_posts_logic(self, current_user_id):
        res = get_global_feed(current_user_id)
        return [Post.convert(row) for row in res]
    
    def delete_post_logic(self, id):
        res = delete_post(id)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Data berhasil dihapus")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error","Data gagal dihapus")
            }
        
    def edit_post_logic(self, id, content, comunity_id):
        if not content or not comunity_id:
            return {
                "status": "Error",
                "message": ("Error","Data tidak boleh kosong")
            }
        
        res = update_post(id, content, comunity_id)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Data berhasil di-update")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error","Data gagal di-update")
            }

class Like_Logic:
    def like_logic(self, user_id, post_id):
        res = like(user_id, post_id)
        if res == "like":
            return {"status": "like"}
        else:
            return {"status": "unlike"}


class Comment_Logic:
    def comments_logic(self, user_id, post_id, content):
        # Perbaikan: Menghilangkan if ganda bersarang yang redundan
        if not content:
            return {
                "status": "Error",
                "message": ("Error","Konten komentar tidak boleh kosong")
            }

        res = comment(user_id, post_id, content)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Comment berhasil dibuat")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error","Comment gagal dibuat")
            }
        
    def get_comments_logic(self, post_id):
        res = get_comments(post_id)
        return [Comment.convert(row) for row in res]
    
    # Perbaikan typo: upadate -> update
    def update_comment_logic(self, id, content):
        if not content:
            return {
                "status": "Error",
                "message": ("Error","Data tidak boleh kosong")
            }
            
        res = update_comment(id, content)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Data berhasil di-update")
            }
        else:
            return {
                "status": "Error",
                "message": ("Error","Data gagal di-update")
            }
        
    def delete_comment_logic(self, id):
        res = delete_comment(id)

        if res:
            return {
                "status": "Success",
                "message": ("Success", "Data berhasil dihapus")
            }
        else:
            # Perbaikan: Pesan error disesuaikan (sebelumnya: "Comment berhasil dibuat")
            return {
                "status": "Error",
                "message": ("Error","Data gagal dihapus")
            }
        
class Saved_Post_Logic:
    def saved_post_logic(self, user_id, post_id):
        res = saved_post(user_id, post_id)
        if res == "save":
            return {"status": "save"}
        else:
            return {"status": "unsave"}

    def get_saved_posts_logic(self, current_user_id):
        res = get_saved_posts(current_user_id)
        return [Post.convert(row) for row in res]
    
class Follow_Logic:
    def follow_user_logic(self, follower_id, following_id):
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
        return get_follower_count(user_id)

    def get_following_count_logic(self, user_id):
        return get_following_count(user_id)
         
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
        conn = get_db()
        conn.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
        conn.commit()
        conn.close()
        return {"status": "Success"}
    

class Badword_Logic:
    def __init__(self, sensor_instance):
        self.sensor = sensor_instance

    def get_badwords_logic(self):
        res = get_badwords()
        return [Badwords.convert(row) for row in res]
    
    def get_badwords_paginated_logic(self):
        res = get_badwords_paginated()
        return [Badwords.convert(row) for row in res]
    
    def create_badword_logic(self, word):
        if not word or not word.strip():
            return {
                "status": "Error",
                "message": ("Error", "Data tidak boleh kosong")
            }
        
        res = create_badwords(word.strip().lower())

        if res == "word_exist":
            return {
                "status": "Error",
                "message": ("Error", "Data sudah ada, silakan masukkan data lain")
            }
                
        self.sensor.refresh_badwords_cache()

        return {
            "status": "Success",
            "message": ("Success", "Kata berhasil ditambahkan"),
        }
    
    def update_badword_logic(self, id_badword, word):
        if not word or not word.strip():
            return {
                "status": "Error",
                "message": ("Error", "Data tidak boleh kosong")
            }
        
        res = update_badwords(id_badword, word.strip().lower())

        if res == "word_exist":
            return {
                "status": "Error",
                "message": ("Error", "Data sudah ada, silakan masukkan data lain")
            }
                
        self.sensor.refresh_badwords_cache()

        return {
            "status": "Success",
            "message": ("Success", "Data berhasil diedit"),
        }
    
    def delete_badword_logic(self, id_badword):        
        res = delete_badword(id_badword)
                
        if not res:
            return {
                "status": "Error",
                "message": ("Error", "Gagal menghapus data dari database")
            }

        self.sensor.refresh_badwords_cache()

        return {
            "status": "Success",
            "message": ("Success", "Data berhasil dihapus"),
        }
        
    
class Sensor_Logic:
    def __init__(self):
        self.bad_words_cache = self.get_badwords_sensor_logic()

    def get_badwords_sensor_logic(self):
        bad_words_set = set()
        res = get_badwords()  # Disarankan menggunakan fungsi khusus agar sinkron
        for row in res:
            badword_dict = Badwords.convert(row)
            kata = badword_dict.word.strip().lower()
            bad_words_set.add(kata)
        return bad_words_set
        
    def sensor_teks(self, teks, user_id):
        if not teks:
            return teks
            
        kata_kata = teks.split()
        is_dirty = False  # Perbaikan: Menggunakan variabel lokal agar thread-safe
        
        for i, kata in enumerate(kata_kata):
            kata_bersih = "".join(char for char in kata if char.isalnum()).lower()
            
            if kata_bersih in self.bad_words_cache:
                sensor = "*" * len(kata_bersih)
                kata_kata[i] = kata.lower().replace(kata_bersih, sensor)
                is_dirty = True

        if is_dirty:
            create_logs_user(user_id)
        
        return " ".join(kata_kata)
        
    def refresh_badwords_cache(self):
        self.bad_words_cache = self.get_badwords_sensor_logic()