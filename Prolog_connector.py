from pyswip import Prolog

# -------------------------------
# Función para convertir lista de sudoku a formato Prolog
# Ejemplo: [5, '.', 4, ...]  -->  "[5, '.', 4, ...]"
def sudoku_to_prolog(sudoku):
    elems = []
    for celda in sudoku:
        if celda == '.':
            elems.append("'.'")
        else:
            elems.append(str(celda))
    return "[" + ", ".join(elems) + "]"

# -------------------------------
# Clase que encapsula las llamadas a Prolog
class PrologConnector:
    def __init__(self):
        self.prolog = Prolog()
        for archivo in ["sudokus.pl", "regla0.pl", "regla1.pl", "regla2.pl", "regla3.pl", "main.pl"]:
            self.prolog.consult(archivo)
    
    def calcular_posibilidades(self, sudoku):
        query = f"posibles({sudoku_to_prolog(sudoku)}, Posibles)."
        resultados = list(self.prolog.query(query))
        return resultados[0]['Posibles'] if resultados else None

    def aplicar_regla0(self, sudoku, posibilidades):
        query = f"regla0({sudoku_to_prolog(sudoku)}, {sudoku_to_prolog(posibilidades)}, NuevoS)."
        resultados = list(self.prolog.query(query))
        return resultados[0]['NuevoS'] if resultados else sudoku

    def aplicar_regla1(self, posibilidades):
        query = f"regla1({sudoku_to_prolog(posibilidades)}, NuevoP)."
        resultados = list(self.prolog.query(query))
        return resultados[0]['NuevoP'] if resultados else posibilidades

    def aplicar_regla2(self, posibilidades):
        query = f"regla2({sudoku_to_prolog(posibilidades)}, NuevoP)."
        resultados = list(self.prolog.query(query))
        return resultados[0]['NuevoP'] if resultados else posibilidades

    def aplicar_regla3(self, posibilidades):
        query = f"regla3({sudoku_to_prolog(posibilidades)}, NuevoP)."
        resultados = list(self.prolog.query(query))
        return resultados[0]['NuevoP'] if resultados else posibilidades

    def validar_movimiento(self, sudoku, index, valor):
        posibilidades = self.calcular_posibilidades(sudoku)
        # La variable 'posibilidades' es una lista de 81 elementos. Para la celda ya llena se devuelve '.'
        celda_posibles = posibilidades[index]
        # Si la celda no está vacía, no se permite el cambio
        if sudoku[index] != '.':
            return False, f"La celda ya contiene {sudoku[index]}"
        try:
            valor_int = int(valor)
        except:
            return False, "Debe ingresar un número entre 1 y 9"
        if valor_int in celda_posibles:
            return True, "Movimiento válido"
        else:
            return False, f"El número {valor_int} no es una posibilidad en esa celda.\nOpciones: {celda_posibles}"
