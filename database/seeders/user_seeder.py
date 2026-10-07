from database.db import db
from app.models.user import User


def seed_users():
    """Pobla la base de datos con un usuario administrador por defecto."""
    admin_email = "admin@admin.com"
    user = User.query.filter_by(email=admin_email).first()

    if not user:
        admin_user = User(
            name="Administrador",
            email=admin_email
        )
        admin_user.set_password("password")

        db.session.add(admin_user)
        db.session.commit()
        print(" [Seeder] Usuario Administrador creado exitosamente.")
    else:
        print(" [Seeder] El usuario Administrador ya existe.")
