from tkinter import *
 
raiz=Tk()
miFrame=Frame(raiz)
miFrame.pack()
 
operacion=""
resultado=0
numeroPantalla=StringVar()
pantalla=Entry(miFrame, textvariable=numeroPantalla)
pantalla.grid(row=1,column=1,padx=10,pady=10,columnspan=4)
pantalla.config(background="white",justify="right")
 
def numeroPulsado(num):
    global operacion
    if operacion != "":
        numeroPantalla.set(num)
    else:
        numeroPantalla.set(numeroPantalla.get()+num)
def suma(num):
    global operacion
    global resultado
    resultado=resultado+int(num)
    operacion="resta"
    numeroPantalla.set(resultado)
def elresultado():
    global resultado
    numeroPantalla.set(resultado+int(numeroPantalla.get()))
    resultado=0

 
#Creamos los botones de la fila del 7
boton7=Button(miFrame,text='7',width=10, command=lambda:numeroPulsado("7"))
boton7.grid(row=2,column=1)
boton8=Button(miFrame,text='8',width=10, command=lambda:numeroPulsado("8"))
boton8.grid(row=2,column=2)
boton9=Button(miFrame,text='9',width=10)
boton9.grid(row=2,column=3)
division=Button(miFrame,text="/",width=10)
division.grid(row=2,column=4)
#crearemos los botones de la fila del 4
boton4=Button(miFrame,text='4',width=10)
boton4.grid(row=3,column=1)
boton5=Button(miFrame,text='5',width=10)
boton5.grid(row=3,column=2)
boton6=Button(miFrame,text='6',width=10)
boton6.grid(row=3,column=3)
multi=Button(miFrame,text="X",width=10)
multi.grid(row=3,column=4)
 
#creamos los borones de la fila del 1
boton1=Button(miFrame,text='1',width=10)
boton1.grid(row=4,column=1)
boton2=Button(miFrame,text='2',width=10)
boton2.grid(row=4,column=2)
boton3=Button(miFrame,text='3',width=10)
boton3.grid(row=4,column=3)
resta=Button(miFrame,text='-',width=10)
resta.grid(row=4,column=4)
#creamos la fila del 0
boton0=Button(miFrame,text='0',width=10)
boton0.grid(row=5,column=1)
botoncoma=Button(miFrame,text=',',width=10)
botoncoma.grid(row=5,column=2)
botonigual=Button(miFrame,text='=',width=10, command=lambda:elresultado())
botonigual.grid(row=5,column=3)
botonmas=Button(miFrame,text='+',width=10, command=lambda:suma(numeroPantalla.get()))
botonmas.grid(row=5,column=4)
 
 
 
 
 
 
 
raiz.mainloop()