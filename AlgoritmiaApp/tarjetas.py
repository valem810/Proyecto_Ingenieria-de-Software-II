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

def leer_archivo(archivo) -> list[int]:
    try:
        # Leer las líneas del archivo
        lines = archivo.readlines()

        # Validación: verificar que el archivo tenga al menos dos líneas (una de encabezado y números)
        if len(lines) < 2:
            raise ValueError("El archivo no tiene suficientes líneas para procesarse. Se requiere al menos una línea de encabezado y números de tarjetas.")
        
        # Verificar que la primera línea sea un número que indique la cantidad de tarjetas
        cantidad_tarjetas = lines[0].strip()
        if not cantidad_tarjetas.isdigit():
            raise ValueError(f"La primera línea del archivo no es un número válido. Valor encontrado: {cantidad_tarjetas}")
        cantidad_tarjetas = int(cantidad_tarjetas)

        # Leer y validar el resto de líneas, asegurándose de que sean números enteros
        numeros = []
        for i, linea in enumerate(lines[1:], start=1):  # Empezar desde la segunda línea
            valor = linea.strip()
            if not valor.isdigit():
                raise ValueError(f"La línea {i + 1} contiene caracteres no válidos. Valor encontrado: {valor}")
            numeros.append(int(valor))

        # Validar que la cantidad de números coincida con el número de tarjetas indicado
        if len(numeros) != cantidad_tarjetas:
            raise ValueError(f"La cantidad de números en el archivo ({len(numeros)}) no coincide con la cantidad indicada en la primera línea ({cantidad_tarjetas}).")

        return numeros

    except ValueError as ve:
        # Captura cualquier error de conversión o formato
        raise ValueError(f"Error en el formato del archivo: {ve}")
    except Exception as e:
        # Captura cualquier otro tipo de error inesperado
        raise ValueError(f"Error inesperado al leer el archivo: {e}")

def cargar_archivo(nombre_archivo: str, arreglo: list[int]) -> None:
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(f"{len(arreglo)}\n")
        archivo.writelines(f"{elemento}\n" for elemento in arreglo)
