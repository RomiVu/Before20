from datetime import datetime, timedelta
from hashlib import md5
from uuid import uuid4

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth_bp.login'
login_manager.login_message = "Please log in to access this page."


follow_relation = db.Table(
    'follow_relation',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

post_category = db.Table(
    'post_category',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', lazy='dynamic', backref='author')
    followed = db.relationship('User', secondary=follow_relation,
                                    primaryjoin=(follow_relation.c.follower_id == id),
                                    secondaryjoin=(follow_relation.c.followed_id == id),
                                    lazy="dynamic", 
                                    backref=db.backref("followers", lazy='dynamic'))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    about_me = db.Column(db.String(140))
    avator = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user') # api/user/admin/staff four kinds of role

    api_token = db.relationship('ApiToken', lazy='dynamic', backref='user')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_following(self, user):
        return self.followed.filter(follow_relation.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def followed_posts(self):
        # include meself post
        followed_posts = Post.query.join(
            follow_relation, (follow_relation.c.followed_id == Post.author_id)).filter(
                follow_relation.c.follower_id == self.id
            )
        my_posts = Post.query.filter_by(author_id=self.id)
        return followed_posts.union(my_posts).order_by(Post.pub_date.desc())
    
    def avatar(self, _):
        return 'http://121.42.14.144/image/cat1.png'

    def __repr__(self):
        return f"<User {self.name}>"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categories = db.relationship(
        'Category', secondary=post_category,
        lazy="dynamic", 
        backref=db.backref("posts", lazy='dynamic')
    )

    def add_category(self, category):
        if not self.is_category_of(category):
            self.categories.append(category)

    def delete_category(self, category):
        if self.is_category_of(category):
            self.categories.remove(category)
    
    def is_category_of(self, category):
        return self.categories.filter(post_category.c.category_id == category.id).count() > 0
    
    # def get_categories_label(self):
    #     return Category.query.join(
    #         post_category, (post_category.c.category_id == id)).filter(
    #             post_category.c.post_id == self.id
    #         )

    def __repr__(self):
        return f"<Post {self.title}>"


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(10), nullable=False, unique=True)
    description = db.Column(db.String(120), nullable=True)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Category {self.title}>"

class ApiToken(db.Model):
    __tablename__ = "apitoken"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.String(140))
    # expire_minutes = current_app.config.get("API_TOKEN_EXPIRE_TIME", 10)
    # to be configed
    exipred = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(minutes=10))

    @classmethod
    def gen_api_token(cls):
        return uuid4().hex
    
    def update_api_token(self):
        if datetime.utcnow() >= self.exipred:
            self.token = ApiToken.gen_api_token()
            self.exipred = datetime.utcnow() + timedelta(minutes=10) # to be configed

    def __repr__(self):
        return f"<ApiToken {self.id}>"