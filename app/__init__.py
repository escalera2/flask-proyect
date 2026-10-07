import os
import importlib
import pkgutil
from flask import Flask, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import config
from database.db import db, migrate
from app.middlewares.auth_middleware import init_auth_middleware

csrf = CSRFProtect()


def register_blueprints_automatically(app):
    """
    Escanea la carpeta app/routes y registra automáticamente
    todos los Blueprints (*_bp) encontrados.
    """
    routes_dir = os.path.join(app.root_path, 'routes')

    if not os.path.exists(routes_dir):
        return

    for root, dirs, files in os.walk(routes_dir):
        for file in files:
            if file.endswith('_routes.py'):

                rel_path = os.path.relpath(
                    os.path.join(root, file), app.root_path)
                module_name = 'app.' + rel_path[:-3].replace(os.sep, '.')

                module = importlib.import_module(module_name)

                for attr_name in dir(module):
                    if attr_name.endswith('_bp'):
                        blueprint = getattr(module, attr_name)
                        app.register_blueprint(blueprint)


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    init_auth_middleware(app)

    @app.route('/')
    def index():
        return redirect(url_for('auth.show_login'))

    register_blueprints_automatically(app)

    from cli import init_cli
    init_cli(app)

    return app
