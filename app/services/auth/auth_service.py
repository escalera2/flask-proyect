from flask import session
from werkzeug.security import check_password_hash
# Importa tu modelo User cuando lo tengas conectado a BD
# from app.models.user import User


class AuthService:

    @staticmethod
    def authenticate(email, password):
        """Verifica credenciales de usuario."""
        # Ejemplo de simulación o consulta a BD
        # user = User.query.filter_by(email=email).first()
        # if user and check_password_hash(user.password, password):
        #     return True, "Inicio de sesión exitoso", user

        if email == "admin@admin.com" and password == "123456":
            user_data = {"id": 1, "name": "Administrador", "email": email}
            return True, "Inicio de sesión exitoso", user_data

        return False, "Correo o contraseña incorrectos.", None

    @staticmethod
    def login_user(user):
        """Guarda los datos clave en la sesión de Flask."""
        session.clear()
        # Si es un objeto SQLAlchemy usa user.id, si es diccionario usa user['id']
        session['user_id'] = user.id if hasattr(user, 'id') else user['id']
        session['user_email'] = user.email if hasattr(
            user, 'email') else user['email']
        session['user_name'] = user.name if hasattr(
            user, 'name') else user.get('name', '')

    @staticmethod
    def logout_user():
        """Limpia la sesión de Flask."""
        session.clear()
