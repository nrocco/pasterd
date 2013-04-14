#!/usr/bin/env python

import random

from bottle import route, run, response, request, install
from bottle_sqlite import SQLitePlugin




DBNAME='pastes.sqlite'
URL='http://0.0.0.0:8000'
ARG='p'

USAGE = '''\
paster.py                                           v 1.0

NAME
    paster - command line paste bin utility


SYNOPSIS
    <command> | curl -F '%s=<-' %s


DESCRIPTION
    Create a paste:
''' % (ARG, URL)



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




install(SQLitePlugin(dbfile=DBNAME))


@route('/', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def index():
    return USAGE



@route('/', method='POST', apply=[respond_in_plaintext]) #, catch_exceptions])
def make_paste(db):
    paste = request.params.get(ARG)
    if not paste:
        raise Exception('Usage: send %s POST variable' % ARG)

    paste_id = generate_rand()

    c = db.execute('INSERT INTO pastes VALUES (?,?)', (paste_id, paste))
    db.commit()

    return '%s/%s\n' % (URL, paste_id)



@route('/:paste_id', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def show_paste(db, paste_id):
    c = db.execute('SELECT * FROM pastes where id = ?', (paste_id,))
    paste = c.fetchone()

    if not paste:
        raise Exception('Paste %s does not exist' % paste_id)

    return '%s' % paste['content']






if '__main__' == __name__:
    import sys
    import os

    if not os.path.isfile(DBNAME):
        print 'Doing create table now'
        import sqlite3
        conn = sqlite3.connect(DBNAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE pastes (id VARCHAR(8) UNIQUE, content TEXT);''')
        conn.commit()
        conn.close()

    if len(sys.argv) == 2 and 'devel' == sys.argv[1]:
        run(host='0.0.0.0', port=8000, reloader=True)
    else:
        run(host='0.0.0.0', port=8000)

