from aiohttp import web
from chat.views import Login, CreateUser, Logout, RoomChat

routes = [
    web.get('/', Login, name="homepage"),
    web.post('/login', Login, name="login"),
    web.get('/create_user', CreateUser, name="create_user"),
    web.post('/create_user', CreateUser),
    web.get('/logout', Logout, name='logout'),
    web.get('/room_chat', RoomChat, name='room_chat')
]