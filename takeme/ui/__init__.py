from datetime import time

from flask import Blueprint, redirect, render_template

from takeme.database import Resource, Settigns, database
from takeme.form import SettingsForm
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
        options = database.session.query(Settigns).first()
        if options is not None:
            options.auto_release = form.auto_release.data
            options.auto_release_time = form.auto_release_time.data
        else:
            new_settings = Settigns(auto_release=form.auto_release.data, auto_release_time=form.auto_release_time.data)
            database.session.add(new_settings)
        database.session.commit()
        return redirect("/")
    return render_template("settings.html", form=form)
