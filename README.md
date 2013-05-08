pasterd
=======

A shameless clone of sprung minus the google-app-engine for use in private
networks.

All credit goes to https://github.com/rupa/sprunge



installation
------------

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

To get information on how to use `pasterd` do:

    $ curl http://0.0.0.0:8000


To create a paste execute some command and pipe it to curl

    $ <command> | curl -F 'p=<-' http://0.0.0.0:8000


For example

    $ cat ~/.vimrc | curl -F 'p=<-' http://0.0.0.0:8000


