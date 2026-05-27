#construcción de menú
#1. Interfaz gráfica con tkinter
#2. Realizar una Interfaz de usuario con menu de selección con texto.

#menú con texto

def imprimir_menu():
    print("Seleccionaste un plato corriente")

#---- parte principal -----

print("Bienvenido a Nuestro Restaurante")
print("Menú de Opciones")
print("1. Corriente")
print("2. Punta Gorda Especial")
print("3. Pescado con arroz de coco")

op=input("Favor seleccione una opción en el menú")
if op=="1":
    imprimir_menu()
elif op=="2":
    print("Seleccionaste una Punta Gorda Especial")
elif op=="3":
    print("Seleccionaste un pescado con arroz de coco")
else:
    print("ha seleccionado una opción invalida")


