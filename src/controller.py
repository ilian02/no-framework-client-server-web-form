from DBServiceInterface import DbServiceI


class Controller:
    def __init__(self, db: DbServiceI):
        self.dbService = db

    async def login_user(self, email: str, password: str):

        errors = []
        if "@" not in email:
            errors.insert(0, "Email must contain @")

        if password.strip() == "":
            errors.insert(0, "Password cannot be empty")

        (login_result, output) = await self.dbService.login_user(email, password)
        match login_result:
            case True:
                self.id = output[0]
            case False:
                errors.insert(0, "Incorrect password")
        
        if len(errors) != 0:
            return (False, errors)
        else:
            return (True, [])
    
    async def register_user(self, first_name: str, last_name: str, email: str
                            , password: str, confirm_password: str):

        errors = []
        if "@" not in email:
            errors.insert(0, "Email must contain @")

        if first_name.strip() == "":
            errors.insert(0, "First name cannot be empty")

        if last_name.strip() == "":
            errors.insert(0, "Last name cannot be empty")

        if email.strip() == "":
            errors.insert(0, "Email cannot be empty")

        if password.strip() == "" or len(password) < 5:
            errors.insert(0, "Password cannot be empty and it must be at least 6 symbols")

        if confirm_password.strip() == "":
            errors.insert(0, "Confirm Password cannot be empty")

        if confirm_password != password:
            errors.insert(0, "Password and Confirm Password do not match")


        if len(errors) != 0:
            return (False, errors)
        else:
            (register_result, reg_errors) = await self.dbService.register_user(first_name, last_name, email, password)
            if register_result is False:
                errors.insert(0, reg_errors)
                return (False, errors)
            else:
                print(f"Registered in as {errors}")
                return (True, [])
    
    async def get_all_users(self):
        (status, result) = await self.dbService.get_users()
        if status:
            return result
        else:
            return (False, ["Error getting users from DB"])

    async def update_user(self, first_name, last_name, password, email):
        (result, user) = await self.dbService.get_user_by_email(email)
        if result == False:
            return (False, ["Error finding user with this email"])
        
        new_fn = user[1]
        new_ln = user[2]
        new_pass = user[3]

        errors = []
        if len(password) < 5 and password != "":
            errors.insert(0, "Password cannot be less than 6 symbols")
            return (False, errors)

        if first_name != "":
            new_fn = first_name
        if last_name != "":
            new_ln = last_name
        if password != "":
            new_pass = password


        (result, output) = await self.dbService.update_user(new_fn, new_ln, email, new_pass)

        if result:
            return (True, [])
        else:
            return (False, output)