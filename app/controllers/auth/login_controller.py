from flask import render_template, request, redirect, url_for, flash
from app.dtos.auth.login_dto import LoginDTO
from app.services.auth.auth_service import AuthService


class LoginController:

    @staticmethod
    def show_login():
        """
        Muestra la página con el formulario de inicio de sesión.
        Ruta: GET /auth/login
        """
        return render_template('auth/LoginPage.html')

    @staticmethod
    def login():
        """
        Procesa la petición POST del formulario de login:
        1. Captura la solicitud HTTP (request.form).
        2. Valida la estructura mediante LoginDTO.
        3. Ejecuta la regla de negocio con AuthService.
        4. Maneja la respuesta, sesiones y mensajes flash.
        Ruta: POST /auth/login
        """
        # 1. Extraer los campos enviados desde la vista
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        # 2. Validar reglas de entrada con el DTO (Form Request)
        dto = LoginDTO(email=email, password=password)
        errors = dto.validate()

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/LoginPage.html', email=email)

        # 3. Lógica de Negocio: Verificar credenciales en la BD
        success, message, user = AuthService.authenticate(
            dto.email, dto.password)

        if not success:
            flash(message, 'danger')
            return render_template('auth/LoginPage.html', email=email)

        # 4. Iniciar sesión y establecer las variables de sesión
        AuthService.login_user(user)
        flash(
            f'¡Bienvenido de nuevo, {user.name if hasattr(user, "name") else user.email}!', 'success')

        # Redirigir al panel principal o dashboard
        return redirect(url_for('auth.show_login'))

    @staticmethod
    def logout():
        """
        Destruye la sesión activa del usuario y redirige al login.
        Ruta: GET/POST /auth/logout
        """
        AuthService.logout_user()
        flash('Has cerrado sesión correctamente.', 'info')
        return redirect(url_for('auth.show_login'))
