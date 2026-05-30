"""
app/controllers/routes.py
Controladores REST (FastAPI Routers).
Solo reciben el request HTTP, delegan al servicio y retornan la respuesta.
No contienen lógica de negocio.
"""

from fastapi import APIRouter
from app.schemas.schemas import (
    LibroCreate, LibroResponse,
    UsuarioCreate, UsuarioResponse,
    PrestamoCreate, PrestamoResponse,
    ReservaCreate, ReservaResponse,
    HistorialResponse, MetricasResponse, APIResponse
)
from app.services.services import (
    LibroService, UsuarioService, PrestamoService,
    ReservaService, HistorialService, MetricasService
)
from app.repositories.repositories import PrestamoRepository

router = APIRouter()

# ─── Instancias de servicios (inyección simple) ───────────────
libro_svc    = LibroService()
usuario_svc  = UsuarioService()
prestamo_svc = PrestamoService()
reserva_svc  = ReservaService()
historial_svc= HistorialService()
metricas_svc = MetricasService()


# ─────────────────────────────────────────────────────────────
# LIBROS
# ─────────────────────────────────────────────────────────────

@router.get("/libros", response_model=list[LibroResponse], tags=["Libros"])
def listar_libros():
    return libro_svc.listar()

@router.post("/libros", response_model=LibroResponse, status_code=201, tags=["Libros"])
def registrar_libro(data: LibroCreate):
    return libro_svc.registrar(data)

@router.get("/libros/buscar", response_model=list[LibroResponse], tags=["Libros"])
def buscar_libros(q: str, campo: str = "titulo"):
    return libro_svc.buscar(q, campo)

@router.get("/libros/{isbn}", response_model=LibroResponse, tags=["Libros"])
def obtener_libro(isbn: str):
    return libro_svc.obtener_por_isbn(isbn)

@router.delete("/libros/{isbn}", response_model=APIResponse, tags=["Libros"])
def eliminar_libro(isbn: str):
    libro_svc.eliminar(isbn, PrestamoRepository())
    return APIResponse(ok=True, mensaje="Libro eliminado del catálogo.")


# ─────────────────────────────────────────────────────────────
# USUARIOS
# ─────────────────────────────────────────────────────────────

@router.get("/usuarios", response_model=list[UsuarioResponse], tags=["Usuarios"])
def listar_usuarios():
    return usuario_svc.listar()

@router.post("/usuarios", response_model=UsuarioResponse, status_code=201, tags=["Usuarios"])
def registrar_usuario(data: UsuarioCreate):
    return usuario_svc.registrar(data)

@router.get("/usuarios/{uid}", response_model=UsuarioResponse, tags=["Usuarios"])
def obtener_usuario(uid: str):
    return usuario_svc.obtener_por_id(uid)


# ─────────────────────────────────────────────────────────────
# PRÉSTAMOS
# ─────────────────────────────────────────────────────────────

@router.get("/prestamos", response_model=list[PrestamoResponse], tags=["Préstamos"])
def listar_prestamos():
    return prestamo_svc.listar_activos()

@router.post("/prestamos", response_model=PrestamoResponse, status_code=201, tags=["Préstamos"])
def registrar_prestamo(data: PrestamoCreate):
    return prestamo_svc.prestar(data)

@router.put("/prestamos/devolver", response_model=APIResponse, tags=["Préstamos"])
def devolver_libro(data: PrestamoCreate):
    prestamo_svc.devolver(data.isbn, data.usuario_id)
    return APIResponse(ok=True, mensaje="Devolución registrada exitosamente.")

@router.get("/prestamos/usuario/{uid}", response_model=list[PrestamoResponse], tags=["Préstamos"])
def prestamos_por_usuario(uid: str):
    return prestamo_svc.listar_activos_por_usuario(uid)


# ─────────────────────────────────────────────────────────────
# RESERVAS
# ─────────────────────────────────────────────────────────────

@router.get("/reservas", response_model=list[ReservaResponse], tags=["Reservas"])
def listar_reservas():
    return reserva_svc.listar_todas()

@router.post("/reservas", response_model=ReservaResponse, status_code=201, tags=["Reservas"])
def registrar_reserva(data: ReservaCreate):
    return reserva_svc.reservar(data)

@router.get("/reservas/{isbn}", response_model=list[ReservaResponse], tags=["Reservas"])
def reservas_por_libro(isbn: str):
    return reserva_svc.listar_por_isbn(isbn)


# ─────────────────────────────────────────────────────────────
# HISTORIAL
# ─────────────────────────────────────────────────────────────

@router.get("/historial", response_model=list[HistorialResponse], tags=["Historial"])
def listar_historial(limit: int = 50):
    return historial_svc.listar(limit)


# ─────────────────────────────────────────────────────────────
# MÉTRICAS
# ─────────────────────────────────────────────────────────────

@router.get("/metricas", response_model=MetricasResponse, tags=["Sistema"])
def obtener_metricas():
    return metricas_svc.obtener()
