
import urllib
from templates import env
from DBService import Db


async def login(scope, receive, send):
    
    register_template = env.get_template("register.html")
    register_content = register_template.render()

    method = scope['method']
    path = scope['path']

    if method == "GET":
        await GET_login(scope, receive, send)
    elif method == 'POST':
        print("You called post")
        await POST_login(scope, receive, send)
    else:
        print("Error")
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [
                [b'content-type', b'text/plane'],
            ],
        })
        await send({
            'type': 'http.response.body',            
            'body': b"Error 404",
        }) 
    
async def GET_login(scope, receive, send):
    login_template = env.get_template("login.html")
    login_content = login_template.render()

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/html'],
        ],
        })
    await send({
            'type': 'http.response.body',
            'body': login_content.encode("utf-8"),
        })   
    
async def POST_login(scope, receive, send):
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body")
        more_body = message.get("more_body", False)

    form_data = urllib.parse.parse_qs(body.decode())
    email = form_data.get("email")[0]
    password = form_data.get("password")[0]

    result = await Db.login_user(email, password)
    
    return_result = f"Hi, {result}"


    if result:
        await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b"text/plane'; charset=utf-8"],            
        ],
        })
        await send({
            'type': 'http.response.body',            
            'body': return_result.encode("utf-8"),
        }) 
    else:
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b"text/plane'; charset=utf-8"],            
            ],
        })
        await send({
            'type': 'http.response.body',            
            'body': "No such user found".encode("utf-8"),
        }) 