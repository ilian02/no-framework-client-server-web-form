from pathlib import Path
import random
import string
from urllib.parse import parse_qs, unquote
from DBServiceInterface import DbServiceI
from controller import Controller
from envs import env, static_dir, sessions
from DBService import DBService
import http.server
from http.cookies import SimpleCookie
import asyncio


def generate_session_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def __init__(self, *args, db=None, **kwargs):
        self.controller = Controller(db)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # session_id = self.get_session_id_from_cookies()
        # username = sessions.get(session_id)

        if self.path == "/":
            template = env.get_template('index.html')
            content = template.render()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())

        elif self.path == "/register":
            template = env.get_template('register.html')
            content = template.render()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())

        elif self.path == "/login":
            self.get_login_page()
        
        elif self.path.startswith("/static/"):
            file_path = static_dir / self.path[len("/static/"):]
            print(file_path)
            if file_path.exists() and file_path.is_file():
                if self.path.endswith(".css"):
                    self.send_response(200)
                    self.send_header("Content-type", "text/css")
                    self.end_headers()
                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def get_login_page(self, error_message=""):
        template = env.get_template('login.html')
        content = template.render()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())


    def do_POST(self):
        if self.path == "/login":
            asyncio.run(self.post_login())
        elif self.path == "/register":
            asyncio.run(self.post_register())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Where are you going!</h1>")
            self.wfile.write(b'<a href="/">Page not found</a>')

    async def post_login(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode())
        
        (status, errors) = await self.controller.login_user(data.get("email")[0], data.get("password")[0])
        template = None
        content = None
        if status == True:
            template = env.get_template('index.html')
            content = template.render()
            self.send_response(302)

        else:
            template = env.get_template('login.html')
            content = template.render(error_message = errors)
            self.send_response(200)
            
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    async def post_register(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode())
        
        (status, errors) = await self.controller.register_user(data.get("first_name")[0], data.get("last_name")[0],
                                                    data.get("email")[0], data.get("password")[0],
                                                    data.get("confirm_password")[0])
        template = None
        content = None
        if status:
            template = env.get_template('index.html')
            content = template.render()
            self.send_response(302)
        else:
            template = env.get_template('register.html')
            content = None
            content = template.render(error_message = errors)
            self.send_response(200)
        
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
    
def create_handler_with_db(db : DbServiceI):
    # A wrapper function to return a handler that includes the db
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, db=db, **kwargs)

    return Handler

def main():
    server_address = ("", 8000)
    db: DbServiceI = DBService("small_db.db")
    asyncio.run(db.create_tables())
    handler_with_db = create_handler_with_db(db)
    httpd = http.server.HTTPServer(server_address, handler_with_db)
    print("Server running on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()