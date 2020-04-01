from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

admin_bp = Blueprint("admin_bp", __name__, template_folder="templates", static_folder="static")

@admin_bp.route("/", defaults={"page": "index"})
@admin_bp.route("/<page>")
def show(page):
    try:
        return render_template(f"pages/{page}.html")
    except TemplateNotFound:
        abort(404)