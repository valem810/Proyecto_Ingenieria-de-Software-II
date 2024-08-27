class ProblemaCaballos:
    def __init__(self, n):
        self.n = n
        self.tablero = [[0] * n for _ in range(n)]
        self.soluciones = []

    def resolver(self):
        max = self.cuantos_caballos()
        self.nCaballos(max, (0, 0))
        return max, self.soluciones

    def cuantos_caballos(self):
        if self.n == 1:
            return 1
        elif self.n == 2:
            return 4
        elif self.n % 2 == 0:
            return (self.n * self.n) // 2
        else:
            return (self.n * self.n) // 2 + 1

    def nCaballos(self, n_Caballos, posicion):
        if n_Caballos == 0:
            self.soluciones.append([row[:] for row in self.tablero])
            return

        i, j = posicion

        while i < self.n:
            while j < self.n:
                if self.validar_posicion((i, j)):
                    self.tablero[i][j] = 1
                    self.nCaballos(n_Caballos - 1, (i, j + 1))
                    self.tablero[i][j] = 0
                j += 1

            j = 0
            i += 1

    def validar_posicion(self, posicion):
        for i in range(self.n):
            for j in range(self.n):
                if self.tablero[i][j] == 1:
                    x = abs(i - posicion[0])
                    y = abs(j - posicion[1])
                    if (x == 2 and y == 1) or (x == 1 and y == 2):
                        return False
        return True


def mostrar_tableros(tablero, name_file):
    with open(name_file, "a") as archivo:
        archivo.write("\n")
        for fila in tablero:
            fila_str = " ".join(map(str, fila))
            archivo.write(fila_str + "\n")


def resolver_problema_caballos(n):
    problema = ProblemaCaballos(n)
    max, soluciones = problema.resolver()

    print(f"Número máximo de caballos colocados: {max}")
    print(f"Formas de colocar los caballos: {len(soluciones)}")

    if n <= 9:
        file_name = f"CABAL_0{n}.txt"
    else:
        file_name = f"CABAL_{n}.txt"

    with open(file_name, "a") as archivo:
        archivo.write(str(max) + "\n")
        archivo.write(str(len(soluciones)) + "\n")

    for solution in soluciones:
        mostrar_tableros(solution, file_name)
        print()