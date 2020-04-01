""" Initialize app """

import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask


def create_app(Config):
    "construct the core application"
    app = Flask(__name__)

    app.config.from_object(Config)

    from .models import db, migrate, login_manager
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # from .admin import admin_routes
    from .auth import auth_routes
    from .main import main_routes
    # from .api import api_routes
    
    app.register_blueprint(auth_routes.auth_bp)
    # app.register_blueprint(admin_routes.auth_bp)
    app.register_blueprint(main_routes.main_bp)
    # app.register_blueprint(admin_routes.api_bp)
    
    return app