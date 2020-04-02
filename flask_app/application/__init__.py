""" Initialize app """
import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap

def create_app(config=None):
    "construct the core application"
    app = Flask(__name__)

    if config is None:
        app.config.from_mapping(
            SECRET_KEY="dev",
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
    else:
        app.config.from_object(config)

    from .models import db, migrate, login_manager
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    Bootstrap(app)
    
    # from .admin import admin_routes
    from .auth import auth_routes
    from .main import main_routes
    # from .api import api_routes
    
    app.register_blueprint(auth_routes.auth_bp)
    # app.register_blueprint(admin_routes.auth_bp)
    app.register_blueprint(main_routes.main_bp)
    # app.register_blueprint(admin_routes.api_bp)
    
    return app