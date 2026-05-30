"""
app/services/services.py
Capa de lógica de negocio. Orquesta repositorios y aplica reglas del dominio.
Usa las estructuras de datos lineales en memoria como caché y para operaciones
que requieren orden específico (pila historial, cola reservas en sesión).
"""

from fastapi import HTTPException, status
from app.models.entities import Libro, Usuario, Prestamo, Reserva, Historial, Pila, Cola
from app.repositories.repositories import (
    LibroRepository, UsuarioRepository, PrestamoRepository,
    ReservaRepository, HistorialRepository
)
from app.schemas.schemas import (
    LibroCreate, UsuarioCreate, PrestamoCreate, ReservaCreate, MetricasResponse
)


# ─────────────────────────────────────────────────────────────
# LIBRO SERVICE
# ─────────────────────────────────────────────────────────────

class LibroService:

    def __init__(self):
        self._repo = LibroRepository()

    def registrar(self, data: LibroCreate) -> Libro:
        if self._repo.find_by_isbn(data.isbn):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El ISBN '{data.isbn}' ya existe en el catálogo."
            )
        libro = Libro(
            isbn=data.isbn, titulo=data.titulo, autor=data.autor,
            anio=data.anio, copias=data.copias, disponibles=data.copias
        )
        return self._repo.create(libro)

    def obtener_por_isbn(self, isbn: str) -> Libro:
        libro = self._repo.find_by_isbn(isbn)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado.")
        return libro

    def listar(self) -> list[Libro]:
        return self._repo.find_all()

    def buscar(self, query: str, campo: str = "titulo") -> list[Libro]:
        return self._repo.search(query, campo)

    def eliminar(self, isbn: str, prestamo_repo: PrestamoRepository) -> None:
        libro = self.obtener_por_isbn(isbn)
        activos = prestamo_repo.find_activos()
        if any(p.isbn == isbn for p in activos):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar: el libro tiene préstamos activos."
            )
        self._repo.delete(isbn)


# ─────────────────────────────────────────────────────────────
# USUARIO SERVICE
# ─────────────────────────────────────────────────────────────

class UsuarioService:

    def __init__(self):
        self._repo = UsuarioRepository()

    def registrar(self, data: UsuarioCreate) -> Usuario:
        if self._repo.find_by_id(data.id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El ID '{data.id}' ya está registrado."
            )
        usuario = Usuario(id=data.id, nombre=data.nombre, correo=data.correo)
        return self._repo.create(usuario)

    def obtener_por_id(self, uid: str) -> Usuario:
        usuario = self._repo.find_by_id(uid)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        return usuario

    def listar(self) -> list[Usuario]:
        return self._repo.find_all()


# ─────────────────────────────────────────────────────────────
# PRESTAMO SERVICE
# ─────────────────────────────────────────────────────────────

class PrestamoService:

    def __init__(self):
        self._repo       = PrestamoRepository()
        self._libro_repo = LibroRepository()
        self._user_repo  = UsuarioRepository()
        self._hist_repo  = HistorialRepository()
        self._reserva_repo = ReservaRepository()

    def prestar(self, data: PrestamoCreate) -> Prestamo:
        libro = self._libro_repo.find_by_isbn(data.isbn)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado.")
        if not self._user_repo.find_by_id(data.usuario_id):
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if not libro.esta_disponible():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sin copias disponibles. Puedes hacer una reserva."
            )

        self._libro_repo.update_disponibles(data.isbn, -1)
        prestamo = self._repo.create(Prestamo(id=None, isbn=data.isbn, usuario_id=data.usuario_id))

        self._hist_repo.create(Historial(
            id=None, tipo="PRÉSTAMO", isbn=data.isbn, usuario_id=data.usuario_id,
            detalle=f"Libro '{libro.titulo}' prestado a usuario {data.usuario_id}"
        ))
        return prestamo

    def devolver(self, isbn: str, usuario_id: str) -> Prestamo:
        prestamo = self._repo.find_activo_by_isbn_usuario(isbn, usuario_id)
        if not prestamo:
            raise HTTPException(status_code=404, detail="No se encontró préstamo activo.")

        self._repo.marcar_devuelto(prestamo.id)
        self._libro_repo.update_disponibles(isbn, +1)

        libro = self._libro_repo.find_by_isbn(isbn)
        self._hist_repo.create(Historial(
            id=None, tipo="DEVOLUCIÓN", isbn=isbn, usuario_id=usuario_id,
            detalle=f"Libro '{libro.titulo}' devuelto por usuario {usuario_id}"
        ))

        # Atender siguiente reserva pendiente (Cola FIFO desde BD)
        pendientes = self._reserva_repo.find_pendientes_por_isbn(isbn)
        if pendientes:
            primera = pendientes[0]
            self._reserva_repo.marcar_atendida(primera.id)
            self._hist_repo.create(Historial(
                id=None, tipo="RESERVA_ATENDIDA", isbn=isbn, usuario_id=primera.usuario_id,
                detalle=f"Reserva atendida para usuario {primera.usuario_id}"
            ))

        return prestamo

    def listar_activos(self) -> list[Prestamo]:
        return self._repo.find_activos()

    def listar_activos_por_usuario(self, usuario_id: str) -> list[Prestamo]:
        return self._repo.find_activos_por_usuario(usuario_id)


# ─────────────────────────────────────────────────────────────
# RESERVA SERVICE
# ─────────────────────────────────────────────────────────────

class ReservaService:

    def __init__(self):
        self._repo       = ReservaRepository()
        self._libro_repo = LibroRepository()
        self._user_repo  = UsuarioRepository()

    def reservar(self, data: ReservaCreate) -> Reserva:
        libro = self._libro_repo.find_by_isbn(data.isbn)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado.")
        if not self._user_repo.find_by_id(data.usuario_id):
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if libro.esta_disponible():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El libro está disponible. Usa préstamo directo."
            )
        reserva = Reserva(id=None, isbn=data.isbn, usuario_id=data.usuario_id)
        return self._repo.create(reserva)

    def listar_por_isbn(self, isbn: str) -> list[Reserva]:
        return self._repo.find_pendientes_por_isbn(isbn)

    def listar_todas(self) -> list[Reserva]:
        return self._repo.find_todas_pendientes()


# ─────────────────────────────────────────────────────────────
# HISTORIAL SERVICE
# ─────────────────────────────────────────────────────────────

class HistorialService:

    def __init__(self):
        self._repo = HistorialRepository()

    def listar(self, limit: int = 50) -> list[Historial]:
        return self._repo.find_all(limit)


# ─────────────────────────────────────────────────────────────
# MÉTRICAS SERVICE
# ─────────────────────────────────────────────────────────────

class MetricasService:

    def obtener(self) -> MetricasResponse:
        libro_repo   = LibroRepository()
        prestamo_repo = PrestamoRepository()
        reserva_repo = ReservaRepository()
        hist_repo    = HistorialRepository()

        libros = libro_repo.find_all()
        return MetricasResponse(
            total_libros      = len(libros),
            disponibles       = sum(l.disponibles for l in libros),
            total_usuarios    = len(UsuarioRepository().find_all()),
            prestamos_activos = prestamo_repo.count_activos(),
            total_reservas    = reserva_repo.count_pendientes(),
            total_historial   = hist_repo.count()
        )
