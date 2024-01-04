from flask import Blueprint, render_template

from takeme.database import Resource, database
from takeme.ui.auth import auth_bp
from takeme.ui.resource import resource_bp

ui_bp = Blueprint("ui", __name__)
ui_bp.register_blueprint(auth_bp, url_prefix="/auth")
ui_bp.register_blueprint(resource_bp, url_prefix="/resource")


@ui_bp.route("/")
def ui():
    resources = database.session.query(Resource).all()
    return render_template("home.html", resources=resources)