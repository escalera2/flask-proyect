from flask import Blueprint
from app.controllers.auth.login_controller import LoginController

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Mapeo de rutas de autenticación
auth_bp.add_url_rule(
    '/login', view_func=LoginController.show_login, methods=['GET'])
auth_bp.add_url_rule(
    '/login', view_func=LoginController.login, methods=['POST'])
auth_bp.add_url_rule(
    '/logout', view_func=LoginController.logout, methods=['GET', 'POST'])
