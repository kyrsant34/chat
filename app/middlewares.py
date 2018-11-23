from aiohttp import web
from aiohttp.web import middleware
from aiohttp_session import get_session
from .routes import routes

@middleware
async def authorize(request, handler):
    def check_path(path):
        result = False
        for r in routes:
            if path.startswith(r[1]):
                result = True
                break
        return result

    # jwt ты ли это)
    session = await get_session(request)
    request.username = session.get('username')
    if request.username or request.path.startswith('/login/') or request.path.startswith('/register/'):
        return await handler(request)
    elif check_path(request.path):
        url = request.app.router['login'].url_for()
        raise web.HTTPFound(url)
    else:
        return web.HTTPNotFound()
