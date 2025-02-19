"""from pyswip import Prolog

prolog = Prolog()

prolog.consult("main.pl")
sudoku = "[
    5 ,'.' , 4 ,  6 , 7 , 8 ,   9 , 1 , 2,
    6 , 7 , 2 ,  '.', 9 , 5 ,   3 , 4 , 8,
   '.', 9 , 8 ,   3 , 4 , 2 ,   5 , 6 , 7,

    8 , 5 , 9 ,   7 , 6 , 1 ,   4 ,'.', 3,
    4 , 2 , 6 ,   8 , 5 , 3 ,  '.', 9 , 1,
    7 , 1 ,'.',   9 , 2 , 4 ,   8 , 5 , 6,

    9 , 6 , 1 ,   5 ,'.', 7 ,   2 , 8 , 4,
    2 , 8 , 7 ,   4 , 1 , 9 ,   6 , 3 ,'.',
    3 , 4 , 5 ,   2 , 8 ,'.',   1 , 7 , 9
]"

query = f"posibles({sudoku}, Posibles)."
res = prolog.query(query)
print(list(res))
"""

from pyswip import Prolog

# Inicializar el motor de Prolog
prolog = Prolog()

# Cargar el archivo Prolog (asegúrate de que el path sea correcto)
prolog.consult("main.pl")  # Cambia "sudoku.pl" por el nombre real de tu archivo

# Definir un Sudoku de 81 casillas (aquí, todas vacías representadas por el átomo '.')
# Para que Prolog interprete correctamente el átomo, lo representamos como "'.'"
sudoku = ["'.'" for _ in range(81)]

# Función para convertir una lista de Python en una lista con sintaxis Prolog
def list_to_prolog(lst):
    # Une los elementos con comas y los encierra entre corchetes
    return "[" + ",".join(lst) + "]"

# Convertir la lista de Sudoku a una cadena con formato Prolog
sudoku_prolog = list_to_prolog(sudoku)
sudoku_prolog = """[
    5 ,'.' , 4 ,  6 , 7 , 8 ,   9 , 1 , 2,
    6 , 7 , 2 ,  '.', 9 , 5 ,   3 , 4 , 8,
   '.', 9 , 8 ,   3 , 4 , 2 ,   5 , 6 , 7,

    8 , 5 , 9 ,   7 , 6 , 1 ,   4 ,'.', 3,
    4 , 2 , 6 ,   8 , 5 , 3 ,  '.', 9 , 1,
    7 , 1 ,'.',   9 , 2 , 4 ,   8 , 5 , 6,

    9 , 6 , 1 ,   5 ,'.', 7 ,   2 , 8 , 4,
    2 , 8 , 7 ,   4 , 1 , 9 ,   6 , 3 ,'.',
    3 , 4 , 5 ,   2 , 8 ,'.',   1 , 7 , 9
]"""
print(sudoku_prolog)


# Construir la consulta: queremos ejecutar posibles(S, Posibles) con nuestro Sudoku S
consulta = "posibles("+sudoku_prolog+", Posibles)."
# Ejecutar la consulta y obtener las soluciones
resultados = list(prolog.query(consulta, catcherrors=True))

# Mostrar el resultado
for sol in resultados:
    print("Posibles para cada casilla:")
    print(sol["Posibles"])
