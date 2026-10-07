# app/routes/usuarios/usuario_routes.py
from flask import Blueprint
from app.controllers.usuarios.usuario_controller import UsuarioController

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Mapeo dinámico: Mapea automáticamente solo los métodos que existan en el Controlador
routes_map = [
    ('index', '/', ['GET']),
    ('create', '/nuevo', ['GET']),
    ('store', '/guardar', ['POST']),
    ('show', '/<int:id>', ['GET']),
    ('edit', '/<int:id>/editar', ['GET']),
    ('update', '/<int:id>/actualizar', ['POST']),
    ('destroy', '/<int:id>/eliminar', ['POST']),
]

for method_name, endpoint, http_methods in routes_map:
    # Verificamos si el método existe en el Controlador antes de registrar la ruta
    if hasattr(UsuarioController, method_name):
        view_func = getattr(UsuarioController, method_name)
        usuarios_bp.add_url_rule(
            endpoint, view_func=view_func, methods=http_methods)
