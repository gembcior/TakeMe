from takeme import create_app
from takeme.socketio import socketio

app = create_app()
socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app)
