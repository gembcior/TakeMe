from takeme import create_app
from takeme.scheduler import scheduler
from takeme.socketio import socketio

app = create_app()
socketio.init_app(app)
scheduler.start()

if __name__ == "__main__":
    socketio.run(app)
