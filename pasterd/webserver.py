# -*- coding: utf-8 -*-
import random
from datetime import datetime

from bottle import route, run, response, request, install
from bottle_sqlite import SQLitePlugin

from pasterd import __version__, __usage__



def generate_rand(size=8):
    chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for x in range(size))


def catch_exceptions(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            response.status= 400
            return '%s: %s\n' % (type(e).__name__, str(e))
    return wrapper


def respond_in_plaintext(fn):
    def wrapper(*args, **kwargs):
        response.content_type = 'text/plain; charset="UTF-8"'
        return fn(*args, **kwargs)
    return wrapper


#
##############################################################################
##############################################################################
#


@route('/ip', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def ip():
    return u'%s\n' % request.get('REMOTE_ADDR')


@route('/robots.txt', method='GET', apply=[respond_in_plaintext])
def robots():
    return u'User-agent: *\nDisallow: /'


@route('/', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def index():
    return __usage__ % (__version__, ARG, URL)


@route('/', method='POST', apply=[respond_in_plaintext, catch_exceptions])
def make_paste(db):
    db.text_factory = str
    paste = request.params.get(ARG)

    if not paste:
        raise Exception('Usage: send %s POST variable' % ARG)

    ip = request.get('REMOTE_ADDR')
    now = datetime.now()
    paste_id = generate_rand()

    c = db.execute(u'INSERT INTO pastes VALUES (?,?,?,?)',
                   (paste_id, ip, now, paste))
    db.commit()

    return '%s/%s\n' % (URL, paste_id)


@route('/:paste_id', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def show_paste(db, paste_id):
    c = db.execute(u'SELECT content FROM pastes WHERE id = ?', (paste_id,))
    paste = c.fetchone()

    if not paste:
        response.status= 404
        return 'Paste %s does not exist' % paste_id

    return '%s' % paste['content']


#
##############################################################################
##############################################################################
#


def run_server(host, port, database, base_url, arg='p', reloader=False):
    global URL, ARG
    URL = base_url
    ARG = arg
    install(SQLitePlugin(dbfile=database))
    run(host=host, port=port, reloader=reloader)
