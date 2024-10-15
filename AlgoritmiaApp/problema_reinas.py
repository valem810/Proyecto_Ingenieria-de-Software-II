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

# Función para convertir imágenes a base64
def img_to_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Función para generar el tablero de ajedrez con las reinas
def mostrar_tableros_reinas(tablero, archivo):
    # Convertir imágenes de reinas a base64
    queen_black_base64 = img_to_base64('media/images/chess-queen-svgrepo-com-black.png')
    queen_white_base64 = img_to_base64('media/images/chess-queen-svgrepo-com-white.png')

    archivo.write("<table style='border-collapse: collapse;'>\n")
    
    # Recorremos las filas del tablero
    for i, fila in enumerate(tablero):
        archivo.write("<tr>\n")
        
        # Recorremos las celdas de cada fila
        for j, celda in enumerate(fila):
            # Determinar el color del cuadro (blanco o negro) alternando según la posición
            is_white_square = (i + j) % 2 == 0  # Alternar color: si la suma del índice es par, es blanco

            if is_white_square:
                # Cuadro blanco: fondo blanco con borde negro
                archivo.write(f"<td style='width:50px;height:50px;background-color:white;border:1px solid black; text-align:center; vertical-align:middle;'>")
                
                # Si hay una reina en esta celda, colocar la reina negra
                if celda == "Q":
                    archivo.write(f"<img src='data:image/png;base64,{queen_black_base64}' width='40' height='40' style='display:block;margin:auto;' />")
            else:
                # Cuadro negro: fondo negro con borde negro
                archivo.write(f"<td style='width:50px;height:50px;background-color:black;border:1px solid black; text-align:center; vertical-align:middle;'>")
                
                # Si hay una reina en esta celda, colocar la reina blanca
                if celda == "Q":
                    archivo.write(f"<img src='data:image/png;base64,{queen_white_base64}' width='40' height='40' style='display:block;margin:auto;' />")
            
            archivo.write("</td>\n")  # Cerrar celda
        
        archivo.write("</tr>\n")  # Cerrar fila
    
    archivo.write("</table>\n")  # Cerrar tabla