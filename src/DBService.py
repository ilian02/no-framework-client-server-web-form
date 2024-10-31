from DBServiceInterface import DbServiceInterface
import sqlite3


class DBService(DbServiceInterface):
    
    def __init__(self, file_name):
        self.file_name = file_name

    async def create_tables(self):

        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = self.conn.curson()
                cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY_KEY
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            password TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE     
                            """)
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print(e)
            return False
                


    async def register_user(self, first_name, last_name, email, password, confirm_password):
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = self.conn.curson()
                cursor.execute("""INSERT INTO users(first_name, last_name, email, password)
                               values({first_name}, {last_name}, {email}, {password})""")
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print(e)
            return False


    async def login_user(self, first_name, last_name, email, password, confirm_password):
        pass

    async def get_users(self):
        pass

    async def get_user_by_id(self, id):
        pass   

    async def create_token(self, user_id):
        pass

    async def check_token(self, token):
        pass


Db = DBService("small_db")