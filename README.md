# Biblioteca_estructura_datos

# 📚 Sistema de Gestión de Biblioteca - Estructuras de Datos

Este proyecto es un prototipo funcional de un Sistema de Gestión de Biblioteca desarrollado en Python. Su objetivo principal es demostrar la aplicación práctica de **Estructuras de Datos Lineales** (Listas, Pilas y Colas) y los principios de la **Programación Orientada a Objetos (POO)**

## 🚀 Características Principales

El sistema incluye una interfaz gráfica de usuario (GUI) amigable que permite realizar las siguientes operaciones:

* **Gestión de Catálogo y Usuarios:** Registro de nuevos libros (ISBN, título, autor) y usuarios (ID, nombre).
* **Consultas:** Listado completo y búsqueda específica de libros y usuarios registrados.
* **Préstamos y Reservas (Uso de Colas):** Permite prestar libros. Si un libro no está disponible, el usuario ingresa a una lista de espera justa bajo el principio FIFO (First In, First Out).
* **Devoluciones Automáticas:** Al devolver un libro, el sistema verifica la lista de espera y lo reasigna automáticamente al siguiente usuario en la cola.
* **Historial de Devoluciones (Uso de Pilas):** Registra los libros devueltos, permitiendo consultar la última devolución realizada bajo el principio LIFO (Last In, First Out).

## 🧠 Estructuras de Datos Implementadas

El núcleo de este sistema se basa en la correcta parametrización de los datos:

1.  **Listas (Arrays Dinámicos):** Utilizadas para almacenar el catálogo general de libros y el registro de usuarios. Permiten una iteración rápida y búsquedas lineales eficientes por atributos (ID o ISBN).
2.  **Colas (`collections.deque`):** Implementadas dentro de cada objeto `Libro` para gestionar la lista de espera. Garantizan una complejidad de O(1) al retirar el primer elemento, respetando el modelo FIFO.
3.  **Pilas (Stacks):** Implementadas mediante listas restringidas (uso exclusivo de `append` y acceso al índice `[-1]`) para gestionar el historial de las devoluciones más recientes (modelo LIFO).

## 📂 Estructura del Proyecto

El proyecto está modularizado separando la lógica de los datos de la interfaz de usuario:

```text
gestion_biblioteca/
├── models/                   # Modelo (Cerebro y Estructuras de Datos)
│   ├── libro.py              # Clase Libro (Contiene la Cola de espera)
│   ├── usuario.py            # Clase Usuario
│   └── biblioteca.py         # Lógica central (Listas generales y Pila de historial)
├── main_tkinter.py           # Vista/Controlador (Interfaz gráfica y ejecución)
└── README.md                 # Documentación del proyecto


## 🛠️ Requisitos e Instalación
Este proyecto fue desarrollado utilizando herramientas nativas de Python, por lo que no requiere la instalación de librerías externas de terceros.

Python: Versión 3.x o superior.

Tkinter: Librería estándar de Python para interfaces gráficas (normalmente preinstalada con Python).

## ▶️ Cómo ejecutar el proyecto
Clona este repositorio o descarga los archivos en tu máquina local.

Abre una terminal y navega hasta el directorio raíz del proyecto.

Ejecuta el archivo principal con el siguiente comando:

Bash
python main_tkinter.py

📝Proyecto académico para el curso de Estructura de Datos.