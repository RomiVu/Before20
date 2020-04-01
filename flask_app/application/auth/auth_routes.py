from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


auth_bp = Blueprint("auth_bp", __name__, template_folder="templates", static_folder="static")


@auth_bp.route('/login')
def login():
    try:
        return render_template('login.html')
    except TemplateNotFound:
        abort(404)


@auth_bp.route('/logout')
def logout():
    try:
        return render_template('logout.html')
    except TemplateNotFound:
        print("wtf ?")
        abort(404)