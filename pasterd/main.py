# -*- coding: utf-8 -*-
import logging



log = logging.getLogger(__name__)


def main():
    from pycli_tools.parsers import get_argparser
    from pasterd import webserver, __version__

    parser = get_argparser(prog='pasterd', version=__version__,
                                 default_config='~/.pasterdrc',
                                 description='Command line paste bin utility')
    parser.add_argument('-b', '--bind', metavar='address:port',
                        default='0.0.0.0:8000', help='Inet socket to bind to')
    parser.add_argument('-u', '--base-url', metavar='http://address:port',
                        help='The base url of this server')
    parser.add_argument('-r', '--reload',
                        action='store_true', help="Auto respawn server")
    parser.add_argument('-d', '--database', default='/tmp/pastes.sqlite',
                        help='location to the pastes sqlite database')
    parser.add_argument('-p', '--paste-variable', default='p')
    args = parser.parse_args()

    parts = args.bind.split(':')
    host = parts[0]
    port = parts[1] if len(parts) > 1 else 8000
    base_url = args.base_url or 'http://%s:%s' % (host, port)

    log.warn('Starting pasterd v%s', __version__)
    webserver.setup(args.database, base_url, args.paste_variable)
    webserver.run(host=host, port=port, reloader=args.reload)
