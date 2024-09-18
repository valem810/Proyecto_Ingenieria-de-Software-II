import base64

class ProblemaCaballos:
    def __init__(self, n):
        self.n = n
        self.tablero = [[0] * n for _ in range(n)]
        self.soluciones = []

    def resolver(self):
        max_caballos = self.cuantos_caballos()
        self.nCaballos(max_caballos, (0, 0))
        return max_caballos, self.soluciones

    def cuantos_caballos(self):
        if self.n == 1:
            return 1
        elif self.n == 2:
            return 4
        elif self.n % 2 == 0:
            return (self.n * self.n) // 2
        else:
            return (self.n * self.n) // 2 + 1

    def nCaballos(self, n_caballos, posicion):
        if n_caballos == 0:
            self.soluciones.append([row[:] for row in self.tablero])
            return

        i, j = posicion

        while i < self.n:
            while j < self.n:
                if self.validar_posicion((i, j)):
                    self.tablero[i][j] = 1
                    self.nCaballos(n_caballos - 1, (i, j + 1))
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

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def mostrar_tableros(tablero, archivo):
    archivo.write('<div style="margin-bottom: 20px;">\n')  # Contenedor con margen inferior
    archivo.write('<table border="1" cellpadding="10" cellspacing="0">\n')  # Tabla para el tablero
    for fila in tablero:
        archivo.write("<tr>\n")
        for celda in fila:
            if celda == 1:
                archivo.write('<td style="width: 40px; height: 40px; text-align: center;">')
                archivo.write('<img src="/media/images/chess-knight-svgrepo-com.svg" alt="Knight" style="width: 30px; height: 30px;" />')
                archivo.write("</td>\n")
            else:
                archivo.write('<td style="width: 40px; height: 40px; text-align: center;">&nbsp;</td>\n')  # Celda vacía
        archivo.write("</tr>\n")
    archivo.write("</table>\n")
    archivo.write("</div>\n")



