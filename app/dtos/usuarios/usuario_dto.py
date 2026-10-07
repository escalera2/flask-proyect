import re


class UsuarioDTO:

    def __init__(self, name="", email="", password=""):
        self.name = name.strip() if name else ""
        self.email = email.strip().lower() if email else ""
        self.password = password.strip() if password else ""

    def validate(self, is_update=False):
        errors = []
        if not self.name:
            errors.append("El nombre es obligatorio.")

        if not self.email:
            errors.append("El correo electrónico es obligatorio.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors.append("El formato del correo electrónico es inválido.")

        if not is_update and not self.password:
            errors.append("La contraseña es obligatoria.")

        return errors
