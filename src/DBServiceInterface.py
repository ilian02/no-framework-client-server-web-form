from abc import ABC, abstractmethod

class DBServiceInterafe(ABC):

    @abstractmethod
    async def register_user(first_name, last_name, email, password, confirm_password):
        pass

    @abstractmethod
    async def login_user(first_name, last_name, email, password, confirm_password):
        pass

    @abstractmethod
    async def create_token(user_id):
        pass

    @abstractmethod
    async def check_token(token):
        pass