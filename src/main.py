"""
Main server to answer requests
"""

import hashlib
import http.server
import asyncio
import time
from urllib.parse import parse_qs
from DBServiceInterface import DbServiceI
from controller import Controller
from envs import env, static_dir
from DBService import DBService


sessions = {}

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP server request handler to take care of all GET and POST queries to the website"""


    def __init__(self, *args, db=None, **kwargs):
        self.controller = Controller(db)
        super().__init__(*args, **kwargs)


    def do_GET(self):
        """Handle register GET queries"""
        if self.path == "/":
            session_id = self.get_session_id()
            template = env.get_template('index.html')
            if session_id and session_id in sessions:
                user_email = sessions[session_id]['email']
                content = template.render(email = user_email)
            else:
                content = template.render()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())
        elif self.path == "/register":
            self.get_register_page()
        elif self.path == "/profile":
            self.get_profile_page()
        elif self.path == "/login":
            self.get_login_page()
        elif self.path == "/all":
            asyncio.run(self.get_all_page())
        elif self.path == "/logout":
            session_id = self.get_session_id()
            if session_id in sessions:
                del sessions[session_id]
            self.send_response(302)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", "session_id=; Max-Age=0; Path=/")
            self.end_headers()
        elif self.path.startswith("/static/"):
            file_path = static_dir / self.path[len("/static/"):]
            if file_path.exists() and file_path.is_file():
                if self.path.endswith(".css"):
                    self.send_response(200)
                    self.send_header("Content-type", "text/css")
                    self.end_headers()
                    with open(file_path, "rb") as f:
                        self.wfile.write(f.read())
                else:
                    return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def get_profile_page(self, errors=""):
        """Render proifle page for GET query"""
        template = env.get_template('profile.html')
        content = template.render(error_message = errors)
        self.send_200_header(content)

    def get_register_page(self, error_message=""):
        """Render register page for GET query"""
        template = env.get_template('register.html')
        content = template.render(error_message)
        self.send_200_header(content)

    def get_login_page(self, error_message=""):
        """Render login page for GET query"""
        template = env.get_template('login.html')
        content = template.render(error_message)
        self.send_200_header(content)

    async def get_all_page(self):
        """Render get_all page for GET query"""
        template = env.get_template('all.html')
        users = await self.controller.get_all_users()
        content = template.render(users = users)
        self.send_200_header(content)

    def send_200_header(self, content):
        """Send all headers and content for 200"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())


    def do_POST(self):
        """Handle all POST queries"""
        if self.path == "/login":
            asyncio.run(self.post_login())
        elif self.path == "/register":
            asyncio.run(self.post_register())
        elif self.path == "/profile":
            asyncio.run(self.post_profile_update())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Where are you going!</h1>")

    async def post_login(self):
        """Handle login POST queries"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode())
        (status, errors) = await self.controller.login_user(data.get("email")[0],
                                                             data.get("password")[0])
        template = None
        content = None
        if status is True:
            session_id = self.generate_session_id(data.get("email")[0])
            sessions[session_id] = {"email": data.get("email")[0], "created_at": time.time()}
            self.send_response(302)
            self.send_header("Set-Cookie", f"session_id={session_id}; HttpOnly; Path=/")
            template = env.get_template('index.html')
            content = template.render(email = sessions[session_id]['email'])
        else:
            template = env.get_template('login.html')
            content = template.render(error_message = errors)
            self.send_response(200)
        
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    async def post_register(self):
        """Handle register POST queries"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode())

        (status, errors) = await self.controller.register_user(data.get("first_name")[0],
                                                                data.get("last_name")[0],
                                                                data.get("email")[0],
                                                                data.get("password")[0],
                                                                data.get("confirm_password")[0])
        template = None
        content = None
        if status:
            template = env.get_template('login.html')
            content = template.render()
            self.send_response(302)
        else:
            template = env.get_template('register.html')
            content = template.render(error_message = errors)
            self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    async def post_profile_update(self):
        """Handle profile_update POST queries"""
        session_id = self.get_session_id()
        if session_id is None:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Where are you going!</h1>")

        user_email = sessions[session_id]['email']
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = parse_qs(post_data.decode())

        first_name = ""
        last_name = ""
        password = ""

        if data.get("first_name"):
            first_name = data.get("first_name")[0]
        if data.get("last_name"):
            last_name = data.get("last_name")[0]
        if data.get("password"):
            password = data.get("password")[0]
        (status, errors) = await self.controller.update_user(first_name, last_name,
                                                   password, user_email)
        template = None
        content = None
        if status:
            template = env.get_template('index.html')
            content = template.render(email = user_email)
            self.send_response(302)
        else:
            template = env.get_template('profile.html')
            content = template.render(error_message = errors)
            self.send_response(200)
        
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())


    def get_session_id(self):
        """Gets session from current user"""
        if "Cookie" in self.headers:
            cookies = self.headers["Cookie"]
            for cookie in cookies.split(";"):
                key, value = cookie.strip().split("=")
                if key == "session_id":
                    return value
        return None
    
    def generate_session_id(self, email):
        """Generate session id"""
        return hashlib.sha256(f"{email}{time.time()}".encode()).hexdigest()
    
def create_handler_with_db(db : DbServiceI):
    """Add db to the http server"""
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, db=db, **kwargs)

    return Handler

def main():
    """Main function to start the server"""
    server_address = ("", 8000)
    db: DbServiceI = DBService("small_db.db")
    asyncio.run(db.create_tables())
    handler_with_db = create_handler_with_db(db)
    httpd = http.server.HTTPServer(server_address, handler_with_db)
    print("Server running on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
