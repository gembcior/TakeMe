from flask_apscheduler import APScheduler

from takeme.database import Resource, database
from takeme.socketio import socketio

scheduler = APScheduler()


def auto_release():
    if scheduler.app is None:
        return
    with scheduler.app.app_context():
        resources = database.session.query(Resource).all()
        for res in resources:
            res.taken = False
            res.taken_by = None
            res.taken_on = None
        database.session.commit()
        socketio.emit("all resource update")
