from flask import Flask, render_template
from flask_sockets import Sockets


app = Flask(__name__)
app.debug = True
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    print('Websocket opened')
    while not ws.closed:
        message = ws.receive()
        reverse = message[::-1]
        ws.send('{} | {}'.format(message, reverse))
    print('Websocket closed')


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
