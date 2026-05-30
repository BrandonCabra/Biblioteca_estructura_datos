"""
app/repositories/repositories.py
Capa de acceso a datos (Repository Pattern).
Cada repositorio encapsula las queries SQL de una entidad.
Los servicios nunca escriben SQL directamente.
"""

import sqlite3
from typing import Optional
from app.database.connection import get_connection
from app.models.entities import Libro, Usuario, Prestamo, Reserva, Historial


# ─────────────────────────────────────────────────────────────
# LIBRO REPOSITORY
# ─────────────────────────────────────────────────────────────

class LibroRepository:

    def create(self, libro: Libro) -> Libro:
        conn = get_connection()
        conn.execute(
            "INSERT INTO libros (isbn, titulo, autor, anio, copias, disponibles) VALUES (?,?,?,?,?,?)",
            (libro.isbn, libro.titulo, libro.autor, libro.anio, libro.copias, libro.copias)
        )
        conn.commit()
        conn.close()
        return libro

    def find_by_isbn(self, isbn: str) -> Optional[Libro]:
        conn = get_connection()
        row = conn.execute("SELECT * FROM libros WHERE isbn = ?", (isbn,)).fetchone()
        conn.close()
        return self._row_to_libro(row) if row else None

    def find_all(self) -> list[Libro]:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM libros ORDER BY titulo").fetchall()
        conn.close()
        return [self._row_to_libro(r) for r in rows]

    def search(self, query: str, campo: str = "titulo") -> list[Libro]:
        allowed = {"titulo", "autor", "isbn"}
        if campo not in allowed:
            campo = "titulo"
        conn = get_connection()
        rows = conn.execute(
            f"SELECT * FROM libros WHERE {campo} LIKE ? ORDER BY titulo",
            (f"%{query}%",)
        ).fetchall()
        conn.close()
        return [self._row_to_libro(r) for r in rows]

    def update_disponibles(self, isbn: str, delta: int) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE libros SET disponibles = disponibles + ? WHERE isbn = ?",
            (delta, isbn)
        )
        conn.commit()
        conn.close()

    def delete(self, isbn: str) -> bool:
        conn = get_connection()
        cursor = conn.execute("DELETE FROM libros WHERE isbn = ?", (isbn,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0

    @staticmethod
    def _row_to_libro(row: sqlite3.Row) -> Libro:
        return Libro(
            isbn=row["isbn"], titulo=row["titulo"], autor=row["autor"],
            anio=row["anio"], copias=row["copias"], disponibles=row["disponibles"],
            created_at=row["created_at"]
        )


# ─────────────────────────────────────────────────────────────
# USUARIO REPOSITORY
# ─────────────────────────────────────────────────────────────

class UsuarioRepository:

    def create(self, usuario: Usuario) -> Usuario:
        conn = get_connection()
        conn.execute(
            "INSERT INTO usuarios (id, nombre, correo) VALUES (?,?,?)",
            (usuario.id, usuario.nombre, usuario.correo)
        )
        conn.commit()
        conn.close()
        return usuario

    def find_by_id(self, uid: str) -> Optional[Usuario]:
        conn = get_connection()
        row = conn.execute("SELECT * FROM usuarios WHERE id = ?", (uid,)).fetchone()
        conn.close()
        return self._row_to_usuario(row) if row else None

    def find_all(self) -> list[Usuario]:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM usuarios ORDER BY nombre").fetchall()
        conn.close()
        return [self._row_to_usuario(r) for r in rows]

    @staticmethod
    def _row_to_usuario(row: sqlite3.Row) -> Usuario:
        return Usuario(id=row["id"], nombre=row["nombre"],
                       correo=row["correo"], created_at=row["created_at"])


# ─────────────────────────────────────────────────────────────
# PRESTAMO REPOSITORY
# ─────────────────────────────────────────────────────────────

class PrestamoRepository:

    def create(self, prestamo: Prestamo) -> Prestamo:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO prestamos (isbn, usuario_id) VALUES (?,?)",
            (prestamo.isbn, prestamo.usuario_id)
        )
        prestamo.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return prestamo

    def find_activos(self) -> list[Prestamo]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM prestamos WHERE activo = 1 ORDER BY fecha_prestamo DESC"
        ).fetchall()
        conn.close()
        return [self._row_to_prestamo(r) for r in rows]

    def find_activo_by_isbn_usuario(self, isbn: str, usuario_id: str) -> Optional[Prestamo]:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM prestamos WHERE isbn=? AND usuario_id=? AND activo=1",
            (isbn, usuario_id)
        ).fetchone()
        conn.close()
        return self._row_to_prestamo(row) if row else None

    def find_activos_por_usuario(self, usuario_id: str) -> list[Prestamo]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM prestamos WHERE usuario_id=? AND activo=1", (usuario_id,)
        ).fetchall()
        conn.close()
        return [self._row_to_prestamo(r) for r in rows]

    def marcar_devuelto(self, prestamo_id: int) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE prestamos SET activo=0, fecha_devolucion=datetime('now','localtime') WHERE id=?",
            (prestamo_id,)
        )
        conn.commit()
        conn.close()

    def count_activos(self) -> int:
        conn = get_connection()
        count = conn.execute("SELECT COUNT(*) FROM prestamos WHERE activo=1").fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def _row_to_prestamo(row: sqlite3.Row) -> Prestamo:
        return Prestamo(
            id=row["id"], isbn=row["isbn"], usuario_id=row["usuario_id"],
            fecha_prestamo=row["fecha_prestamo"], fecha_devolucion=row["fecha_devolucion"],
            activo=bool(row["activo"])
        )


# ─────────────────────────────────────────────────────────────
# RESERVA REPOSITORY
# ─────────────────────────────────────────────────────────────

class ReservaRepository:

    def create(self, reserva: Reserva) -> Reserva:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO reservas (isbn, usuario_id) VALUES (?,?)",
            (reserva.isbn, reserva.usuario_id)
        )
        reserva.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return reserva

    def find_pendientes_por_isbn(self, isbn: str) -> list[Reserva]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM reservas WHERE isbn=? AND atendida=0 ORDER BY fecha ASC",
            (isbn,)
        ).fetchall()
        conn.close()
        return [self._row_to_reserva(r) for r in rows]

    def find_todas_pendientes(self) -> list[Reserva]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM reservas WHERE atendida=0 ORDER BY fecha ASC"
        ).fetchall()
        conn.close()
        return [self._row_to_reserva(r) for r in rows]

    def marcar_atendida(self, reserva_id: int) -> None:
        conn = get_connection()
        conn.execute("UPDATE reservas SET atendida=1 WHERE id=?", (reserva_id,))
        conn.commit()
        conn.close()

    def count_pendientes(self) -> int:
        conn = get_connection()
        count = conn.execute("SELECT COUNT(*) FROM reservas WHERE atendida=0").fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def _row_to_reserva(row: sqlite3.Row) -> Reserva:
        return Reserva(
            id=row["id"], isbn=row["isbn"], usuario_id=row["usuario_id"],
            fecha=row["fecha"], atendida=bool(row["atendida"])
        )


# ─────────────────────────────────────────────────────────────
# HISTORIAL REPOSITORY
# ─────────────────────────────────────────────────────────────

class HistorialRepository:

    def create(self, entrada: Historial) -> Historial:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO historial (tipo, isbn, usuario_id, detalle) VALUES (?,?,?,?)",
            (entrada.tipo, entrada.isbn, entrada.usuario_id, entrada.detalle)
        )
        entrada.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return entrada

    def find_all(self, limit: int = 50) -> list[Historial]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT * FROM historial ORDER BY fecha DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        return [self._row_to_historial(r) for r in rows]

    def count(self) -> int:
        conn = get_connection()
        count = conn.execute("SELECT COUNT(*) FROM historial").fetchone()[0]
        conn.close()
        return count

    @staticmethod
    def _row_to_historial(row: sqlite3.Row) -> Historial:
        return Historial(
            id=row["id"], tipo=row["tipo"], isbn=row["isbn"],
            usuario_id=row["usuario_id"], detalle=row["detalle"], fecha=row["fecha"]
        )
