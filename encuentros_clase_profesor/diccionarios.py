#Diccionarios en Programación
# Par entre clave y un valor separado por :  y entre {}

libro= {"titulo": "La Hojarasca", "isbn": "978-3-16-148410-0", "autor": "Gabriel García Márquez"}
print(libro)

#----------------
#Sistema básico de Biblioteca con operaciones básicas

#----Zona de funciones ----

libros={}
usuarios={}

def agregar_libro():
    id=input( "Id libro: ")
    if id in libros:
        print("Ya existe un libro con ese ID")
        return
    libros[id] = {
        "titulo": input("Título del libro: "),
        "autor": input("Autor del libro: "),
        "disponible": True
    }
    print()
    print(f"libro '{libros[id]['titulo']}' Agregado")
    print("-----------------")
    print()
    print()

def agregar_usuario():
    id=input("id usuario: ")
    if id in usuarios:
        print("Ya existe un usuario con ese ID")
        return
    usuarios[id]= {
        "nombre" : input("Nombre del usuario: "),
        "prestamos": []
    }
    print()
    print(f"Usuario '{usuarios[id]['nombre']}' se agregó exitosamente")
    print("-----------------")
    

def listar_libros():
    if not libros:
        print("no hay libros registrados")
        return
    for id,l in libros.items():  #//recorremos el diccionario con items() para obtener clave y valor
        estado="disponible" if l["disponible"] else "Prestado"
        print()
        print(f"[{id}] {l['titulo']} - {l['autor']} - ({estado})")

def listar_usuarios():
    if not usuarios:
        print("No hay usuarios registrados")
        return
    for id,u in usuarios.items():
        print()
        print(f"[{id}] {u['nombre']} -- Préstamos: {u['prestamos'] or 'Ninguno'}")

def prestar_libro():
    uid=input("ID Usuario: ")
    bid=input("ID Libro: ")
    u=usuarios.get(uid)
    l=libros.get(bid)
    if not u:
        print("Usuario no encontrado");
        return
    if not l:
        print("Libro no encontrado");
        return
    if not l["disponible"]:
        print("Libro no disponible");
        return
    l["disponible"]=False
    u["prestamos"].append(bid) #agregamos el id del libro a la lista de préstamos del usuario
    print()
    print(f"Libro '{l['titulo']}' prestado a '{u['nombre']}'")
    print()




#-------Programa Principal-------
while True:
    print("Bienvenido a Nuestra Biblioteca Básica")
    print ("Menú de opciones")
    print("1. Agregar Libro")
    print("2. Agregar Usuario")
    print("3. Listar Libros")
    print("4. Listar Usuarios")
    print("5. Prestar Libro")
    print("6. Salir")

    op=input("Ingrese opción a Seleccionar: ")
    if op=="1":
        agregar_libro()

    elif op=="2":
        agregar_usuario()

    elif op=="3":
        listar_libros()

    elif op=="4":
        listar_usuarios()

    elif op=="5":
        prestar_libro()

    elif op=="6":
        print("Saliento- ...")
        break
    
    else:
        print("ha seleccionado una opción invalida")
    print()
