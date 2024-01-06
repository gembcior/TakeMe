from datetime import datetime

from flask import Blueprint, abort, make_response, redirect, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.exc import NoResultFound

from takeme.database import Resource, database
from takeme.form import AddResourceForm, ResourceUpdateForm

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
    resource.message = ""
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
    form = ResourceUpdateForm()
    form.name.data = resource.name
    form.resource_type.data = resource.resource_type
    form.notes.data = resource.notes
    return render_template("resource.html", resource=resource, form=form)


@resource_bp.post("/update/<name>")
@login_required
def update_by_name(name):
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        abort(404)
    form = ResourceUpdateForm()
    if form.validate_on_submit():
        resource.name = form.name.data
        resource.resource_type = form.resource_type.data
        resource.notes = form.notes.data
        database.session.commit()
        return redirect("/")
    return render_template("resource.html", resource=resource, form=form)


@resource_bp.put("/msg/<name>")
@login_required
def msg_by_name(name):
    if not request.is_json:
        return make_response({"error": f"Unsupported request format"}, 400)
    if request.json is None:
        return make_response({"error": f"Unsupported request format"}, 400)
    if "data" not in request.json:
        return make_response({"error": f"Unsupported request format"}, 400)
    data = request.json["data"]
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        return make_response({"error": f"No resource found with name {name}"}, 400)
    resource.message = data
    database.session.commit()
    return make_response({"ok": "true"}, 200)
