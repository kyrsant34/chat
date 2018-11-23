import json
from time import time

import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session
from app.settings import logger
from .models import User


def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)

def fill_session(request, user, session):
    session['username'] = user.username
    session['last_visit'] = time()
    redirect(request, 'index')

def convert_json(message):
    return json.dumps({'error': message})


class Login(web.View):

    @aiohttp_jinja2.template('auth/login.html')
    async def get(self):
        return {'router': self.request.app.router}

    async def post(self):
        data = await self.request.post()
        try:
            # no validate sql injection
            user = await User.get_object(username=data['username'], password=data['password'])
            session = await get_session(self.request)
            fill_session(self.request, user, session)
        except Exception as exc:
            raise
            logger.info(f'{exc}')
            redirect(self.request, 'login')


class Register(web.View):

    @aiohttp_jinja2.template('auth/register.html')
    async def get(self):
        return {'router': self.request.app.router}

    async def post(self):
        data = await self.request.post()
        try:
            # no validate sql injection
            user = await User.create_object(username=data['username'], password=data['password'])
            session = await get_session(self.request)
            fill_session(self.request, user, session)
        except Exception as exc:
            raise
            logger.info(f'{exc}')
            redirect(self.request, 'register')


class LogOut(web.View):

    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
        redirect(self.request, 'login')


class UserList(web.View):

    async def get(self):
        users = await User.objects().execute(User.select(User.username).where(User.is_active == True))
        return web.json_response([user.username for user in users])
