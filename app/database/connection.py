"""
app/database/connection.py
Gestión de la conexión SQLite y creación del esquema de base de datos.
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "biblioteca.db"


def get_connection() -> sqlite3.Connection:
    """Retorna una conexión a la base de datos SQLite con row_factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row          # permite acceso por nombre de columna
    conn.execute("PRAGMA foreign_keys = ON") # activa integridad referencial
    return conn


def init_db() -> None:
    """Crea todas las tablas si no existen e inserta datos de demostración."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS libros (
            isbn        TEXT PRIMARY KEY,
            titulo      TEXT NOT NULL,
            autor       TEXT NOT NULL,
            anio        TEXT,
            copias      INTEGER NOT NULL DEFAULT 1,
            disponibles INTEGER NOT NULL DEFAULT 1,
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id          TEXT PRIMARY KEY,
            nombre      TEXT NOT NULL,
            correo      TEXT,
            created_at  TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE TABLE IF NOT EXISTS prestamos (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn            TEXT NOT NULL REFERENCES libros(isbn),
            usuario_id      TEXT NOT NULL REFERENCES usuarios(id),
            fecha_prestamo  TEXT DEFAULT (datetime('now','localtime')),
            fecha_devolucion TEXT,
            activo          INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS reservas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn        TEXT NOT NULL REFERENCES libros(isbn),
            usuario_id  TEXT NOT NULL REFERENCES usuarios(id),
            fecha       TEXT DEFAULT (datetime('now','localtime')),
            atendida    INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS historial (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo        TEXT NOT NULL,
            isbn        TEXT NOT NULL,
            usuario_id  TEXT NOT NULL,
            detalle     TEXT,
            fecha       TEXT DEFAULT (datetime('now','localtime'))
        );
    """)

    # Datos de demostración solo si la BD está vacía
    existing = cursor.execute("SELECT COUNT(*) FROM libros").fetchone()[0]
    if existing == 0:
        libros_demo = [
            ("978-0-06-112008-4", "Cien años de soledad",               "Gabriel García Márquez", "1967", 3),
            ("978-0-7432-7356-5", "Harry Potter y la piedra filosofal",  "J.K. Rowling",           "1997", 2),
            ("978-84-339-7557-3", "El amor en los tiempos del cólera",   "Gabriel García Márquez", "1985", 2),
            ("978-84-9838-226-1", "El nombre de la rosa",                "Umberto Eco",            "1980", 1),
            ("978-0-316-76948-0", "El guardián entre el centeno",        "J.D. Salinger",          "1951", 2),
        ]
        cursor.executemany(
            "INSERT INTO libros (isbn, titulo, autor, anio, copias, disponibles) VALUES (?,?,?,?,?,?)",
            [(i,t,a,y,c,c) for i,t,a,y,c in libros_demo]
        )
        usuarios_demo = [
            ("U001", "María González",   "maria@demo.com"),
            ("U002", "Carlos Rodríguez", "carlos@demo.com"),
            ("U003", "Ana Martínez",     "ana@demo.com"),
        ]
        cursor.executemany(
            "INSERT INTO usuarios (id, nombre, correo) VALUES (?,?,?)",
            usuarios_demo
        )

    conn.commit()
    conn.close()
