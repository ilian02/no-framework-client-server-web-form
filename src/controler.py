

import DBServiceInterface


class Controler:
    def __init__(self, db: DBServiceInterface):
        self.dbService = db

    def login_user(self, email, password):
        print("Logging in")
        
        print(email, password)

        return (False, ["Email not found"])