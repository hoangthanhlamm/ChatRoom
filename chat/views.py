import logging
from datetime import datetime
from time import time

import aiohttp_jinja2
import bcrypt
from aiohttp import web, WSMsgType
from aiohttp_session import get_session

from errors import *
from mongo_connect import Account, Message

history = []
offset = 0
max_msg = 20


class Login(web.View):
    @aiohttp_jinja2.template('chat/login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'room_chat')
        return None

    async def post(self):
        body = await self.request.post()
        data = {
            "username": body.get('username'),
            "password": body.get('password')
        }

        acc = Account()
        username = data['username']
        user = await acc.get_user(username)
        if user is None:
            return web.Response(text='User does not exists')

        password = bytes(data['password'], 'utf-8')
        hash_password = user['hash_password']
        if not bcrypt.checkpw(password, bytes.fromhex(hash_password)):
            return web.Response(text='Wrong password')

        session = await get_session(self.request)
        _session = json.dumps({"username": username})
        logging.info(_session)
        set_session(session, _session)

        redirect(self.request, 'room_chat')


class CreateUser(web.View):
    @aiohttp_jinja2.template('chat/create_user.html')
    async def get(self):
        return None

    async def post(self):
        body = await self.request.post()
        data = {
            "username": body.get('username'),
            "password": body.get('password'),
            "email": body.get('email')
        }
        required_fields = ['username', 'password', 'email']
        validate_fields(required_fields, data)

        acc = Account()
        username = data['username']
        check = await acc.get_user(username)
        if check is not None:
            return web.Response(text='User already exists')

        password = data['password']
        hashed_password = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

        result = await acc.create_user({
            "username": username,
            "hash_password": hashed_password.hex(),
            "email": data['email'],
        })
        redirect(self.request, 'room_chat')


class Logout(web.View):
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
        redirect(self.request, 'homepage')


class RoomChat(web.View):
    @aiohttp_jinja2.template('chat/room_chat.html')
    async def get(self):
        session = await get_session(self.request)
        if not session.get('user'):
            redirect(self.request, 'homepage')

        message = Message()
        messages = await message.load_msg(max_msg)
        history.clear()
        for msg in messages:
            history.append({
                "time": datetime.strptime(str(msg['time']), '%Y-%m-%d %H:%M:%S.%f'),
                "sender": msg['sender'],
                "msg": msg['msg']
            })
        return {"messages": history}


class WebSocket(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        session = await get_session(self.request)
        message = Message()
        _user = session.get('user')
        # logging.info(_user)
        user = json.loads(_user)
        # logging.info(user)
        username = user.get('username')

        for _ws in self.request.app['websockets']:
            await _ws.send_str('%s joined' % username)
        self.request.app['websockets'].append(ws)

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                time_chat = datetime.now()
                _message = {
                    "time": time_chat,
                    "sender": username,
                    "msg": msg.data
                }
                await message.save_msg(_message)
                if len(history) > max_msg:
                    del history[0]
                history.append(_message)
                logging.info(_message)

                for _ws in self.request.app['websockets']:
                    await _ws.send_str('(%s) %s' % (username, msg.data))

            elif msg.type == WSMsgType.ERROR:
                logging.debug('ws connection closed with exception %s' % ws.exception())

        self.request.app['websockets'].remove(ws)
        for _ws in self.request.app['websockets']:
            await _ws.send_str('%s disconnected' % username)
        logging.debug('websocket connection close')
        return ws


async def load_msg():
    if not history:
        message = Message()
        messages = await message.load_msg(max_msg)
        for msg in messages:
            history.append({
                "time": datetime.strptime(msg['time'], '%Y-%m-%d %H:%M:%S.%f'),
                "user": msg['sender'],
                "msg": msg['msg']
            })


def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)


def set_session(session, user_id):
    session['user'] = str(user_id)
    session['last_visit'] = time()


def convert_json(message):
    return json.dumps({'error': message})


def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise ApiBadRequest("'{}' parameter is required".format(field))
