import copy
import base64

class ProblemaReinas:
    def __init__(self, n):
        self.n = n
        self.tablero = [["x"] * n for _ in range(n)]
        self.soluciones = []

    def resolver(self):
        self.solve(0)
        return len(self.soluciones), self.soluciones

    def solve(self, col):
        if col >= self.n:
            self.soluciones.append(copy.deepcopy(self.tablero))
            return

        for i in range(self.n):
            if self.is_safe(i, col):
                self.tablero[i][col] = "Q"
                self.solve(col + 1)
                self.tablero[i][col] = "x"

    def is_safe(self, row, col):
        # Verificar la fila a la izquierda
        for j in range(col):
            if self.tablero[row][j] == "Q":
                return False

        # Verificar la diagonal superior izquierda
        i, j = row, col
        while i >= 0 and j >= 0:
            if self.tablero[i][j] == "Q":
                return False
            i -= 1
            j -= 1

        # Verificar la diagonal inferior izquierda
        i, j = row, col
        while i < self.n and j >= 0:
            if self.tablero[i][j] == "Q":
                return False
            i += 1
            j -= 1

        return True

def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def mostrar_tableros_reinas(tablero, archivo):
    queen_image_base64 = img_to_base64('media/images/chess-queen-svgrepo-com.png')
    archivo.write("<table style='border-collapse: collapse;'>\n")
    for fila in tablero:
        archivo.write("<tr>\n")
        for celda in fila:
            if celda == "Q":
                archivo.write(f"<td style='width:50px;height:50px;border:1px solid black; text-align:center; vertical-align:middle;'>"
                              f"<img src='data:image/png;base64,{queen_image_base64}' width='40' height='40' style='display:block;margin:auto;' /></td>\n")
            else:
                archivo.write("<td style='width:50px;height:50px;border:1px solid black;'></td>\n")
        archivo.write("</tr>\n")
    archivo.write("</table>\n")