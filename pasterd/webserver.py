import random
from datetime import datetime

from bottle import route, run, response, request, install
from bottle_sqlite import SQLitePlugin

from pasterd import VERSION


USAGE = '''
pasterd                                             v %s

NAME
    pasterd - command line paste bin utility


SYNOPSIS
    <command> | curl -F '%s=<-' %s


DESCRIPTION
    Create a paste:
'''



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
    return '%s\n' % request.get('REMOTE_ADDR')


@route('/robots.txt', method='GET', apply=[respond_in_plaintext])
def robots():
    return 'User-agent: *\nDisallow: /'


@route('/', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def index():
    return USAGE % (VERSION, ARG, URL)



@route('/', method='POST', apply=[respond_in_plaintext, catch_exceptions])
def make_paste(db):
    paste = request.params.get(ARG)

    if not paste:
        raise Exception('Usage: send %s POST variable' % ARG)

    ip = request.get('REMOTE_ADDR')
    now = datetime.now()
    paste_id = generate_rand()

    c = db.execute('INSERT INTO pastes VALUES (?,?,?,?)',
                   (paste_id, ip, now, paste))
    db.commit()

    return '%s/%s\n' % (URL, paste_id)



@route('/:paste_id', method='GET', apply=[respond_in_plaintext, catch_exceptions])
def show_paste(db, paste_id):
    c = db.execute('SELECT content FROM pastes WHERE id = ?', (paste_id,))
    paste = c.fetchone()

    if not paste:
        response.status= 404
        return 'Paste %s does not exist' % paste_id

    return '%s' % paste['content']


#
##############################################################################
##############################################################################
#

def main():
    import os
    from pycli_tools.parsers import get_argparser

    parser = get_argparser(prog='pasterd', version=VERSION,
                                 default_config='~/.pasterdrc',
                                 description='Command line paste bin utility')
    parser.add_argument('-b', '--bind', metavar='address:port',
                        default='0.0.0.0:8000', help='Inet socket to bind to')
    parser.add_argument('-u', '--base-url', metavar='http://address:port',
                        help='The base url of this server')
    parser.add_argument('-r', '--reload',
                        action='store_true', help="Auto respawn server")
    parser.add_argument('-d', '--database', default='pastes.sqlite',
                        help='location to the pastes sqlite database')
    args = parser.parse_args()

    parts = args.bind.split(':')
    host = parts[0]
    port = parts[1] if len(parts) > 1 else 8000

    global URL
    URL = args.base_url or 'http://%s:%s' % (host, port)

    global ARG
    ARG = 'p'

    if not os.path.isfile(args.database):
        print 'Doing create table now'
        import sqlite3
        conn = sqlite3.connect(args.database)
        c = conn.cursor()
        c.execute('''CREATE TABLE pastes (id VARCHAR(8) UNIQUE, ip VARCHAR(15), created VARCHAR(26), content TEXT);''')
        conn.commit()
        conn.close()

    print 'Starting pasterd v%s' % VERSION

    install(SQLitePlugin(dbfile=args.database))
    run(host=host, port=port, reloader=args.reload)
