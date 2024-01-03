from flask import Blueprint, redirect, render_template

from hcit.database import Resource, database
from hcit.form import AddResourceForm

resource_bp = Blueprint("resource", __name__)


@resource_bp.route("/add", methods=["GET", "POST"])
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


@resource_bp.route("/take", methods=["GET", "POST"])
def take():
    return redirect("/")


@resource_bp.route("/release", methods=["GET", "POST"])
def release():
    return redirect("/")
