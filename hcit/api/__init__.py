from flask import Blueprint

from hcit.api.resource import api_resource_bp

api_bp = Blueprint("api", __name__)
api_bp.register_blueprint(api_resource_bp, url_prefix="/resource")


@api_bp.route("/")
def api():
    return {"api": "OK", "method": "GET"}
