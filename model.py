class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        
    @staticmethod
    def convert(data):
        return User(data["id"], data["username"], data["password"], data["role"])