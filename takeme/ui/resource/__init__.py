from datetime import datetime

from flask import Blueprint, abort, make_response, redirect, render_template, request
from flask_login import current_user, login_required
from sqlalchemy.exc import NoResultFound

from takeme.database import Resource, database
from takeme.form import AddResourceForm, ResourceUpdateForm
from takeme.socketio import socketio

resource_bp = Blueprint("resource", __name__)


def get_resource(id: int) -> Resource | None:
    try:
        resource = database.session.query(Resource).filter_by(id=id).one()
    except NoResultFound:
        return None
    return resource


def update_database_resource(resource: Resource) -> None:
    database.session.merge(resource)
    database.session.commit()


def emit_resource_update(id: int) -> None:
    resource = get_resource(id)
    if resource is None:
        socketio.emit("resource not update", {"resource_id": id})
        return
    output = {
        "resource_id": resource.id,
    }
    socketio.emit("resource update", output)


@resource_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddResourceForm()
    if form.validate_on_submit():
        resource = Resource(
            name=form.name.data.strip(),
            resource_type=form.resource_type.data,
            notes=form.notes.data.strip(),
        )
        database.session.add(resource)
        database.session.commit()
        emit_resource_update(resource.id)
        return redirect("/")
    return render_template("add.html", form=form)


@resource_bp.post("/take/<id>")
@login_required
def take_by_id(id):
    resource = get_resource(id)
    if resource is None:
        return make_response({"error": f"No resource found with id {id}"}, 400)
    resource.taken = True
    resource.taken_by = current_user.username
    resource.taken_on = datetime.now()
    resource.message = ""
    database.session.merge(resource)
    database.session.commit()
    emit_resource_update(resource.id)
    return make_response({"ok": "true"}, 200)


@resource_bp.post("/release/<id>")
@login_required
def release_by_id(id):
    resource = get_resource(id)
    if resource is None:
        return make_response({"error": f"No resource found with id {id}"}, 400)
    resource.taken = False
    resource.taken_by = None
    resource.taken_on = None
    database.session.commit()
    emit_resource_update(resource.id)
    return make_response({"ok": "true"}, 200)


@resource_bp.route("/<id>")
@login_required
def get_by_id(id):
    resource = get_resource(id)
    if resource is None:
        abort(404)
    form = ResourceUpdateForm()
    form.name.data = resource.name
    form.resource_type.data = resource.resource_type
    form.notes.data = resource.notes
    return render_template("resource.html", resource=resource, form=form)


@resource_bp.post("/update/<id>")
@login_required
def update_by_id(id):
    resource = get_resource(id)
    if resource is None:
        abort(404)
    form = ResourceUpdateForm()
    if form.validate_on_submit():
        # TODO add name validation to prevent update to exising name
        resource.name = form.name.data
        resource.resource_type = form.resource_type.data
        resource.notes = form.notes.data.strip()
        database.session.commit()
        emit_resource_update(resource.id)
        return redirect("/")
    return render_template("resource.html", resource=resource, form=form)


@resource_bp.post("/rm/<id>")
@login_required
def rm_by_id(id):
    resource = get_resource(id)
    if resource is None:
        abort(404)
    database.session.delete(resource)
    database.session.commit()
    emit_resource_update(resource.id)
    return redirect("/")


@resource_bp.put("/msg/<id>")
@login_required
def msg_by_id(id):
    if not request.is_json:
        return make_response({"error": f"Unsupported request format"}, 400)
    if request.json is None:
        return make_response({"error": f"Unsupported request format"}, 400)
    if "data" not in request.json:
        return make_response({"error": f"Unsupported request format"}, 400)
    data = request.json["data"]
    resource = get_resource(id)
    if resource is None:
        return make_response({"error": f"No resource found with id {id}"}, 400)
    resource.message = data
    database.session.commit()
    emit_resource_update(resource.id)
    return make_response({"ok": "true"}, 200)


@resource_bp.get("/list/<id>")
def get_list_item_by_id(id):
    resource = get_resource(id)
    if resource is None:
        abort(404)
    return render_template("resource_item.html", resource=resource)
