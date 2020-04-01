from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder="static")


@main_bp.route('/')
@main_bp.route('/index')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@main_bp.route('/user/<username>')
def user(username):
    try:
        return render_template('user.html')
    except TemplateNotFound:
        abort(404)