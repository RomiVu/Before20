from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from jinja2 import TemplateNotFound
from flask_login import current_user, logout_user, login_user

from .auth_forms import RegisterForm, LoginForm, ResetPasswordForm
from ..models import db, User, Post, Category


auth_bp = Blueprint("auth_bp", __name__, template_folder="templates", static_folder="static")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_anonymous:
        return redirect(url_for("main_bp.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/egister.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_anonymous:
        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).first()
            if (user is None) or (not user.check_password(form.password.data)):
                flash('Invalid username or password')
                return redirect(url_for('auth_bp.login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main_bp.index'))
        return render_template('auth/login.html', form=form)
    else:
        return redirect(url_for("main_bp.index"))

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main_bp.index"))


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if not current_user.is_anonymous:
        return redirect(url_for("main_bp.index"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None:
            flash(f"username:{form.username.data} doesn't exist")
            return redirect(url_for('auth_bp.reset_password'))
        user.set_password(form.password.data)
        db.session.commit()
        flash(f"username:{form.username.data} have changed your password.")
        return redirect(url_for('auth_bp.login'))
    return render_template('auth/reset_password.html', form=form)