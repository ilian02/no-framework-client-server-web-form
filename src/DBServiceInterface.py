from abc import ABC, abstractmethod

class DbServiceI(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def create_tables(self):
        pass    

    @abstractmethod
    async def register_user(self, first_name, last_name, email, password):
        pass

    @abstractmethod
    async def login_user(self, email, password):
        pass
    
    @abstractmethod
    async def get_users(self):
        pass

    @abstractmethod
    async def update_user(self, first_name, last_name, email, password):
        pass

    @abstractmethod
    async def get_user_by_id(self, id):
        pass    

    @abstractmethod
    async def get_user_by_email(self, email):
        pass