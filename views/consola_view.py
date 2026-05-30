# Los menús y mensajes en pantalla

def mostrar_menu():
    print("\n" + "="*45)
    print(" 📚 SISTEMA DE GESTIÓN DE BIBLIOTECA (MVC) 📚")
    print("="*45)
    print("1. Registrar nuevo libro")
    print("2. Registrar nuevo usuario")
    print("3. Prestar libro (Usa Colas de espera)")
    print("4. Devolver libro (Usa Pilas y Colas)")
    print("5. Ver última devolución (Pila - LIFO)")
    print("6. Salir")
    print("="*45)
    return input("Seleccione una opción: ")