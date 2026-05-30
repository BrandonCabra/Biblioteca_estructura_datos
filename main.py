# archivo principal que ejecuta el programa
# Archivo: main.py
# Archivo: main.py
from models.biblioteca import Biblioteca

def mostrar_menu():
    print("\n" + "="*50)
    print(" 📚 SISTEMA DE GESTIÓN DE BIBLIOTECA (MVC) 📚")
    print("="*50)
    print(" --- ADMINISTRACIÓN (Listas) ---")
    print("  1. Registrar nuevo libro")
    print("  2. Registrar nuevo usuario")
    print("  3. Listar todos los libros")
    print("  4. Listar todos los usuarios")
    print(" --- BÚSQUEDAS (Listas) ---")
    print("  5. Buscar libro por ISBN")
    print("  6. Buscar usuario por ID")
    print(" --- OPERACIONES (Pilas y Colas) ---")
    print("  7. Prestar libro (Usa Cola de espera - FIFO)")
    print("  8. Devolver libro (Usa Pilas y Colas)")
    print("  9. Ver última devolución (Usa Pila - LIFO)")
    print(" --- SALIR ---")
    print(" 10. Salir del sistema")
    print("="*50)
    return input("Seleccione una opción (1-10): ")

def main():
    # Instanciamos el "Cerebro" (El Modelo)
    mi_biblioteca = Biblioteca()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            print("\n--- REGISTRAR LIBRO ---")
            isbn = input("Ingrese el ISBN: ")
            titulo = input("Ingrese el Título: ")
            autor = input("Ingrese el Autor: ")
            mensaje = mi_biblioteca.registrar_libro(isbn, titulo, autor)
            print(f"> {mensaje}")
            
        elif opcion == "2":
            print("\n--- REGISTRAR USUARIO ---")
            id_usuario = input("Ingrese el ID de Usuario: ")
            nombre = input("Ingrese el Nombre completo: ")
            mensaje = mi_biblioteca.registrar_usuario(id_usuario, nombre)
            print(f"> {mensaje}")
            
        elif opcion == "3":
            print("\n--- CATÁLOGO DE LIBROS ---")
            if not mi_biblioteca.catalogo:
                print("> No hay libros registrados en el sistema.")
            else:
                for libro in mi_biblioteca.catalogo:
                    print(str(libro))
                    
        elif opcion == "4":
            print("\n--- REGISTRO DE USUARIOS ---")
            if not mi_biblioteca.usuarios:
                print("> No hay usuarios registrados en el sistema.")
            else:
                for usuario in mi_biblioteca.usuarios:
                    print(str(usuario))
                    
        elif opcion == "5":
            print("\n--- BUSCAR LIBRO ---")
            isbn = input("Ingrese el ISBN del libro a buscar: ")
            libro = mi_biblioteca.buscar_libro(isbn)
            if libro:
                print(f"> ENCONTRADO: {str(libro)}")
            else:
                print(f"> ERROR: No se encontró ningún libro con el ISBN '{isbn}'.")
                
        elif opcion == "6":
            print("\n--- BUSCAR USUARIO ---")
            id_usuario = input("Ingrese el ID del usuario a buscar: ")
            usuario = mi_biblioteca.buscar_usuario(id_usuario)
            if usuario:
                print(f"> ENCONTRADO: {str(usuario)}")
                print(f"  Préstamos activos (ISBNs): {usuario.libros_prestados or 'Ninguno'}")
            else:
                print(f"> ERROR: No se encontró ningún usuario con el ID '{id_usuario}'.")
            
        elif opcion == "7":
            print("\n--- PRESTAR LIBRO ---")
            isbn = input("Ingrese el ISBN del libro a solicitar: ")
            id_usuario = input("Ingrese el ID del usuario que lo solicita: ")
            mensaje = mi_biblioteca.prestar_libro(isbn, id_usuario)
            print(f"> {mensaje}")
            
        elif opcion == "8":
            print("\n--- DEVOLVER LIBRO ---")
            isbn = input("Ingrese el ISBN del libro a devolver: ")
            id_usuario = input("Ingrese el ID del usuario que lo devuelve: ")
            mensaje = mi_biblioteca.devolver_libro(isbn, id_usuario)
            print(f"> {mensaje}")
            
        elif opcion == "9":
            print("\n--- HISTORIAL DE DEVOLUCIONES ---")
            mensaje = mi_biblioteca.ver_ultima_devolucion()
            print(f"> {mensaje}")
            
        elif opcion == "10":
            print("\nSaliendo del sistema... ¡Gracias por usar la Biblioteca!")
            break
            
        else:
            print("\n> Opción inválida. Por favor, intente de nuevo ingresando un número del 1 al 10.")

if __name__ == "__main__":
    main()