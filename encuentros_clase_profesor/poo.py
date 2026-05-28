
# #Programación Orientada a Objetos
# Objetos con atributos y métodos / Clases como molde para crear objetos
#----Ejemplo de clase Cuenta Bancaria ----
"""
class CuentaBancaria:
    def __init__(self, titular, saldo=0):  #Constructor para inicializar los atributos de la clase
        self.titular = titular  #Atributo para almacenar el nombre del titular de la cuenta
        self.saldo = saldo  #Atributo para almacenar el saldo de la cuenta, con un valor predeterminado de 0
        print(f"Cuenta de {self.titular} Creada con exito y su saldo es: {self.saldo}")

    def depositar(self, cantidad): #Método para depositar dinero en la cuenta
        if cantidad > 0:
            self.saldo += cantidad
            print(f"Depósito exitoso. Nuevo saldo: {self.saldo}")
        else:
            print("La cantidad a depositar debe ser mayor a cero.")
    
    def retirar(self, cantidad): #Método para retirar dinero de la cuenta
        if cantidad > self.saldo:
            print("Fondos insuficientes")
        else:
            self.saldo -= cantidad
            print(f"Retiro exitoso. Nuevo saldo: {self.saldo}")
    
    def transferir(self,otra_cuenta,monto):
        if monto<=0:
            print("Monto Inválido.")
        elif monto>self.saldo:
            print("Fondos insuficientes para la transferencia.")
        else:
            self.saldo-=monto
            otra_cuenta.saldo += monto
            print(f"Transferencia exitosa de ${monto} a la cuenta realizado con exito")
    
    def mostrar_saldo(self): #Método para mostrar el saldo actual de la cuenta
        print(f" {self.titular}, tu saldo actual es: {self.saldo}")



#----Instancia de la clase CuentaBancaria ----
cuenta1 = CuentaBancaria("José", 50000)

#----Uso del método depositar ----
cuenta1.depositar(10000)

#----Uso del método retirar ----
cuenta1.retirar(25000)

#----transferencia
cuenta1.transferir("maria", 1000)

#----Uso del método mostrar_saldo ----
cuenta1.mostrar_saldo()
"""

#_____________________________________
#Cuenta con Clientes
class Cliente:
    def __init__(self, nombre, dni):
        self.nombre = nombre
        self.dni = dni
        self.cuentas=[] #Lista para almacenar las cuentas del cliente
    
    def agregar_cuenta (self, cuenta):
        self.cuentas.append(cuenta) #Agrega una cuenta a la lista de cuentas del cliente


    def mostrar_cuentas(self):
        print(f"\nCuentas de {self.nombre}: ")
        if not self.cuentas:
            print("No tiene cuentas registradas.")
        for cuenta in self.cuentas:
            cuenta.mostrar_informacion() #lo construimos en la clase cuenta bancaria
            print(f"Cuenta con saldo: {cuenta.saldo}")
    
class CuentaBancaria:
    def __init__(self, numero_cuenta, cliente, saldo_inicial=0):
        self.numero_cuenta = numero_cuenta
        self.cliente = cliente
        self.saldo = saldo_inicial
        cliente.agregar_cuenta(self) #Agrega la cuenta al cliente automáticamente al crearla

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
            print(f"Depósito de ${monto} realizado correctamente.")
        else:
            print("Monto inválido.")
        
    def retirar(self, monto):
        if monto <= 0:
            print("Monto inválido.")
        elif monto > self.saldo:
            print("Fondos insuficientes.")
        else:
            self.saldo-=monto
            print(f"Retiro de ${monto} realizado correctamente.")

            
    def transferir(self, otra_cuenta, monto):
        if monto <= 0:
            print("Monto inválido.")
        elif monto > self.saldo:
            print("Fondos insuficientes para la transferencia.")
        else:
            self.saldo-=monto
            otra_cuenta.saldo+=monto #Deposita el monto en la otra cuenta
            print(f"Transferencia de ${monto} a la cuenta {otra_cuenta.numero_cuenta} realizada con exito.")

    def mostrar_informacion(self):
        print(f"Cuenta: {self.numero_cuenta}: saldo {self.saldo}")


cliente1=Cliente("Laura", "1234A")
cliente2=Cliente("Carlos", "5678B")

#cuentas asociadas
cuenta1= CuentaBancaria("0001", cliente1, 50000)
cuenta2= CuentaBancaria("0002", cliente1, 30000)
cuenta3= CuentaBancaria("0003", cliente2, 15000)

#oPERACIONES
cuenta1.depositar(300)
cuenta1.retirar(2000)
cuenta1.transferir(cuenta3, 5000)

#mostrar información
cliente1.mostrar_cuentas()
cliente2.mostrar_cuentas()


'''
#----Instancia de la clase Cliente ----
cliente1 = Cliente("Ana", "12345678")
#----Creación de cuentas para el cliente ----
cuenta2 = Cliente.CuentaBancaria("001", cliente1, 30000)
cuenta3 = Cliente.CuentaBancaria("002", cliente1, 15000)
#----Agregamos las cuentas al cliente ----
cliente1.agregar_cuenta(cuenta2)
'''