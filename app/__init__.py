import os
from flask import Flask

from app.config import configurations
from app.core.macro_loader import autoload_macros
from app.extensions import db, migrate, bcrypt, login_manager, csrf, debug_toolbar, mail

from app.users.views import users_bp
from app.auth.views import auth_bp

APP_FOLDER = os.path.dirname(os.path.realpath(__file__))


def create_app(environment="dev"):
    app = Flask(__name__)

    # Configuration
    app.config.from_object(configurations[environment])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    debug_toolbar.init_app(app)
    mail.init_app(app)

    # Register blueprint
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)

    # register macros autoloader
    macros_folder = os.path.join(APP_FOLDER, "templates/macros")
    autoload_macros(app.jinja_env, macros_folder)

    return app
