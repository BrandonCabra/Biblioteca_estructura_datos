# archivo principal que ejecuta el programa
# Archivo: main.py
from models.biblioteca import Biblioteca
from views.consola_view import mostrar_menu

def main_consola():
    # Instanciamos el "Cerebro" (El Modelo)
    mi_biblioteca = Biblioteca()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            print("\n-- REGISTRAR LIBRO --")
            isbn = input("ISBN: ")
            titulo = input("Título: ")
            autor = input("Autor: ")
            mensaje = mi_biblioteca.registrar_libro(isbn, titulo, autor)
            print(f"> {mensaje}")
            
        elif opcion == "2":
            print("\n-- REGISTRAR USUARIO --")
            id_usuario = input("ID de Usuario: ")
            nombre = input("Nombre completo: ")
            mensaje = mi_biblioteca.registrar_usuario(id_usuario, nombre)
            print(f"> {mensaje}")
            
        elif opcion == "3":
            print("\n-- PRESTAR LIBRO --")
            isbn = input("ISBN del libro a solicitar: ")
            id_usuario = input("ID del usuario que lo solicita: ")
            mensaje = mi_biblioteca.prestar_libro(isbn, id_usuario)
            print(f"> {mensaje}")
            
        elif opcion == "4":
            print("\n-- DEVOLVER LIBRO --")
            isbn = input("ISBN del libro a devolver: ")
            id_usuario = input("ID del usuario que lo devuelve: ")
            mensaje = mi_biblioteca.devolver_libro(isbn, id_usuario)
            print(f"> {mensaje}")
            
        elif opcion == "5":
            print("\n-- HISTORIAL DE DEVOLUCIONES --")
            mensaje = mi_biblioteca.ver_ultima_devolucion()
            print(f"> {mensaje}")
            
        elif opcion == "6":
            print("\nSaliendo del sistema... ¡Gracias por usar la Biblioteca!")
            break
        else:
            print("\n> Opción inválida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main_consola()