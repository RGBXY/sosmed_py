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
    def __init__(self, id, content, created_at, username=None, user_role=None, comunity_name=None):
        self.id = id
        self.content = content
        self.created_at = created_at

        self.username = username
        self.user_role = user_role
        self.comunity_name = comunity_name

    @staticmethod
    def convert(data):
        return Post(
            data["id"],
            data["content"],
            data["created_at"],
            data["username"],
            data["user_role"],
            data["comunity_name"]
        )
