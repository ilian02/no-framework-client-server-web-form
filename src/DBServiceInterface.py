"""
Interface for databases
"""

from abc import ABC, abstractmethod

class DbServiceI(ABC):

    def __init__(self):
        pass

    @abstractmethod
    async def create_tables(self):
        """Takes care of table creation if they do not exist"""  

    @abstractmethod
    async def register_user(self, first_name, last_name, email, password):
        """Add new user to the database"""

    @abstractmethod
    async def login_user(self, email, password):
        """Looks for user with email and password in the database"""

    @abstractmethod
    async def get_users(self):
        """Returns all users"""

    @abstractmethod
    async def update_user(self, first_name, last_name, email, password):
        """Updates user by email"""

    @abstractmethod
    async def get_user_by_id(self, id):
        """Gets user by id"""   

    @abstractmethod
    async def get_user_by_email(self, email):
        """Gets user by email"""
