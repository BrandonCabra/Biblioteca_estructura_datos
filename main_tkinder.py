# interfaz con tkinter.py
# Archivo: main_tkinter.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from models.biblioteca import Biblioteca

class AplicacionBiblioteca:
    def __init__(self, root):
        self.biblio = Biblioteca() # Instanciamos nuestro modelo central
        self.root = root
        self.root.title("Gestión de Biblioteca - Estructuras de Datos")
        self.root.geometry("450x550") # Ajustamos el tamaño para los nuevos botones
        
        # Etiqueta de título principal
        tk.Label(root, text="📚 Sistema de Biblioteca (Tkinter)", font=("Arial", 16, "bold")).pack(pady=10)
        
        # --- SECCIÓN DE REGISTROS y LISTAS (Estructura: Listas/Arrays) ---
        frame_registros = tk.LabelFrame(root, text=" Administración General ", padx=10, pady=5)
        frame_registros.pack(pady=5, fill="x", padx=15)
        
        tk.Button(frame_registros, text="1. Registrar Libro", command=self.registrar_libro, width=22).grid(row=0, column=0, padx=5, pady=3)
        tk.Button(frame_registros, text="2. Registrar Usuario", command=self.registrar_usuario, width=22).grid(row=0, column=1, padx=5, pady=3)
        tk.Button(frame_registros, text="3. Listar Libros", command=self.listar_libros, width=22).grid(row=1, column=0, padx=5, pady=3)
        tk.Button(frame_registros, text="4. Listar Usuarios", command=self.listar_usuarios, width=22).grid(row=1, column=1, padx=5, pady=3)
        
        # --- SECCIÓN DE BÚSQUEDAS (Estructura: Listas/Búsqueda Lineal) ---
        frame_busquedas = tk.LabelFrame(root, text=" Consultas y Búsquedas ", padx=10, pady=5)
        frame_busquedas.pack(pady=5, fill="x", padx=15)
        
        tk.Button(frame_busquedas, text="5. Buscar Libro (ISBN)", command=self.buscar_libro, width=22).grid(row=0, column=0, padx=5, pady=3)
        tk.Button(frame_busquedas, text="6. Buscar Usuario (ID)", command=self.buscar_usuario, width=22).grid(row=0, column=1, padx=5, pady=3)

        # --- SECCIÓN DE OPERACIONES (Estructura: Pilas y Colas) ---
        frame_operaciones = tk.LabelFrame(root, text=" Préstamos y Flujos ", padx=10, pady=5)
        frame_operaciones.pack(pady=5, fill="x", padx=15)

        tk.Button(frame_operaciones, text="7. Prestar Libro (Colas)", command=self.prestar_libro, width=47).pack(pady=3)
        tk.Button(frame_operaciones, text="8. Devolver Libro (Pilas/Colas)", command=self.devolver_libro, width=47).pack(pady=3)
        tk.Button(frame_operaciones, text="9. Ver Última Devolución (Pila)", command=self.ver_historial, width=47).pack(pady=3)
        
        # Botón de Salida
        tk.Button(root, text="Salir del Sistema", command=root.quit, width=25, fg="white", bg="red").pack(pady=15)

    # --- 1 y 2. MÉTODOS DE REGISTRO ---
    def registrar_libro(self):
        isbn = simpledialog.askstring("Registrar", "Ingrese el ISBN del libro:")
        if isbn:
            titulo = simpledialog.askstring("Registrar", "Ingrese el Título:")
            autor = simpledialog.askstring("Registrar", "Ingrese el Autor:")
            if titulo and autor:
                mensaje = self.biblio.registrar_libro(isbn, titulo, autor)
                messagebox.showinfo("Éxito", mensaje)

    def registrar_usuario(self):
        id_usuario = simpledialog.askstring("Registrar", "Ingrese el ID del Usuario:")
        if id_usuario:
            nombre = simpledialog.askstring("Registrar", "Ingrese el Nombre Completo:")
            if nombre:
                mensaje = self.biblio.registrar_usuario(id_usuario, nombre)
                messagebox.showinfo("Éxito", mensaje)

    # --- 3 y 4. MÉTODOS DE LISTAR (Recorrido de Listas) ---
    def listar_libros(self):
        # Accedemos directamente a la lista 'catalogo' de nuestro modelo biblioteca
        if not self.biblio.catalogo:
            messagebox.showwarning("Catálogo", "No hay libros registrados en el sistema.")
            return
        
        # Concatenamos los textos gracias al método __str__ de la clase Libro
        lineas = [str(libro) for libro in self.biblio.catalogo]
        texto_completo = "\n".join(lineas)
        messagebox.showinfo("Catálogo de Libros", texto_completo)

    def listar_usuarios(self):
        # Accedemos directamente a la lista 'usuarios' de nuestro modelo biblioteca
        if not self.biblio.usuarios:
            messagebox.showwarning("Usuarios", "No hay usuarios registrados en el sistema.")
            return
        
        lineas = [str(usuario) for usuario in self.biblio.usuarios]
        texto_completo = "\n".join(lineas)
        messagebox.showinfo("Registro de Usuarios", texto_completo)

    # --- 5 y 6. MÉTODOS DE BÚSQUEDA ---
    def buscar_libro(self):
        isbn = simpledialog.askstring("Buscar", "Ingrese el ISBN del libro a buscar:")
        if isbn:
            libro = self.biblio.buscar_libro(isbn)
            if libro:
                # Mostramos la información completa y detallada del libro encontrado
                messagebox.showinfo("Libro Encontrado", str(libro))
            else:
                messagebox.showerror("Error", f"No se encontró ningún libro con el ISBN: {isbn}")

    def buscar_usuario(self):
        id_usuario = simpledialog.askstring("Buscar", "Ingrese el ID del usuario a buscar:")
        if id_usuario:
            usuario = self.biblio.buscar_usuario(id_usuario)
            if usuario:
                # Mostramos la información y préstamos activos del usuario
                info = str(usuario) + f"\nISBNs prestados: {usuario.libros_prestados or 'Ninguno'}"
                messagebox.showinfo("Usuario Encontrado", info)
            else:
                messagebox.showerror("Error", f"No se encontró ningún usuario con el ID: {id_usuario}")

    # --- 7, 8 y 9. FLUJOS COMPLEJOS (Pilas y Colas) ---
    def prestar_libro(self):
        isbn = simpledialog.askstring("Préstamo", "ISBN del libro solicitado:")
        id_usuario = simpledialog.askstring("Préstamo", "ID del usuario solicitante:")
        if isbn and id_usuario:
            mensaje = self.biblio.prestar_libro(isbn, id_usuario)
            messagebox.showinfo("Resultado del Préstamo", mensaje)

    def devolver_libro(self):
        isbn = simpledialog.askstring("Devolución", "ISBN del libro a devolver:")
        id_usuario = simpledialog.askstring("Devolución", "ID del usuario que devuelve:")
        if isbn and id_usuario:
            mensaje = self.biblio.devolver_libro(isbn, id_usuario)
            messagebox.showinfo("Resultado de la Devolución", mensaje)

    def ver_historial(self):
        mensaje = self.biblio.ver_ultima_devolucion()
        messagebox.showinfo("Historial (Pila LIFO)", mensaje)

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AplicacionBiblioteca(ventana_principal)
    ventana_principal.mainloop()