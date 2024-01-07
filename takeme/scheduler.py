from flask_apscheduler import APScheduler

from takeme.database import Settigns, database

scheduler = APScheduler()


@scheduler.task("cron", id="auto_release", minute="*")
def auto_release():
    if scheduler.app is None:
        return
    with scheduler.app.app_context():
        settings = database.session.query(Settigns).first()
        if settings is not None:
            do_release = settings.auto_release
        else:
            do_release = False
        if do_release:
            print("Auto Release executed")
        else:
            print("Auto Release disabled")
