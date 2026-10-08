
from models import user

class Admin (user.User):

    def role(self)-> str:
        return "admin"