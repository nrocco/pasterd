pasterd
=======

A shameless clone of sprung minus the google-app-engine for use in private
networks.

All credit goes to https://github.com/rupa/sprunge

`pasterd` is a simple http webservice just like paste bin.
You can store snippets of text based content using HTTP POST request and share
them with the rest of the world using plaing HTTP GET requests.


installation
------------

You only need to download, install and run `pasterd` on the server side.
Typically you run `pasterd` like any other bottle.py app; on `127.0.0.1`
behind a proxy server such as `nginx` or `apache`.

You can install `pasterd` using pip

    $ pip install -e git+https://github.com/nrocco/pasterd#egg=pasterd-dev


This will install a program `pasterd`

    $ pasterd --help
    usage: pasterd [-h] [-V] [-b address:port] [-u http://address:port] [-r]

    Command line paste bin utility

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -b address:port, --bind address:port
                            Inet socket to bind to
      -u http://address:port, --base-url http://address:port
                            The base url of this server
      -r, --reload          Auto respawn server



usage
-----

After having installed `pasterd` on the server side from any client you can
use e.g. `curl` to send GET and POST requests to `pasterd`.

To get information on how to use `pasterd` do:

    $ curl http://0.0.0.0:8000


To create a paste execute some command and pipe it to curl

    $ <command> | curl -F 'p=<-' http://0.0.0.0:8000


For example

    $ cat ~/.vimrc | curl -F 'p=<-' http://0.0.0.0:8000


