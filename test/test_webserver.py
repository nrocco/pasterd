from os import remove, path
from pasterd import __version__
from pasterd import webserver

import bottle
from bottle_sqlite import SQLitePlugin

from webtest import TestApp



if path.isfile('/tmp/pasterd-test.sqlite'):
    remove('/tmp/pasterd-test.sqlite')
webserver.setup('/tmp/pasterd-test.sqlite')


def test_generate_random_string():
    assert len(webserver.generate_rand()) == 8
    assert '.' not in webserver.generate_rand()


def test_version_number():
    assert __version__ in webserver.index()


def test_robots_txt():
    assert 'Disallow' in webserver.robots()


def test_index():
    app = TestApp(bottle.app())
    resp = app.get('/')
    assert resp.status == '200 OK'
    assert resp.status_int == 200
    assert resp.content_type == 'text/plain'
    assert resp.content_length > 0
    assert __version__ in resp


def test_get_ip():
    app = TestApp(bottle.app())
    resp = app.get('/ip')
    assert resp.status == '200 OK'
    assert resp.status_int == 200
    assert resp.content_type == 'text/plain'
    assert resp.content_length > 0


def test_non_existent_paste_gives_404():
    app = TestApp(bottle.app())
    resp = app.get('/hihaho', status=404)
    assert resp.status == '404 Not Found'
    assert resp.status_int == 404
    assert resp.content_type == 'text/plain'
    assert resp.content_length > 0


def test_make_paste():
    app = TestApp(bottle.app())
    resp = app.post('/', {'p': 'this is a test paste'})
    assert resp.status == '200 OK'
    assert resp.status_int == 200
    assert resp.content_type == 'text/plain'
    assert resp.content_length > 0

    paste_url = resp.body.decode("utf-8").replace(webserver.URL, '').strip()
    resp2 = app.get(paste_url)
    assert resp.status == '200 OK'
    assert resp.status_int == 200
    assert resp.content_type == 'text/plain'
    assert resp.content_length > 0
    assert resp2.body.decode("utf-8") == 'this is a test paste'


def test_use_wrong_paste_variable_gives_400():
    app = TestApp(bottle.app())
    resp = app.post('/', {'b': 'this is a test paste'}, status=400)
    assert 'Usage: send p POST variable' in resp.body.decode("utf-8")
    assert resp.status == '400 Bad Request'
    assert resp.status_int == 400
    assert resp.content_type == 'text/plain'
    assert resp.content_length > 0
