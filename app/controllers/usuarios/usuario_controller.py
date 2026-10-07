from flask import render_template, request, redirect, url_for, flash
from app.services.usuarios.usuario_service import UsuarioService
from app.dtos.usuarios.usuario_dto import UsuarioDTO


class UsuarioController:

    @staticmethod
    def index():
        items = UsuarioService.get_all()
        return render_template('usuarios/UsuarioPage.html', items=items)

    @staticmethod
    def store():
        dto = UsuarioDTO(
            name=request.form.get('name'),
            email=request.form.get('email'),
            password=request.form.get('password')
        )
        errors = dto.validate()

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('usuarios.index'))

        success, message = UsuarioService.create(request.form)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('usuarios.index'))

    @staticmethod
    def update(id):
        dto = UsuarioDTO(
            name=request.form.get('name'),
            email=request.form.get('email'),
            password=request.form.get('password')
        )
        errors = dto.validate(is_update=True)

        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('usuarios.index'))

        success, message = UsuarioService.update(id, request.form)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('usuarios.index'))

    @staticmethod
    def destroy(id):
        success, message = UsuarioService.delete(id)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('usuarios.index'))
