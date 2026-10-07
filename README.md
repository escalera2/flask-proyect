# Arquitectura Modular Flask - MVC con CLI Integrada

Proyecto base estructurado bajo una arquitectura inspirada en **MVC Modular** con **Flask** y **PostgreSQL**. Diseñado para máxima escalabilidad, desacoplamiento de capas y automatización de scaffolding mediante CLI personalizada.
> 📌 **Propósito del Proyecto:** Este repositorio es un proyecto práctico diseñado para implementar y explorar una arquitectura modular escalable en **Flask**, aplicando el patrón MVC desacoplado con controladores, servicios, DTOs y automatización por CLI.
---

## Características Principales

- **Arquitectura Modular por Subcarpetas:** Componentes aislados por módulo (`app/controllers/<modulo>/`, `app/services/<modulo>/`, `app/routes/<modulo>/`, `app/dtos/<modulo>/`).
- **Registro Automático de Blueprints:** La aplicación escanea e importa dinámicamente cualquier módulo registrado en `app/routes/` sin necesidad de tocar `app/__init__.py`.
- **Ruteo Dinámico Inteligente (`hasattr`):** Las rutas solo se exponen si el método existe en el controlador. Eliminar un método no rompe la aplicación ni genera errores de tipo `AttributeError`.
- **CLI Personalizada (`flask make`):** Comandos para generar y eliminar módulos y componentes frontend/backend en segundos.
- **Seguridad Garantizada:** Protección global CSRF mediante `Flask-WTF`, almacenamiento seguro de contraseñas con `Werkzeug` y middleware de autenticación.
- **Base de Datos y Seeders:** Integración con `SQLAlchemy`, control de versiones de esquema con `Flask-Migrate` y sistema de seeders para datos iniciales.

---

## Comandos de Scaffolding CLI (`flask make`)

### 1. Generar Modelo (`make model`)
Crea un modelo de SQLAlchemy en `app/models/` con la clave primaria `id` y marcas de tiempo (`created_at`, `updated_at`).
> **Nota:** Usar siempre el nombre en **singular**.

```bash
flask make model persona

```

* **Ubicación:** `app/models/persona.py`

---

### 2. Generar Backend de Módulo (`make module`)

Genera la estructura CRUD en subcarpetas dedicadas con validación dinámica de métodos.

```bash
flask make module persona

```

* `app/controllers/personas/persona_controller.py`
* `app/services/personas/persona_service.py`
* `app/routes/personas/persona_routes.py`
* `app/dtos/personas/persona_dto.py`

---

### 3. Generar Vistas Frontend (`make view`)

Crea las plantillas HTML del módulo utilizando componentes en PascalCase.

```bash
flask make view persona

```

* `app/templates/personas/PersonaForm.html`
* `app/templates/personas/PersonaPage.html`

---

### 4. Eliminar Módulo Completo (`make destroy`)

Elimina automáticamente todos los controladores, servicios, DTOs, rutas y vistas del módulo sin afectar los modelos de la base de datos.

```bash
flask make destroy persona

```

---

## Gestión de Base de Datos, Migraciones y Seeders

### 1. Flujo de Migraciones (`Flask-Migrate`):

Al crear un modelo nuevo o modificar sus campos:

```bash
# Inicializar carpeta de migraciones (solo la primera vez en el proyecto)
flask db init

# Crear un punto de migración
flask db migrate -m "Crear tabla personas"

# Aplicar los cambios a la base de datos PostgreSQL
flask db upgrade

```

### 2. Poblar Base de Datos (`Seeders`):

Para insertar el usuario Administrador por defecto (`admin@admin.com` / `password`):

```bash
flask db seed

```

---

## Instalación y Configuración Local

1. **Clonar el repositorio:**
```bash
git clone <URL_DEL_REPOSiTORIO>
cd <NOMBRE_PROYECTO>

```


2. **Crear y activar el entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
# venv\Scripts\activate   # En Windows

```


3. **Instalar dependencias:**
```bash
pip install -r requirements.txt

```


4. **Configurar el archivo `.env`:**
Crea un archivo `.env` en la raíz del proyecto basándote en el siguiente ejemplo:
```env
SECRET_KEY=dev-secret-key-change-in-production
DB_USERNAME=postgres
DB_PASSWORD=tu_contrasena
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=flask_db

```


5. **Ejecutar servidor de desarrollo:**
```bash
python run.py

```



---

## 📁 Estructura del Proyecto

```text
├── app/
│   ├── controllers/   # Controladores divididos por subcarpeta de módulo
│   ├── dtos/          # Validadores DTO de entrada
│   ├── middlewares/   # Middlewares globales y filtros de autenticación
│   ├── models/        # Entidades SQLAlchemy (Mapeo BD)
│   ├── routes/        # Rutas/Blueprints con ruteo dinámico por módulo
│   ├── services/      # Capa de lógica de negocio pura
│   ├── static/        # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/     # Plantillas Jinja2 (vistas en PascalCase)
│   └── __init__.py    # App Factory con registro automático de Blueprints
├── database/          # Instancia DB y Seeders
├── migrations/        # Historial de versiones de la BD (Flask-Migrate)
├── .env               # Variables de entorno (Ignorado en Git)
├── .gitignore         # Exclusión de venv, __pycache__, .env, etc.
├── cli.py             # Herramienta de comandos CLI (flask make / flask db)
├── config.py          # Mapeo de entornos (DevelopmentConfig / ProductionConfig)
├── requirements.txt   # Lista de dependencias congeladas
└── run.py             # Punto de entrada de la aplicación

```

```

```
