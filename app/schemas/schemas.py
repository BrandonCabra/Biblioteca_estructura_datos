"""
app/schemas/schemas.py
Schemas Pydantic para validación de request/response en la API REST.
Separan la representación de red de las entidades del dominio.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ─── REQUEST SCHEMAS ──────────────────────────────────────────

class LibroCreate(BaseModel):
    isbn:   str = Field(..., min_length=1, description="ISBN único del libro")
    titulo: str = Field(..., min_length=1)
    autor:  str = Field(..., min_length=1)
    anio:   Optional[str] = None
    copias: int = Field(1, ge=1)


class UsuarioCreate(BaseModel):
    id:     str = Field(..., min_length=1, description="ID único del usuario")
    nombre: str = Field(..., min_length=1)
    correo: Optional[str] = None


class PrestamoCreate(BaseModel):
    isbn:       str = Field(..., min_length=1)
    usuario_id: str = Field(..., min_length=1)


class ReservaCreate(BaseModel):
    isbn:       str = Field(..., min_length=1)
    usuario_id: str = Field(..., min_length=1)


# ─── RESPONSE SCHEMAS ─────────────────────────────────────────

class LibroResponse(BaseModel):
    isbn:        str
    titulo:      str
    autor:       str
    anio:        Optional[str]
    copias:      int
    disponibles: int
    created_at:  Optional[str]


class UsuarioResponse(BaseModel):
    id:         str
    nombre:     str
    correo:     Optional[str]
    created_at: Optional[str]


class PrestamoResponse(BaseModel):
    id:               Optional[int]
    isbn:             str
    usuario_id:       str
    fecha_prestamo:   Optional[str]
    fecha_devolucion: Optional[str]
    activo:           bool


class ReservaResponse(BaseModel):
    id:         Optional[int]
    isbn:       str
    usuario_id: str
    fecha:      Optional[str]
    atendida:   bool


class HistorialResponse(BaseModel):
    id:         Optional[int]
    tipo:       str
    isbn:       str
    usuario_id: str
    detalle:    Optional[str]
    fecha:      Optional[str]


class MetricasResponse(BaseModel):
    total_libros:      int
    disponibles:       int
    total_usuarios:    int
    prestamos_activos: int
    total_reservas:    int
    total_historial:   int


class APIResponse(BaseModel):
    """Wrapper genérico de respuesta."""
    ok:      bool
    mensaje: str
    data:    Optional[dict] = None
