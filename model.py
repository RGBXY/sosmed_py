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