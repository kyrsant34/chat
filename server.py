import hashlib

from aiohttp import web

from app.routes import routes
from app.middlewares import authorize
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import jinja2
import aiohttp_jinja2

from app.settings import logger, db, SECRET_KEY

async def on_shutdown(app):
    for ws in app.websockets:
        await ws.close(code=1001, message='Server shutdown')

# Лучше перевести на редис .
middlewares = [
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest())),
    authorize,
]

app = web.Application(middlewares=middlewares)
app.websockets = {}
app.on_cleanup.append(on_shutdown)
app.db = db

for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

logger.debug('Server started...')
web.run_app(app)
logger.debug('Server stopped')
