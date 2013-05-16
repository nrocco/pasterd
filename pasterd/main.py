


def main():
    import os
    from pycli_tools.parsers import get_argparser

    from pasterd import __version__
    from pasterd.webserver import run_server

    parser = get_argparser(prog='pasterd', version=__version__,
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
    base_url = args.base_url or 'http://%s:%s' % (host, port)

    if not os.path.isfile(args.database):
        print 'Doing create table now'
        import sqlite3
        conn = sqlite3.connect(args.database)
        c = conn.cursor()
        c.execute('''CREATE TABLE pastes (id VARCHAR(8) UNIQUE, ip VARCHAR(15), created VARCHAR(26), content TEXT);''')
        conn.commit()
        conn.close()

    print 'Starting pasterd v%s' % parser.version

    run_server(host=host, port=port, reloader=args.reload,
               database=args.database, arg='p', base_url=base_url)
