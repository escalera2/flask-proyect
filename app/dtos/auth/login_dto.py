import re


class LoginDTO:

    def __init__(self, email: str, password: str):
        self.email = (email or "").strip().lower()
        self.password = password or ""

    def validate(self) -> list[str]:
        """
        Valida el formato y presencia de datos de entrada.
        Retorna una lista de errores (vacía si todo es válido).
        """
        errors = []

        if not self.email:
            errors.append("El correo electrónico es obligatorio.")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            errors.append("El formato del correo electrónico no es válido.")

        if not self.password:
            errors.append("La contraseña es obligatoria.")

        return errors
