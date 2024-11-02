"""
Database service that implements DBServiceI interface to work with sqlite3 db
"""

from db_service_interface import DbServiceI
import sqlite3
import bcrypt


class DbService(DbServiceI):
    
    def __init__(self, file_name):
        self.file_name = file_name

    async def create_tables(self):
        """Creates dababase and tables if not existing"""

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
        """Tries to add user to db"""
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""SELECT id FROM USERS WHERE EMAIL = ?""", (email, ))
                result = cursor.fetchone()
                if result is not None:
                    return (False, "Email already exists")

                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode(), salt)

                cursor.execute("""INSERT INTO users(first_name, last_name, email, password)
                               VALUES(?, ?, ?, ?)""", (first_name, last_name, email, hashed_password))
                conn.commit()
                return (True, cursor.lastrowid)
        except sqlite3.OperationalError as e:
            print(e)
            return (False, "An error has been found")


    async def login_user(self, email, password):
        """Tries to login user"""
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM users
                               WHERE email = ?
                                """, (email, ))
                
                (ret_id, ret_first_name, ret_last_name, ret_password, ret_email) = cursor.fetchone()
                
                if ret_id is None:
                    return (False, ["Email not found"])

                if bcrypt.checkpw(password.encode(), ret_password):
                    return (True, [ret_id])
                else:
                    return (False, ["Wrong password"])
                    
                
        except sqlite3.OperationalError as e:
            print(e)
            return False

    async def get_users(self):
        """Gets all users from db"""
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM users""")
                users = cursor.fetchall()
                return (True, users)
        except sqlite3.OperationalError as e:
            print(e)
            return (False, ["Error getting users from database"])

    async def get_user_by_id(self, id):
        """Gets user by id"""
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM users
                                WHERE id = ?""", (id, ))
                user = cursor.fetchone()
                return (True, user)
        except sqlite3.OperationalError as e:
            print(e)
            return (False, ["Error getting users from database"])
        
    async def get_user_by_email(self, email):
        """Gets user by email"""
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""SELECT * FROM users
                                WHERE email = ?""", (email, ))
                user = cursor.fetchone()
                return (True, user)
        except sqlite3.OperationalError as e:
            print(e)
            return (False, ["Error getting user from database"])

    async def update_user(self, first_name, last_name, email, password):
        """Updates user information"""
        try:
            with sqlite3.connect(self.file_name) as conn: 
                cursor = conn.cursor()
                cursor.execute("""UPDATE users
                                SET first_name = ?, last_name = ?, password = ?
                                WHERE email = ?""", (first_name, last_name, password, email))
                return (True, [])
        except sqlite3.OperationalError as e:
            print(e)
            return (False, ["Something is wrong"])
