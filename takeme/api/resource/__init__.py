from datetime import datetime

from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import current_user
from sqlalchemy.exc import NoResultFound

from takeme.database import Resource, database
from takeme.login import jwt

api_resource_bp = Blueprint("api", __name__)


def resource_as_dict(resource: Resource):
    as_dict = {
        "name": resource.name,
        "taken": resource.taken,
        "taken_by": resource.taken_by,
        "taken_on": resource.taken_on,
        "resource_type": resource.resource_type,
    }
    return as_dict


def serialize_resource(resource: Resource):
    return jsonify(resource_as_dict(resource))


def serialize_all_resource(resource: list[Resource]):
    output = []
    for item in resource:
        output.append(resource_as_dict(item))
    return jsonify(output)


@api_resource_bp.get("/")
def resource_get():
    resource = database.session.query(Resource).all()
    return serialize_all_resource(resource)


@api_resource_bp.get("/<name>")
def resource_get_by_name(name):
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        return jsonify([])
    return serialize_resource(resource)


@api_resource_bp.post("/take/<name>")
# @jwt_required()
def resource_post_take(name):
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        return make_response({"error": f"No resource found with name {name}"}, 400)
    resource.taken = True
    # resource.taken_by = get_jwt_identity()
    resource.taken_by = current_user.username
    resource.taken_on = datetime.now()
    database.session.commit()
    return make_response({"ok": "true"}, 200)


@api_resource_bp.post("/release/<name>")
# @jwt_required()
def resource_post_release(name):
    try:
        resource = database.session.query(Resource).filter_by(name=name).one()
    except NoResultFound:
        return make_response({"error": f"No resource found with name {name}"}, 400)
    resource.taken = False
    resource.taken_by = None
    resource.taken_on = None
    database.session.commit()
    return make_response({"ok": "true"}, 200)


@api_resource_bp.put("/")
def resource_put():
    return {"resource": "OK", "method": "PUT"}


@api_resource_bp.delete("/")
def resource_delete():
    return {"resource": "OK", "method": "DELETE"}
