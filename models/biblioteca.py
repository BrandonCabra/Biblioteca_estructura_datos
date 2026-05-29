# Aquí van las estructuras de datos como listas, pilas y colas

from models.libro import Libro
from models.usuario import Usuario

class Biblioteca:
    def __init__(self):
        # Estructura Lineal: Listas (Para búsquedas iterativas)
        self.catalogo = []
        self.usuarios = []
        
        # Estructura Lineal: Pila / Stack (Comportamiento LIFO) Guardará el registro de los últimos libros devueltos
        self.historial_devoluciones = []

    # --- MÉTODOS DE REGISTRO (Usando Listas) ---
    def registrar_libro(self, isbn, titulo, autor):
        nuevo_libro = Libro(isbn, titulo, autor)
        self.catalogo.append(nuevo_libro)
        return f"Libro '{titulo}' registrado con éxito."

    def registrar_usuario(self, id_usuario, nombre):
        nuevo_usuario = Usuario(id_usuario, nombre)
        self.usuarios.append(nuevo_usuario)
        return f"Usuario '{nombre}' registrado con éxito."

    # --- MÉTODOS DE BÚSQUEDA (Iterando Listas) ---
    def buscar_libro(self, isbn):
        for libro in self.catalogo:
            if libro.isbn == isbn:
                return libro
        return None

    def buscar_usuario(self, id_usuario):
        for usuario in self.usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        return None

    # --- LÓGICA PRINCIPAL: PRÉSTAMOS, RESERVAS (Colas) Y DEVOLUCIONES (Pilas) ---
    def prestar_libro(self, isbn, id_usuario):
        libro = self.buscar_libro(isbn)
        usuario = self.buscar_usuario(id_usuario)

        if not libro or not usuario:
            return "Error: Libro o Usuario no encontrado."

        if libro.disponible:
            libro.disponible = False
            usuario.libros_prestados.append(libro.isbn)
            return f"Éxito: El libro '{libro.titulo}' ha sido prestado a {usuario.nombre}."
        else:
            # Si no está disponible, usamos la COLA del libro
            libro.agregar_reserva(usuario.id_usuario)
            return f"El libro no está disponible. {usuario.nombre} ha sido añadido a la COLA de espera."

    def devolver_libro(self, isbn, id_usuario):
        libro = self.buscar_libro(isbn)
        usuario = self.buscar_usuario(id_usuario)

        if not libro or not usuario:
            return "Error: Libro o Usuario no encontrado."

        if isbn in usuario.libros_prestados:
            usuario.libros_prestados.remove(isbn)
            
            # 1. Agregamos el libro a la PILA de historial (Push)
            self.historial_devoluciones.append(libro.titulo)

            # 2. Revisamos si hay alguien en la COLA de espera para este libro
            siguiente_usuario_id = libro.obtener_siguiente_reserva()
            
            if siguiente_usuario_id:
                # Se lo prestamos automáticamente al primero de la cola (FIFO)
                siguiente_usuario = self.buscar_usuario(siguiente_usuario_id)
                siguiente_usuario.libros_prestados.append(libro.isbn)
                return f"Devolución exitosa. El libro '{libro.titulo}' fue reasignado automáticamente a {siguiente_usuario.nombre} (estaba en la cola)."
            else:
                # Si no hay nadie en la cola, el libro vuelve a estar disponible
                libro.disponible = True
                return f"Devolución exitosa. El libro '{libro.titulo}' ahora está disponible en el catálogo."
        else:
            return "Error: Este usuario no tiene prestado este libro."

    def ver_ultima_devolucion(self):
        """Muestra el último elemento de la pila (LIFO) sin borrarlo."""
        if self.historial_devoluciones:
            return f"El último libro devuelto a la biblioteca fue: '{self.historial_devoluciones[-1]}'"
        return "El historial de devoluciones está vacío."