class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        
    @staticmethod
    def convert(data):
        return User(data["id"], data["username"], data["password"], data["role"])
    
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
    def __init__(self, id, content, created_at, username, user_role, comunity_name, total_likes, is_liked_by_me, is_saved_by_me):
        self.id = id
        self.content = content
        self.created_at = created_at
        self.username = username
        self.user_role = user_role
        self.comunity_name = comunity_name
        self.total_likes = total_likes
        self.is_liked_by_me = is_liked_by_me
        self.is_saved_by_me = is_saved_by_me

    @staticmethod
    def convert(data):
        return Post(
            data["id"],
            data["content"],
            data["created_at"],
            data["username"],
            data["user_role"],
            data["comunity_name"],
            data["total_likes"],
            data["is_liked_by_me"],
            data["is_saved_by_me"]
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