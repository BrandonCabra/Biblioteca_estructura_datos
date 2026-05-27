#menú para agregar libro, agregar ususario, listar libro y listar ususarios

libros=[]
usuarios=[]

def agregar_libro():
    id_libro=input("Ingrese ID del Libro: ")
    titulo_libro=input("Ingrese Título del Libro: ")
    autor_libro=input("Ingrese Autor del Libro: ")
    #isbn
    #volumen, etc
    for l in libros:
        if l["id"]==id_libro:
            print()
            print("Ya existe un libro con ese ID")
            print()
            return
    libros.append({"id":id_libro, "titulo":titulo_libro, "autor":autor_libro, "disponible":True})
    print()
    print(f"Libro agregado: {libros}")
    print()

def listar_libros():
    if not libros:
        print("No hay libros registrados")
    for l in libros:
        estado= "Disponible" if l["disponible"] else "Prestado"
        print()
        print(f"--ID: {l['id']} ** Título: {l['titulo']} ** Autor: {l['autor']} ** Estado: {estado}--")
        print()

#---- parte principal -----

while True:
    print("Bienvenido a la Biblioteca Re Básica")
    print("1. Agregar Libro")
    print("2. Agregar Usuario")
    print("3. Listar Libros")
    print("4. Listar Usuarios")
    print("5. Salir")
    op=input("Favor seleccione una opción: ")
    if op=="1":
        agregar_libro()

    elif op=="2":
        print("Seleccionaste Agregar Usuario")

    elif op=="3":
        listar_libros()


    elif op=="5":
        print("Gracias por visitar nuestra Biblioteca, Saliendo del sistema")
        break
    
    else:
        print("ha seleccionado una opción invalida")


