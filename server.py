import gevent.monkey
gevent.monkey.patch_socket()

import json
import itertools
import gevent
import gevent.event
import requests
from flask import Flask, render_template
from flask_sockets import Sockets


app = Flask(__name__)
app.debug = True
sockets = Sockets(app)
app.websockets = set()
heartbeat_evt = gevent.event.Event()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/start-task')
def start_task():
    gevent.spawn(big_task)
    return 'ok'


@app.route('/toggle-beat')
def toggle_beat():
    if heartbeat_evt.is_set():
        heartbeat_evt.clear()
    else:
        heartbeat_evt.set()
    return 'ok'


@sockets.route('/echo')
def echo_socket(ws):
    print('Websocket opened')
    app.websockets.add(ws)

    while not ws.closed:
        message = ws.receive()
        if message is not None:
            reverse = message[::-1]
            broadcast('{} | {}'.format(message, reverse), src='echo')

    print('Websocket closed')
    app.websockets.remove(ws)


def big_task():
    gevent.joinall([
        gevent.spawn(cool_task, 8),
        gevent.spawn(boring_task, 4),
        gevent.spawn(get_ip_address),
    ])
    broadcast('Work is done!!!', src='big')


def cool_task(num_steps):
    for i in range(1, num_steps+1):
        broadcast('Cool task step {}'.format(i), src='cool')
        gevent.sleep(0.5)


def boring_task(num_steps):
    for i in range(1, num_steps+1):
        broadcast('Boring task step {}'.format(i), src='boring')
        gevent.sleep(1.2)


def get_ip_address():
    text = requests.get('http://ipecho.net/plain').text
    broadcast('Your IP address is {}'.format(text), src='ip')


def heart_beat():
    for i in itertools.count(1):
        heartbeat_evt.wait()
        broadcast('Heartbeat {}'.format(i), src='heartbeat')
        gevent.sleep(1)


def broadcast(message, src=''):
    data = json.dumps(dict(value=message, src=src))
    for ws in app.websockets:
        ws.send(data)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    gevent.spawn(heart_beat)
    port = 8000
    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    print('Starting server on port {}'.format(port))
    server.serve_forever()
