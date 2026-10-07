from database.db import db
from app.models.user import User


class UsuarioService:

    @staticmethod
    def get_all():
        return User.query.order_by(User.id.desc()).all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create(data):
        email = data.get('email', '').strip().lower()

        if User.query.filter_by(email=email).first():
            return False, "El correo electrónico ya está registrado."

        user = User(
            name=data.get('name', '').strip(),
            email=email
        )
        user.set_password(data.get('password', ''))

        db.session.add(user)
        db.session.commit()
        return True, "Usuario creado exitosamente."

    @staticmethod
    def update(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return False, "Usuario no encontrado."

        email = data.get('email', '').strip().lower()
        existing = User.query.filter(
            User.email == email, User.id != user_id).first()
        if existing:
            return False, "El correo electrónico ya pertenece a otro usuario."

        user.name = data.get('name', '').strip()
        user.email = email

        if data.get('password'):
            user.set_password(data.get('password'))

        db.session.commit()
        return True, "Usuario actualizado exitosamente."

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if not user:
            return False, "Usuario no encontrado."

        db.session.delete(user)
        db.session.commit()
        return True, "Usuario eliminado correctamente."
