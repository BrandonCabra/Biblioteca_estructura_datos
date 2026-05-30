# Sistema de Gestión de Biblioteca

API REST para gestión de biblioteca desarrollada con FastAPI, SQLite y una estructura modular por capas.

## Características

- Registro, consulta y eliminación de libros.
- Registro y consulta de usuarios.
- Gestión de préstamos, devoluciones y reservas.
- Historial y métricas del sistema.
- Frontend estático servido desde FastAPI.
- Documentación automática con Swagger y ReDoc.

## Estructura del proyecto

```text
Biblioteca_estructura_datos/
├── app/
│   ├── controllers/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
├── static/
├── templates/
├── biblioteca.db
├── main.py
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.12 o superior.
- Dependencias listadas en `requirements.txt`.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

Puedes iniciar el servidor de cualquiera de estas formas:

```bash
python main.py
```

```bash
uvicorn main:app --reload
```

Luego abre:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Endpoints principales

- `GET /api/libros`
- `POST /api/libros`
- `GET /api/usuarios`
- `POST /api/usuarios`
- `GET /api/prestamos`
- `POST /api/prestamos`
- `GET /api/reservas`
- `POST /api/reservas`
- `GET /api/historial`
- `GET /api/metricas`

## Nota

La base de datos SQLite se inicializa al arrancar la aplicación desde `main.py`.
