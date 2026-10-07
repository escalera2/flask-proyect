import os
import shutil
import click
from database.seeders.user_seeder import seed_users


def get_module_names(name: str):
    """
    Normaliza el nombre del módulo.
    Entrada: 'persona' o 'personas'
    Retorna:
      folder_name: 'personas' (plural para carpetas/rutas)
      singular_name: 'persona' (para archivos y variables)
      class_name: 'Persona' (para Clases, Modelos y Vistas PascalCase)
    """
    clean_name = name.lower().strip()
    if clean_name.endswith('s'):
        folder_name = clean_name
        singular_name = clean_name[:-1]
    else:
        folder_name = f"{clean_name}s"
        singular_name = clean_name

    class_name = singular_name.capitalize()
    return folder_name, singular_name, class_name


# -----------------------------------------------------------------------------
# GRUPO DE COMANDOS: flask make ...
# -----------------------------------------------------------------------------
@click.group()
def make():
    """Comandos personalizados para generar y eliminar módulos/componentes en Flask."""
    pass


@make.command('model')
@click.argument('name')
def make_model(name):
    """
    Genera un modelo de SQLAlchemy con campos base (id, created_at, updated_at).
    Ejemplo: flask make model persona
    """
    folder, singular, cap = get_module_names(name)
    file_path = f"app/models/{singular}.py"

    content = f"""from datetime import datetime
from database.db import db

class {cap}(db.Model):
    __tablename__ = '{folder}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Campos de ejemplo (agregue o ajuste según su entidad)
    # name = db.Column(db.String(100), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<{cap} {{self.id}}>'
"""

    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
        click.echo(f"  [Modelo Creado] {file_path}")
    else:
        click.echo(f"  [Existe] {file_path}")


@make.command('module')
@click.argument('name')
def make_module(name):
    """
    Genera la estructura CRUD en subcarpetas por módulo con ruteo dinámico inteligente.
    Ejemplo: flask make module persona
    """
    folder, singular, cap = get_module_names(name)

    files = {
        # CONTROLADOR DENTRO DE SUBCARPETA POR MÓDULO
        f"app/controllers/{folder}/{singular}_controller.py": f"""from flask import render_template, request, redirect, url_for, flash
from app.services.{folder}.{singular}_service import {cap}Service

class {cap}Controller:

    @staticmethod
    def index():
        \"\"\"Listar registros\"\"\"
        items = {cap}Service.get_all()
        return render_template('{folder}/{cap}Page.html', items=items)

    @staticmethod
    def show(id):
        \"\"\"Ver detalle de un registro\"\"\"
        item = {cap}Service.get_by_id(id)
        return render_template('{folder}/{cap}Page.html', item=item)

    @staticmethod
    def create():
        \"\"\"Mostrar formulario de creación\"\"\"
        return render_template('{folder}/{cap}Page.html')

    @staticmethod
    def store():
        \"\"\"Procesar y guardar nuevo registro\"\"\"
        data = request.form
        {cap}Service.create(data)
        return redirect(url_for('{folder}.index'))

    @staticmethod
    def edit(id):
        \"\"\"Mostrar formulario de edición\"\"\"
        item = {cap}Service.get_by_id(id)
        return render_template('{folder}/{cap}Page.html', item=item)

    @staticmethod
    def update(id):
        \"\"\"Procesar la actualización del registro\"\"\"
        data = request.form
        {cap}Service.update(id, data)
        return redirect(url_for('{folder}.index'))

    @staticmethod
    def destroy(id):
        \"\"\"Eliminar un registro\"\"\"
        {cap}Service.delete(id)
        return redirect(url_for('{folder}.index'))
""",

        # SERVICIO DENTRO DE SUBCARPETA POR MÓDULO
        f"app/services/{folder}/{singular}_service.py": f"""class {cap}Service:

    @staticmethod
    def get_all():
        return []

    @staticmethod
    def get_by_id(id):
        return None

    @staticmethod
    def create(data):
        pass

    @staticmethod
    def update(id, data):
        pass

    @staticmethod
    def delete(id):
        pass
""",

        # RUTAS DINÁMICAS INTELIGENTES (Verifica hasattr por defecto)
        f"app/routes/{folder}/{singular}_routes.py": f"""from flask import Blueprint
from app.controllers.{folder}.{singular}_controller import {cap}Controller

{folder}_bp = Blueprint('{folder}', __name__, url_prefix='/{folder}')

# Mapeo dinámico: Registra automáticamente SOLO los métodos que existan en {cap}Controller
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
    if hasattr({cap}Controller, method_name):
        view_func = getattr({cap}Controller, method_name)
        {folder}_bp.add_url_rule(endpoint, view_func=view_func, methods=http_methods)
""",

        # DTO DENTRO DE SUBCARPETA POR MÓDULO
        f"app/dtos/{folder}/{singular}_dto.py": f"""class {cap}DTO:

    @staticmethod
    def validate(data):
        errors = []
        return errors
"""
    }

    for path, content in files.items():
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            click.echo(f"  [Creado] {path}")
        else:
            click.echo(f"  [Existe] {path}")


@make.command('view')
@click.argument('name')
def make_view(name):
    """
    Crea la carpeta de plantillas HTML en app/templates/<modulo_plural>/
    con componentes en PascalCase (ej. PersonaForm.html, PersonaPage.html).
    Ejemplo: flask make view persona
    """
    folder, singular, cap = get_module_names(name)
    template_dir = f"app/templates/{folder}"
    os.makedirs(template_dir, exist_ok=True)

    form_filename = f"{cap}Form.html"
    page_filename = f"{cap}Page.html"

    files = {
        f"{template_dir}/{form_filename}": f"<!-- Formulario reutilizable para {cap} -->\n<form>\n</form>",
        f"{template_dir}/{page_filename}": f"""{{% extends "base.html" %}}

{{% block title %}}{cap}s{{% endblock %}}

{{% block content %}}
<h2>Módulo {cap}s</h2>
{{% include "{folder}/{form_filename}" %}}
{{% endblock %}}
"""
    }

    for path, content in files.items():
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write(content)
            click.echo(f"  [Creado] {path}")
        else:
            click.echo(f"  [Existe] {path}")


@make.command('destroy')
@click.argument('name')
def destroy_module(name):
    """
    Elimina los controladores, servicios, rutas, DTOs y vistas de un módulo.
    NO elimina los modelos de la base de datos.
    Ejemplo: flask make destroy persona
    """
    folder, singular, _ = get_module_names(name)

    files_to_remove = [
        f"app/controllers/{folder}/{singular}_controller.py",
        f"app/services/{folder}/{singular}_service.py",
        f"app/routes/{folder}/{singular}_routes.py",
        f"app/dtos/{folder}/{singular}_dto.py",
    ]

    folders_to_check = [
        f"app/controllers/{folder}",
        f"app/services/{folder}",
        f"app/routes/{folder}",
        f"app/dtos/{folder}",
    ]

    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            click.echo(f"  [Eliminado] {file_path}")

    for folder_path in folders_to_check:
        if os.path.exists(folder_path):
            entries = os.listdir(folder_path)
            if not entries or entries == ['__pycache__']:
                shutil.rmtree(folder_path)
                click.echo(f"  [Carpeta Eliminada] {folder_path}")

    template_dir = f"app/templates/{folder}"
    if os.path.exists(template_dir):
        shutil.rmtree(template_dir)
        click.echo(f"  [Carpeta de Vistas Eliminada] {template_dir}")

    click.echo(
        f"\n✨ Módulo '{folder}' eliminado correctamente (Modelos no afectados).")


# -----------------------------------------------------------------------------
# GRUPO DE COMANDOS DE BASE DE DATOS Y SEEDERS: flask db ...
# -----------------------------------------------------------------------------
@click.group(name='db')
def db_cli():
    """Comandos personalizados para la gestión de base de datos."""
    pass


@db_cli.command('seed')
def run_seeders():
    """Ejecuta los seeders para poblar la base de datos con datos iniciales."""
    click.echo("Ejecutando seeders...")
    seed_users()
    click.echo("Proceso de seeder completado.")


# -----------------------------------------------------------------------------
# REGISTRO DE COMANDOS EN LA APLICACIÓN FLASK
# -----------------------------------------------------------------------------
def init_cli(app):
    app.cli.add_command(make)
    app.cli.add_command(db_cli)
