from datetime import time

from flask import Blueprint
from flask import current_app as app
from flask import redirect, render_template
from flask_socketio import emit

from takeme.database import Resource, Settigns, database
from takeme.form import SettingsForm
from takeme.scheduler import auto_release, scheduler
from takeme.socketio import socketio
from takeme.ui.auth import auth_bp
from takeme.ui.resource import resource_bp

ui_bp = Blueprint("ui", __name__)
ui_bp.register_blueprint(auth_bp, url_prefix="/auth")
ui_bp.register_blueprint(resource_bp, url_prefix="/resource")


@ui_bp.route("/")
def ui():
    resources = database.session.query(Resource).all()
    return render_template("home.html", resources=resources)


@ui_bp.get("/settings")
def settings_get():
    form = SettingsForm()
    options = database.session.query(Settigns).first()
    if options is not None:
        form.auto_release.data = options.auto_release
        form.auto_release_time.data = options.auto_release_time
    else:
        form.auto_release.data = False
        form.auto_release_time.data = time(0, 0)
    return render_template("settings.html", form=form)


@ui_bp.post("/settings")
def settings_post():
    form = SettingsForm()
    if form.validate_on_submit():
        new_settings = Settigns(auto_release=form.auto_release.data, auto_release_time=form.auto_release_time.data)
        database.session.merge(new_settings)
        database.session.commit()
        scheduler.remove_all_jobs()
        if new_settings.auto_release:
            scheduler.add_job(
                func=auto_release,
                trigger="cron",
                hour=new_settings.auto_release_time.hour,
                minute=new_settings.auto_release_time.minute,
                id="AutoRelease",
                name="AutoRelease",
                replace_existing=True,
            )
        return redirect("/")
    return render_template("settings.html", form=form)


@socketio.on("connect")
def test_connect():
    app.logger.info(f"SocketIO client connected")
    emit("after connect", {"data": "Connected"})


@socketio.on("disconnect")
def test_disconnect():
    app.logger.info(f"SocketIO client disconnected")
