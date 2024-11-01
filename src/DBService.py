from DBServiceInterface import DbServiceI
import sqlite3


class DBService(DbServiceI):
    
    def __init__(self, file_name):
        self.file_name = file_name

    async def create_tables(self):
        print("Creating users table")
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            password TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE)     
                            """)
                conn.commit()
        except sqlite3.OperationalError as e:
            print(e)
            return False
                


    async def register_user(self, first_name, last_name, email, password):
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO users(first_name, last_name, email, password)
                               VALUES(?, ?, ?, ?)""", (first_name, last_name, email, password))
                conn.commit()
                print("Registered")
                return (True, cursor.lastrowid)
        except sqlite3.OperationalError as e:
            print(e)
            return (False, ["Email already exists"])


    async def login_user(self, email, password):
        try:
            print(email)
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM users
                               WHERE email = ?
                                """, (email, ))
                
                (ret_id, ret_first_name, ret_last_name, ret_password, ret_email) = cursor.fetchone()
                
                if ret_id is None:
                    return (False, ["Email not found"])

                if password == ret_password:
                    return (True, [ret_id])
                else:
                    return (False, ["Wrong password"])
                    
                
        except sqlite3.OperationalError as e:
            print(e)
            return False

    async def get_users(self):
        pass

    async def get_user_by_id(self, id):
        pass   

    async def create_token(self, user_id):
        pass

    async def check_token(self, token):
        pass
