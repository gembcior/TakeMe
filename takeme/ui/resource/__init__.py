from datetime import datetime

from flask import Blueprint, abort, make_response, redirect, render_template
from flask_login import current_user, login_required
from sqlalchemy.exc import NoResultFound

from takeme.database import Resource, database
from takeme.form import AddResourceForm

resource_bp = Blueprint("resource", __name__)


@resource_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddResourceForm()
    if form.validate_on_submit():
        resource = Resource(
            name=form.name.data,
            resource_type=form.resource_type.data,
            notes=form.notes.data,
        )
        database.session.add(resource)
        database.session.commit()
        return redirect("/")
    return render_template("add.html", form=form)


@resource_bp.post("/take/<name>")
@login_required
def take_by_name(name):
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        return make_response({"error": f"No resource found with name {name}"}, 400)
    resource.taken = True
    resource.taken_by = current_user.username
    resource.taken_on = datetime.now()
    database.session.commit()
    return make_response({"ok": "true"}, 200)


@resource_bp.post("/release/<name>")
@login_required
def release_by_name(name):
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        return make_response({"error": f"No resource found with name {name}"}, 400)
    resource.taken = False
    resource.taken_by = None
    resource.taken_on = None
    database.session.commit()
    return make_response({"ok": "true"}, 200)


@resource_bp.route("/<name>")
def get_by_name(name):
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        abort(404)
    return render_template("resource.html", resource=resource)
