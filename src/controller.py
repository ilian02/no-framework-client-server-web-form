

from DBServiceInterface import DbServiceI


class Controller:
    def __init__(self, db: DbServiceI):
        self.dbService = db

    async def login_user(self, email: str, password: str):
        print("Logging in")
        
        errors = []
        if "@" not in email:
            errors += "Email must contain @"

        if password.strip() == "":
            errors += "Password cannot be empty"

        (login_result, output) = await self.dbService.login_user(email, password)
        match login_result:
            case True:
                self.id = output[0]
            case "Email not found":
                errors += "An account with this password does not exist"
            case "Wrong password":
                errors += "Password does not match"

        if len(errors) != 0:
            return (False, errors)
        else:
            return (True, [])
    
    async def register_user(self, first_name: str, last_name: str, email: str
                            , password: str, confirm_password: str):

        errors = []
        if "@" not in email:
            errors += "Email must contain @"

        if first_name.strip() == "":
            errors += "First name cannot be empty"

        if last_name.strip() == "":
            errors += "Last name cannot be empty"

        if email.strip() == "":
            errors += "Email cannot be empty"

        if password.strip() == "":
            errors += "Password cannot be empty"

        if confirm_password.strip() == "":
            errors += "Confirm Password cannot be empty"

        if confirm_password != password:
            errors += "Password and Confirm Password do not match"


        if len(errors) != 0:
            return (False, errors)
        else:
            (register_result, errors) = await self.dbService.register_user(first_name, last_name, email, password)
            if register_result == False:
                errors += "Email already exists"
                return (False, errors)
            else:
                print(f"Registered in as {errors}")
                return (True, [])
    
    async def get_all_users(self):
        (status, result) = await self.dbService.get_users()
        if status:
            return result
        else:
            return "Error getting users from DB"
