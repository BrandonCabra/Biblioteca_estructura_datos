# Clase Libro

from collections import deque

class Libro:
    def __init__(self, isbn, titulo, autor):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.disponible = True
        
        # Estructura Lineal: Cola (Queue) implementada con deque
        # Garantiza el principio FIFO (First In, First Out)
        self.cola_espera = deque()

    def agregar_reserva(self, id_usuario):
        """Agrega un usuario al final de la cola (In)."""
        self.cola_espera.append(id_usuario)

    def obtener_siguiente_reserva(self):
        """Retira y devuelve al primer usuario de la cola (Out)."""
        if self.cola_espera:
            # popleft() extrae el elemento del extremo izquierdo (el más antiguo)
            return self.cola_espera.popleft()
        return None

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        espera = len(self.cola_espera)
        return f"[{self.isbn}] {self.titulo} por {self.autor} - {estado} (En espera: {espera})"