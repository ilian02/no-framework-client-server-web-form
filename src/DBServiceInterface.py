from abc import ABC, abstractmethod

class DbServiceInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def create_tables(self, first_name, last_name, email, password, confirm_password):
        pass    

    @abstractmethod
    async def register_user(self, first_name, last_name, email, password, confirm_password):
        pass

    @abstractmethod
    async def login_user(self, first_name, last_name, email, password, confirm_password):
        pass
    
    @abstractmethod
    async def get_users(self):
        pass

    @abstractmethod
    async def get_user_by_id(self, id):
        pass    

    @abstractmethod
    async def create_token(self, user_id):
        pass

    @abstractmethod
    async def check_token(self, token):
        pass