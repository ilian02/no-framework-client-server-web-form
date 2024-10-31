
from templates import env


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
    print("You called post")
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plane'],            
        ],
    })
    await send({
        'type': 'http.response.body',            
        'body': b"Put request",
    }) 