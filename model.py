class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        
    @staticmethod
    def convert(data):
        return User(data["id"], data["username"], data["password"], data["role"])
    
class Comunity_Member:
    def __init__(self, id, username, role, joined_at):
        self.id = id
        self.username = username
        self.role = role
        self.joined_at = joined_at

    @staticmethod
    def convert(data):
        if not data:
            return None
            
        return Comunity_Member(
            id=data[0], 
            username=data[1], 
            role=data[2], 
            joined_at=data[3]
        )
    
class Comunity:
    def __init__(self, id, user_id, name, description):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.description = description

    @staticmethod
    def convert(data):
        return Comunity(data["id"], data["user_id"], data["name"], data["description"])
    
class Post:
    def __init__(self, id, user_id, content, created_at, username, user_role, comunity_name, total_likes, is_liked_by_me, is_saved_by_me, follow_status=None):
        self.id = id
        self.user_id = user_id  # Ditambahkan
        self.content = content
        self.created_at = created_at
        self.username = username
        self.user_role = user_role
        self.comunity_name = comunity_name
        self.total_likes = total_likes
        self.is_liked_by_me = is_liked_by_me
        self.is_saved_by_me = is_saved_by_me
        self.follow_status = follow_status  # Ditambahkan (default None jika tidak ada)

    @staticmethod
    def convert(data):
        return Post(
            data["id"],
            data["user_id"],  # Ditambahkan
            data["content"],
            data["created_at"],
            data["username"],
            data["user_role"],
            data["comunity_name"],
            data["total_likes"],
            data["is_liked_by_me"],
            data["is_saved_by_me"],
            data["follow_status"],
        )
    
class Comment:
     def __init__(self, id, user_id, post_id, content, created_at, username):
        self.id = id
        self.user_id = user_id
        self.post_id = post_id
        self.content = content
        self.created_at = created_at
        self.username = username

     @staticmethod
     def convert(data):
        return Comment(
            data["id"],
            data["user_id"],
            data["post_id"],
            data["content"],
            data["created_at"],
            data["username"])

class NotificationData:
    def __init__(self, id, user_id, sender_id, type, message, related_id, is_read, created_at, sender_username=None):
        self.id = id
        self.user_id = user_id
        self.sender_id = sender_id
        self.type = type
        self.message = message
        self.related_id = related_id
        self.is_read = is_read
        self.created_at = created_at
        self.sender_username = sender_username # Opsional untuk mempermudah UI

    @staticmethod
    def convert(data):
        return NotificationData(
            data["id"],
            data["user_id"],
            data["sender_id"],
            data["type"],
            data["message"],
            data["related_id"],
            data["is_read"],
            data["created_at"],
            data["sender_username"] if "sender_username" in data.keys() else None
        )
    
class Badwords:
     def __init__(self, id, word):
        self.id = id
        self.word = word

     @staticmethod
     def convert(data):
        return Badwords(
            data["id"],
            data["word"],
        )