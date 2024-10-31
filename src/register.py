
from templates import env
from DBService import Db
import urllib.parse

async def register(scope, receive, send):
    
    register_template = env.get_template("register.html")
    register_content = register_template.render()

    method = scope['method']
    path = scope['path']

    if method == "GET":
        await GET_register(scope, receive, send)
    elif method == 'POST':
        print("You called post")
        await POST_register(scope, receive, send)
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
    
async def GET_register(scope, receive, send):
    register_template = env.get_template("register.html")
    register_content = register_template.render()

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/html'],
        ],
        })
    await send({
            'type': 'http.response.body',
            'body': register_content.encode("utf-8"),
        })   
    
async def POST_register(scope, receive, send):
    print("You called post")

    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get("body")
        more_body = message.get("more_body", False)

    form_data = urllib.parse.parse_qs(body.decode())
    first_name = form_data.get("first_name")[0]
    last_name = form_data.get("last_name")[0]
    email = form_data.get("email")[0]
    password = form_data.get("password")[0]
    confirm_password = form_data.get("confirm_password")[0]
    # Check if password are the same and hash it

    return_result = f"Hi, {first_name} {last_name}"

    if await Db.register_user(first_name, last_name, email, password):
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
            'body': "Email is already used".encode("utf-8"),
        })