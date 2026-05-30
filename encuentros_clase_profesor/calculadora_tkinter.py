# uso de tkinter para crear una calculadora sencilla

import re
import tkinter as tk


def main():
	raiz = tk.Tk()
	raiz.title("Calculadora con Tkinter")
	raiz.resizable(0, 0)

	mi_frame = tk.Frame(raiz, padx=10, pady=10)
	mi_frame.pack()

	expresion = tk.StringVar()
	pantalla = tk.Entry(
		mi_frame,
		textvariable=expresion,
		font=("Consolas", 18),
		justify="right",
		bd=6,
		relief="sunken",
		width=17,
	)
	pantalla.grid(row=0, column=0, columnspan=4, padx=2, pady=(0, 8), ipady=6)

	def agregar_texto(texto):
		expresion.set(expresion.get() + texto)

	def limpiar():
		expresion.set("")

	def borrar_ultimo():
		expresion.set(expresion.get()[:-1])

	def calcular():
		expr = expresion.get().strip()
		if not expr:
			return

		expr = expr.replace("x", "*").replace("÷", "/")
		# Permitimos solo caracteres aritmeticos para evaluar de forma segura.
		if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
			expresion.set("Error")
			return

		try:
			resultado = eval(expr, {"__builtins__": {}}, {})
			if isinstance(resultado, float) and resultado.is_integer():
				resultado = int(resultado)
			expresion.set(str(resultado))
		except ZeroDivisionError:
			expresion.set("No se puede dividir por 0")
		except Exception:
			expresion.set("Error")

	def crear_boton(texto, fila, columna, comando, colspan=1, ancho=5):
		boton = tk.Button(
			mi_frame,
			text=texto,
			width=ancho,
			height=2,
			font=("Segoe UI", 11, "bold"),
			command=comando,
		)
		boton.grid(row=fila, column=columna, columnspan=colspan, padx=2, pady=2, sticky="nsew")

	crear_boton("C", 1, 0, limpiar)
	crear_boton("<-", 1, 1, borrar_ultimo)
	crear_boton("(", 1, 2, lambda: agregar_texto("("))
	crear_boton(")", 1, 3, lambda: agregar_texto(")"))

	crear_boton("7", 2, 0, lambda: agregar_texto("7"))
	crear_boton("8", 2, 1, lambda: agregar_texto("8"))
	crear_boton("9", 2, 2, lambda: agregar_texto("9"))
	crear_boton("/", 2, 3, lambda: agregar_texto("/"))

	crear_boton("4", 3, 0, lambda: agregar_texto("4"))
	crear_boton("5", 3, 1, lambda: agregar_texto("5"))
	crear_boton("6", 3, 2, lambda: agregar_texto("6"))
	crear_boton("x", 3, 3, lambda: agregar_texto("x"))

	crear_boton("1", 4, 0, lambda: agregar_texto("1"))
	crear_boton("2", 4, 1, lambda: agregar_texto("2"))
	crear_boton("3", 4, 2, lambda: agregar_texto("3"))
	crear_boton("-", 4, 3, lambda: agregar_texto("-"))

	crear_boton("0", 5, 0, lambda: agregar_texto("0"), colspan=2, ancho=12)
	crear_boton(".", 5, 2, lambda: agregar_texto("."))
	crear_boton("+", 5, 3, lambda: agregar_texto("+"))

	crear_boton("=", 6, 0, calcular, colspan=4, ancho=24)

	for i in range(4):
		mi_frame.grid_columnconfigure(i, weight=1)

	raiz.bind("<Return>", lambda event: calcular())
	raiz.mainloop()


if __name__ == "__main__":
	main()
