# esta es la que llama a la mera mera de tarjetas, para que cuando la metas al menu solo llames a tarjetas()

# para que funke ocupas el archivo de entrada, lo llamas como gustes nomas pones

def tarjetas() -> None:
    archivo = input("Ingrese el nombre del archivo con extension .in a leer (solo el nombre sin extension): ")
    entrada = archivo + ".in"
    salida = archivo + ".out"

    arreglo = leer_archivo(entrada)
    nuevos_indices = cards_problem(arreglo)

    cargar_archivo(salida, nuevos_indices)
    print(len(arreglo) - len(nuevos_indices), "tarjetas descartadas de la lista")

    print("Tarjetas restantes: ")
    for idx in nuevos_indices:
        print(arreglo[idx], end=", ")

def cards_problem(arr: list[int]) -> list[int]:
    n = len(arr)
    lis, tail, prev = [], [0] * n, [-1] * n
    len_size = 1

    def binary_search(left: int, right: int, key: int) -> int:
        while left < right:
            mid = (left + right) // 2
            if arr[tail[mid]] < key:
                left = mid + 1
            else:
                right = mid
        return left

    for i in range(1, n):
        if arr[i] < arr[tail[0]]:
            tail[0] = i
        elif arr[i] >= arr[tail[len_size - 1]]:
            prev[i], tail[len_size] = tail[len_size - 1], i
            len_size += 1
        else:
            pos = binary_search(0, len_size - 1, arr[i])
            prev[i], tail[pos] = tail[pos - 1], i

    idx = tail[len_size - 1]
    while idx != -1:
        lis.append(idx)
        idx = prev[idx]

    return lis[::-1]

def leer_archivo(nombre_archivo: str) -> list[int]:
    try:
        with open(nombre_archivo, 'r') as archivo:
            return [int(linea.strip()) for linea in archivo.readlines()[1:]]
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no se encuentra.")
        # Puedes manejar la excepción de la manera que consideres adecuada.
        # Puede ser salir del programa, pedir al usuario que proporcione el archivo correcto, etc.
        exit()

def cargar_archivo(nombre_archivo: str, arreglo: list[int]) -> None:
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(f"{len(arreglo)}\n")
        archivo.writelines(f"{elemento}\n" for elemento in arreglo)