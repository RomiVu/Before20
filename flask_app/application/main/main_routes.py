from datetime import datetime

from flask import Blueprint, render_template, abort, flash, request, url_for, redirect, current_app
from jinja2 import TemplateNotFound
from flask_login import login_required, current_user

from .main_form import EditProfileForm, PostForm
from ..models import db, User, Post

main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder="static")

@main_bp.before_app_request
def update_last_seen():
    if not current_user.is_anonymous:
        user = User.query.filter_by(name=current_user.name).first()
        if user:
            user.last_seen = datetime.utcnow()
            db.session.commit()
        
@main_bp.route('/')
@main_bp.route('/index')
def index():
    try:
        return render_template('main/index.html')
    except TemplateNotFound:
        abort(404)

@main_bp.route('/user/<username>')
@login_required
def user(username):
    try:
        user = User.query.filter_by(name=username).first_or_404(description=f"there is no user named {username}")
        posts = user.followed_posts().all()
        return render_template('main/user.html', user=user, posts=posts)
    except TemplateNotFound:
        abort(404)

@main_bp.route('/edit_profile/<username>', methods=["GET", "POST"])
@login_required
def edit_profile(username):
    user = User.query.filter_by(name=username).first_or_404(description=f"username:{username} doesn't exit.")
    form = EditProfileForm(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('main_bp.user', username=user.name))
    return render_template('main/edit_profile.html', form=form)


@main_bp.route('/follow/<username>')
@login_required
def follow(username):
    if current_user is None or username == current_user.name:
        flash(f'Invaild user or You can not ollow yourself.')
        return redirect(url_for('main_bp.index'))
    user = User.query.filter_by(name=username).first()
    current_user.follow(user)
    posts = user.followed_posts().all()

    db.session.commit()
    return render_template('main/user.html', user=user, posts=posts)


@main_bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    if current_user is None or username == current_user.name:
        flash(f'Invaild user or You can not unfollow yourself.')
        return redirect(url_for('main_bp.index'))
    user = User.query.filter_by(name=username).first()
    current_user.unfollow(user)
    posts = user.followed_posts().all()

    db.session.commit()
    return render_template('main/user.html', user=user, posts=posts)


@main_bp.route('/post', methods=["GET", "POST"])
@login_required
def post():
    if not current_user.is_authenticated:
        return redirect(url_for('auth_bp.login'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author_id=current_user.id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main_bp.user', username=current_user.name))
    return render_template('main/post.html', form=form)


@main_bp.route('/explore')
@login_required
def explore():
    posts = Post.query.order_by(Post.pub_date.desc()).limit(50).all()
    return render_template('main/explore.html', posts=posts)