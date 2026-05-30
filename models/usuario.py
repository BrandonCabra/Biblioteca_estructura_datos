# Clase Usuario

class Usuario:
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario
        self.nombre = nombre
        # Estructura Lineal: Lista (Arreglo dinámico)
        # Permite agregar o remover elementos sin importar el orden estricto,
        # ideal ya que el usuario puede devolver cualquier libro en cualquier momento.
        self.libros_prestados = []

    def __str__(self):  # Este método especial nos permite imprimir el objeto de forma legible
        return f"[{self.id_usuario}] {self.nombre} - Préstamos activos: {len(self.libros_prestados)}"

