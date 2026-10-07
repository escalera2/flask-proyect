from functools import wraps
from flask import session, redirect, url_for, flash, request


def login_required(f):
    """
    Decorador para proteger rutas individuales.
    Uso: @login_required arriba de un método en el controlador o ruta.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.show_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def init_auth_middleware(app):
    """
    Middleware global usando hooks de Flask (before_request).
    Protege todas las rutas por defecto, excepto las públicas especificados.
    """
    # Lista de rutas públicas que NO requieren autenticación
    PUBLIC_ENDPOINTS = [
        'auth.show_login',
        'auth.login',
        'static'
    ]

    @app.before_request
    def check_authentication():
        # Si la ruta solicitada es None o es una ruta pública, permitir acceso
        if request.endpoint is None or request.endpoint in PUBLIC_ENDPOINTS:
            return None

        # Si el usuario no tiene sesión activa, redirigir al login
        if 'user_id' not in session:
            flash(
                'Sesión expirada o no iniciada. Por favor, ingresa tus credenciales.', 'warning')
            return redirect(url_for('auth.show_login'))
