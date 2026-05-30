"""
app/models/entities.py
Entidades del dominio. Estructuras de datos lineales implementadas como clases
puras de Python, sin dependencia de frameworks ni de la capa de persistencia.
"""

from dataclasses import dataclass, field
from typing import Optional


# ─────────────────────────────────────────────────────────────
# ENTIDADES DEL DOMINIO
# ─────────────────────────────────────────────────────────────

@dataclass
class Libro:
    isbn: str
    titulo: str
    autor: str
    anio: str
    copias: int
    disponibles: int
    created_at: Optional[str] = None

    def esta_disponible(self) -> bool:
        return self.disponibles > 0


@dataclass
class Usuario:
    id: str
    nombre: str
    correo: Optional[str]
    created_at: Optional[str] = None


@dataclass
class Prestamo:
    id: Optional[int]
    isbn: str
    usuario_id: str
    fecha_prestamo: Optional[str] = None
    fecha_devolucion: Optional[str] = None
    activo: bool = True


@dataclass
class Reserva:
    id: Optional[int]
    isbn: str
    usuario_id: str
    fecha: Optional[str] = None
    atendida: bool = False


@dataclass
class Historial:
    id: Optional[int]
    tipo: str          # "PRÉSTAMO" | "DEVOLUCIÓN" | "RESERVA"
    isbn: str
    usuario_id: str
    detalle: Optional[str] = None
    fecha: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# ESTRUCTURAS DE DATOS LINEALES
# ─────────────────────────────────────────────────────────────

class Nodo:
    """Nodo genérico para Lista Enlazada, Pila y Cola."""
    def __init__(self, dato):
        self.dato = dato
        self.siguiente: Optional["Nodo"] = None


class ListaEnlazada:
    """
    Lista enlazada simple genérica.
    HEAD → Nodo1 → Nodo2 → ... → NULL
    Complejidades: agregar O(n), buscar O(n), eliminar O(n)
    """

    def __init__(self):
        self.cabeza: Optional[Nodo] = None
        self.tamanio: int = 0

    def agregar(self, dato) -> None:
        nuevo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.tamanio += 1

    def buscar(self, clave, campo: str):
        actual = self.cabeza
        while actual:
            if str(getattr(actual.dato, campo, "")) == str(clave):
                return actual.dato
            actual = actual.siguiente
        return None

    def listar(self) -> list:
        elementos, actual = [], self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def eliminar(self, clave, campo: str) -> bool:
        if self.cabeza is None:
            return False
        if str(getattr(self.cabeza.dato, campo, "")) == str(clave):
            self.cabeza = self.cabeza.siguiente
            self.tamanio -= 1
            return True
        actual = self.cabeza
        while actual.siguiente:
            if str(getattr(actual.siguiente.dato, campo, "")) == str(clave):
                actual.siguiente = actual.siguiente.siguiente
                self.tamanio -= 1
                return True
            actual = actual.siguiente
        return False


class Pila:
    """
    Pila LIFO genérica.
    CIMA → Nodo1 → Nodo2 → ... → BASE
    Complejidades: apilar O(1), desapilar O(1)
    """

    def __init__(self):
        self.cima: Optional[Nodo] = None
        self.tamanio: int = 0

    def apilar(self, dato) -> None:
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cima
        self.cima = nuevo
        self.tamanio += 1

    def desapilar(self):
        if self.esta_vacia():
            return None
        dato = self.cima.dato
        self.cima = self.cima.siguiente
        self.tamanio -= 1
        return dato

    def ver_cima(self):
        return self.cima.dato if self.cima else None

    def esta_vacia(self) -> bool:
        return self.cima is None

    def listar(self) -> list:
        elementos, actual = [], self.cima
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos


class Cola:
    """
    Cola FIFO genérica.
    FRENTE → Nodo1 → Nodo2 → ... → FINAL
    Complejidades: encolar O(1), desencolar O(1)
    """

    def __init__(self):
        self.frente: Optional[Nodo] = None
        self.final:  Optional[Nodo] = None
        self.tamanio: int = 0

    def encolar(self, dato) -> None:
        nuevo = Nodo(dato)
        if self.final:
            self.final.siguiente = nuevo
        self.final = nuevo
        if self.frente is None:
            self.frente = nuevo
        self.tamanio += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.frente.dato
        self.frente = self.frente.siguiente
        if self.frente is None:
            self.final = None
        self.tamanio -= 1
        return dato

    def esta_vacia(self) -> bool:
        return self.frente is None

    def listar(self) -> list:
        elementos, actual = [], self.frente
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos
