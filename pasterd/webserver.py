# -*- coding: utf-8 -*-
import logging
import os
import random
import base64

from mimetypes import MimeTypes
from datetime import datetime

import bottle
from bottle_sqlite import SQLitePlugin

from pasterd import __version__, __usage__



log = logging.getLogger(__name__)
VAR = 'p'
URL = 'http://0.0.0.0'


def generate_rand(size=8):
    chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(chars) for x in range(size))


def catch_exceptions(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            bottle.response.status= 400
            return '%s: %s\n' % (type(e).__name__, str(e))
    return wrapper


def respond_in_plaintext(fn):
    def wrapper(*args, **kwargs):
        bottle.response.content_type = 'text/plain; charset="UTF-8"'
        return fn(*args, **kwargs)
    return wrapper


#
##############################################################################
##############################################################################
#


@bottle.route('/ip', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def ip():
    return '%s\n' % bottle.request.get('REMOTE_ADDR')


@bottle.route('/robots.txt', method='GET', apply=[respond_in_plaintext])
def robots():
    return 'User-agent: *\nDisallow: /'


@bottle.route('/', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def index():
    return __usage__ % (__version__, VAR, URL)


@bottle.route('/', method='POST', apply=[respond_in_plaintext, catch_exceptions])
def make_paste(db):
    db.text_factory = str

    if VAR in bottle.request.files:
        upload = bottle.request.files.get(VAR)
        name, ext = os.path.splitext(upload.filename)

        if ext not in ('.png','.jpg','.jpeg'):
            raise Exception('File extension not allowed.')

        mime = MimeTypes()
        mime_type = mime.guess_type(upload.filename)
        content_type = mime_type[0]
        paste = base64.b64encode(upload.file.read())
    elif VAR in bottle.request.params:
        content_type = "text/plain"
        paste = bottle.request.params.get(VAR)
    else:
        raise Exception('Usage: send %s POST variable' % VAR)

    ip = bottle.request.get('REMOTE_ADDR')
    now = datetime.now()
    paste_id = generate_rand()

    c = db.execute('INSERT INTO pastes VALUES (?,?,?,?,?)',
                   (paste_id, ip, now, content_type, paste))
    db.commit()

    return '%s/%s\n' % (URL, paste_id)


@bottle.route('/:paste_id', method='GET', apply=[catch_exceptions])
def show_paste(db, paste_id):
    c = db.execute('SELECT type, content FROM pastes WHERE id = ?', (paste_id,))
    paste = c.fetchone()

    if not paste:
        bottle.response.status= 404
        return 'Paste %s does not exist' % paste_id

    if "text/plain" != paste['type']:
        content = base64.b64decode(paste['content'])
    else:
        content = paste['content']

    bottle.response.content_type = paste['type']
    return '%s' % content


#
##############################################################################
##############################################################################
#


def setup(db, base_url=URL, paste_variable=VAR):
    global URL, VAR
    URL = base_url
    VAR = paste_variable

    log.warn('Using sqlite database in %s', db)
    if not os.path.isfile(db):
        import sqlite3
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS pastes (id VARCHAR(8) UNIQUE, ip VARCHAR(15), created VARCHAR(26), type VARCHAR(50), content TEXT);''')
        conn.commit()
        conn.close()
    bottle.install(SQLitePlugin(dbfile=db))


def run(host, port, reloader):
    return bottle.run(host=host, port=port, reloader=reloader)
