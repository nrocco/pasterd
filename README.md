pasterd
=======

A shameless clone of sprunge minus the google-app-engine for use in private
networks.
Handy for work if you need to share code or configuration snippets with
collegues.

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

    $ pip install https://github.com/nrocco/pasterd/archive/master.zip#egg=pasterd-dev


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


Start a new instance of `pasterd`:

    $ pasterd -b 127.0.0.1:8000 -u http://pasterd.local

This will start a new instance of `pasterd` running on the loopback interface
on port `8000`. The argument to the `-u` or `--base-url` option is used inside
the help text when you browse to `pasterd` using your favorite browser.

Now you can configure your http proxy server to proxy pass all requests for
`http://pasterd.local` to `127.0.0.1:8000` and you're done.


usage
-----

After having installed `pasterd` on the server side from any client you can
use e.g. `curl` to send GET and POST requests to `pasterd`.

To get information on how to use `pasterd` from the client point of view do:

    $ curl http://pasterd.local


To create a paste execute some command and pipe it to curl

    $ <command> | curl -F 'p=<-' http://pasterd.local


For example

    $ cat ~/.vimrc | curl -F 'p=<-' http://pasterd.local


