import sys
import asyncio
import logging

from aiohttp import web
import jinja2
import aiohttp_jinja2 as jtemplate
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from routes import routes
import mongo_connect
import settings

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(funcName)s :'
                           ' line %(lineno)d :: %(message)s', level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def start_server(host, port):
    app = web.Application()

    app['secret_key'] = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    app['private_key'] = 'ab0880a6a9b593b6b4dfb23b842716f5777ff8656df940f137b00cc3ed76be2d'
    app['websockets'] = []
    setup(app, EncryptedCookieStorage(bytes(app['secret_key'], 'utf-8')))

    app.add_routes(routes)
    app.router.add_static('/static', settings.STATIC_PATH, name='static')
    app.router.add_static('/media', settings.MEDIA_PATH, name='media')
    jtemplate.setup(app, loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH))

    logging.info('Starting Company Api on %s:%s', host, port)
    web.run_app(
        app,
        host=host,
        port=port,
        access_log=LOGGER,
        access_log_format='%r: %s status, %b size, in %Tf s'
    )


def main():
    # init_db = database.InitDB()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(init_db.create_db())

    try:
        start_server('localhost', 8096)
    except Exception as err:
        logging.error(err)
        sys.exit(1)
    # finally:
    #     database.conn.close()


if __name__ == '__main__':
    main()
