# Gestor de Tareas (Python + PostgreSQL)

Proyecto CRUD en consola para crear, listar, editar, actualizar estado y eliminar tareas usando PostgreSQL.

## Tecnologías
- Python
- PostgreSQL
- psycopg2
- python-dotenv

## Configuración
1. Crear DB `tareas_db` y tabla `tareas` (ver script en pgAdmin).
2. Crear `.env` con credenciales.
3. Instalar dependencias:
   - python -m venv venv
   - venv\Scripts\activate
   - pip install -r requirements.txt

## Ejecutar
python app.py
