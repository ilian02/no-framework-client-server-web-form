
import uvicorn
from register import register
from login import login
from templates import env, static_dir
import mimetypes
from DBService import Db
import asyncio

async def app(scope, receive, send):
    assert scope['type'] == 'http'

    path = scope['path']

    if path == '/register':
        await register(scope, receive, send) 
    elif path == '/login':
        await login(scope, receive, send)
    elif path == '/':
        template = env.get_template("index.html")
        content = template.render()

        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/html'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': content.encode("utf-8"),
        })
    elif scope['path'].startswith("/static/"):
        file_path = static_dir / scope['path'][len("/static/"):]
        if file_path.exists() and file_path.is_file():
            content_type, _ = mimetypes.guess_type(str(file_path))
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    (b"content-type", content_type.encode() if content_type else b"text/plain"),                    ],
                })
            with file_path.open("rb") as f:
                await send({
                    "type": "http.response.body",
                    "body": f.read(),
                })
    else:
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Why are you here',
        })


async def main():
    await Db.create_tables()
    uvicorn.run("main:app", reload=True, port=8080, log_level="info")

if __name__ == "__main__":
    asyncio.run(main())