"""
main.py — Punto de entrada de la aplicación FastAPI.
Configura la app, CORS, rutas estáticas y la base de datos.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uvicorn

from app.database.connection import init_db
from app.controllers.routes import router

# ─── Inicializar BD al arrancar ───────────────────────────────
init_db()

# ─── Aplicación FastAPI ───────────────────────────────────────
app = FastAPI(
    title="Sistema de Gestión de Biblioteca",
    description="API REST con arquitectura limpia — MVC + Repository Pattern + SQLite",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ─── CORS (permite que el frontend consuma la API) ────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Archivos estáticos ───────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# ─── Rutas de la API ─────────────────────────────────────────
app.include_router(router, prefix="/api")

# ─── Sirve el frontend ────────────────────────────────────────
@app.get("/", include_in_schema=False)
def index():
    return FileResponse(str(BASE_DIR / "templates" / "index.html"))


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
