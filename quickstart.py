import gevent
from flask import Flask, render_template
from flask_sockets import Sockets


app = Flask(__name__)
app.debug = True
sockets = Sockets(app)
app.websockets = set()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/start-task')
def start_task():
    gevent.spawn(cool_task, 10)
    return 'ok'


@sockets.route('/echo')
def echo_socket(ws):
    print('Websocket opened')
    app.websockets.add(ws)

    while not ws.closed:
        message = ws.receive()
        if message is not None:
            reverse = message[::-1]
            ws.send('{} | {}'.format(message, reverse))
    print('Websocket closed')
    app.websockets.remove(ws)



def cool_task(num_steps):
    for i in range(1, num_steps+1):
        for ws in app.websockets:
            ws.send('Task step {}'.format(i))
        gevent.sleep(0.5)



if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 8000), app, handler_class=WebSocketHandler)
    server.serve_forever()
