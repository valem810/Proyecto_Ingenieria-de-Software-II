from caballos import resolver_problema_caballos
from tarjetas import *

while True:
    
    print("********MENU*************")
    print("1. Resolver el problema de los n Caballos.")
    print("2. Resolver el problema de la lista de tarjetas.")
    print("3. Terminar la ejecucion.")

    opc = int(input("Elija una opcion:"))

    if opc == 1:
        print("\n EL PROBLEMA DE LOS N CABALLOS")
        n = int(input("Ingrese el tamaño del tablero: "))
        resolver_problema_caballos(n)
        print("\n")
    elif opc == 2:
        print("\n LA LISTA DE TARJETAS")
        tarjetas()
        print("\n")
    elif opc == 3:
        break
