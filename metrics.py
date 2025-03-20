import ast
import os
import time
from Prolog_connector import PrologConnector

def aplicar_algoritmo(nombre_algoritmo, sudoku, posibilidades, connector):
    """
    Aplica un algoritmo de resolución del sudoku basado en una secuencia de reglas.
    Devuelve el nuevo sudoku y las nuevas posibilidades, así como un registro de las acciones realizadas.
    """
    # Dividimos el nombre del algoritmo para obtener la secuencia de reglas
    secuencia = nombre_algoritmo.split("-")
    
    # Inicializamos variables para seguimiento
    cambio = True
    sudoku_actual = sudoku.copy()
    posibilidades_actual = posibilidades.copy()
    acciones_realizadas = []
    
    # Índice actual en la secuencia de reglas
    indice = 0
    
    # Bucle principal: seguimos aplicando reglas mientras haya cambios
    while cambio and indice < len(secuencia):
        # Seleccionamos la regla actual
        regla = secuencia[indice]
        
        # Aplicamos la regla correspondiente
        sudoku_nuevo = sudoku_actual.copy()
        posibilidades_nuevo = posibilidades_actual.copy()
        
        # Registramos el tiempo de inicio para esta regla
        tiempo_inicio = time.time()
        
        if regla == "R0" or regla == "0":
            # Regla 0: Llena celdas con una única posibilidad
            sudoku_nuevo = connector.aplicar_regla0(sudoku_actual, posibilidades_actual)
            posibilidades_nuevo = connector.calcular_posibilidades(sudoku_nuevo)
            
            # Calculamos el tiempo de ejecución de esta regla en milisegundos
            tiempo_ejecucion = int((time.time() - tiempo_inicio) * 1000)
            
            # Verificamos si hubo cambios
            if sudoku_nuevo != sudoku_actual:
                # Guardamos la acción realizada
                acciones_realizadas.append({
                    "regla": "regla0",
                    "sudoku_antes": sudoku_actual.copy(),
                    "sudoku_despues": sudoku_nuevo.copy(),
                    "posibilidades_antes": posibilidades_actual.copy(),
                    "posibilidades_despues": posibilidades_nuevo.copy(),
                    "celdas_cambiadas": sum(1 for i in range(len(sudoku_actual)) if sudoku_actual[i] != sudoku_nuevo[i]),
                    "tiempo_ejecucion": tiempo_ejecucion
                })
                
                # Actualizamos el estado actual
                sudoku_actual = sudoku_nuevo.copy()
                posibilidades_actual = posibilidades_nuevo.copy()
                
                # Reiniciamos el índice para volver a la primera regla
                indice = 0
                cambio = True
                continue
            
        elif regla == "R1" or regla == "1":
            # Regla 1: Reduce posibilidades en filas
            posibilidades_nuevo = connector.aplicar_regla1(posibilidades_actual)
            
            # Calculamos el tiempo de ejecución de esta regla en milisegundos
            tiempo_ejecucion = int((time.time() - tiempo_inicio) * 1000)
            
            # Verificamos si hubo cambios
            if posibilidades_nuevo != posibilidades_actual:
                # Guardamos la acción realizada
                acciones_realizadas.append({
                    "regla": "regla1",
                    "sudoku_antes": sudoku_actual.copy(),
                    "sudoku_despues": sudoku_actual.copy(),
                    "posibilidades_antes": posibilidades_actual.copy(),
                    "posibilidades_despues": posibilidades_nuevo.copy(),
                    "tiempo_ejecucion": tiempo_ejecucion
                })
                
                # Actualizamos el estado actual
                posibilidades_actual = posibilidades_nuevo.copy()
                
                # Reiniciamos el índice para volver a la primera regla
                indice = 0
                cambio = True
                continue
            
        elif regla == "R2" or regla == "2":
            # Regla 2: Reduce posibilidades en columnas
            posibilidades_nuevo = connector.aplicar_regla2(posibilidades_actual)
            
            # Calculamos el tiempo de ejecución de esta regla en milisegundos
            tiempo_ejecucion = int((time.time() - tiempo_inicio) * 1000)
            
            # Verificamos si hubo cambios
            if posibilidades_nuevo != posibilidades_actual:
                # Guardamos la acción realizada
                acciones_realizadas.append({
                    "regla": "regla2",
                    "sudoku_antes": sudoku_actual.copy(),
                    "sudoku_despues": sudoku_actual.copy(),
                    "posibilidades_antes": posibilidades_actual.copy(),
                    "posibilidades_despues": posibilidades_nuevo.copy(),
                    "tiempo_ejecucion": tiempo_ejecucion
                })
                
                # Actualizamos el estado actual
                posibilidades_actual = posibilidades_nuevo.copy()
                
                # Reiniciamos el índice para volver a la primera regla
                indice = 0
                cambio = True
                continue
            
        elif regla == "R3" or regla == "3":
            # Regla 3: Reduce posibilidades en bloques 3x3
            posibilidades_nuevo = connector.aplicar_regla3(posibilidades_actual)
            
            # Calculamos el tiempo de ejecución de esta regla en milisegundos
            tiempo_ejecucion = int((time.time() - tiempo_inicio) * 1000)
            
            # Verificamos si hubo cambios
            if posibilidades_nuevo != posibilidades_actual:
                # Guardamos la acción realizada
                acciones_realizadas.append({
                    "regla": "regla3",
                    "sudoku_antes": sudoku_actual.copy(),
                    "sudoku_despues": sudoku_actual.copy(),
                    "posibilidades_antes": posibilidades_actual.copy(),
                    "posibilidades_despues": posibilidades_nuevo.copy(),
                    "tiempo_ejecucion": tiempo_ejecucion
                })
                
                # Actualizamos el estado actual
                posibilidades_actual = posibilidades_nuevo.copy()
                
                # Reiniciamos el índice para volver a la primera regla
                indice = 0
                cambio = True
                continue
        
        # Si llegamos aquí, la regla actual no produjo cambios
        indice += 1
        if indice >= len(secuencia):
            # Si hemos probado todas las reglas y no hubo cambios, terminamos
            cambio = False
    
    # Devolvemos el sudoku final, las posibilidades finales y la lista de acciones realizadas
    return sudoku_actual, posibilidades_actual, acciones_realizadas

def aplicar_reglas(sudoku, posibilidades, connector, algoritmo="default"):
    celdas_rellenadas = 0
    # Algoritmos disponibles
    algoritmos_disponibles = {
        "R0-1-2-3": "R0-1-2-3",
        "R0-2-3-1": "R0-2-3-1",
        "R1-2-3-0": "R1-2-3-0",
        "R2-3-1-0": "R2-3-1-0",
        "R0": "R0",
        "R1-0": "R1-0",
        "R2-0": "R2-0",
        "R3-0": "R3-0"
    }

    # Verificamos si el algoritmo existe
    if algoritmo not in algoritmos_disponibles:
        print(f"Algoritmo '{algoritmo}' no reconocido. Usando algoritmo predeterminado.")
        algoritmo = "default"
    
    # Obtenemos la secuencia de reglas del algoritmo
    secuencia_algoritmo = algoritmos_disponibles[algoritmo]
    
    # Aplicamos el algoritmo
    nuevo_sudoku, nuevas_posibilidades, acciones = aplicar_algoritmo(
        secuencia_algoritmo, sudoku, posibilidades, connector)
    
    # Registramos las acciones en el historial
    for accion in acciones:        
        # Si es la regla0, añadimos información de celdas cambiadas
        if accion["regla"] == "regla0" and "celdas_cambiadas" in accion:
            celdas_rellenadas += accion["celdas_cambiadas"]

    def hace_cambios(accion):
        return accion.sudoku_antes != accion.sudoku_despues or \
        accion.posibilidades_antes != accion.posibilidades_despues
    
    filter(hace_cambios, acciones)

    return nuevo_sudoku, len(acciones)


def main():
    prolog = PrologConnector()
    salida = ""
    
    algoritmos = [
        "R0-1-2-3",
        "R0-2-3-1",
        "R1-2-3-0",
        "R2-3-1-0",
        "R0",
        "R1-0",
        "R2-0",
        "R3-0"
    ]
    
    folder_path = "./sudokus/"
    sudokus_0 = []
    sudokus_1 = []
    sudokus_2 = []
    sudokus_3 = []
    sudokus_4 = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                sudoku_text = file.read()
                sudoku_list = ast.literal_eval(sudoku_text)
                if filename.startswith("sudoku_0"): sudokus_0.append(sudoku_list)
                elif filename.startswith("sudoku_1"): sudokus_1.append(sudoku_list)
                elif filename.startswith("sudoku_2"): sudokus_2.append(sudoku_list)
                elif filename.startswith("sudoku_3"): sudokus_3.append(sudoku_list)
                elif filename.startswith("sudoku_4"): sudokus_4.append(sudoku_list)

    salida += "\n Sudokus Fáciles (0):\n"
    salida += "=========================================================================\n"
    salida += " Algoritmo   | Sudokus resueltos | Celdas rellenadas | Reglas aplicadas\n"
    salida += "-------------+-------------------+--------------------+------------------\n"

    resueltos_acum = [0 for _ in range(len(algoritmos))]
    resueltos_total = [0 for _ in range(len(algoritmos))]
    rellenadas_acum = [0 for _ in range(len(algoritmos))]
    rellenadas_total = [0 for _ in range(len(algoritmos))]
    acciones_total = [0 for _ in range(len(algoritmos))]

    for algo in algoritmos:
        idx = algoritmos.index(algo)

        resueltos, celdas, rellenables, total_acciones = 0, 0, 0, 0
        salida += f" {algo} {' ' * (12 - len(algo))}| "
        for sudoku in sudokus_0:
            pos = prolog.calcular_posibilidades(sudoku)
            new_sudoku, num_acciones = aplicar_reglas(sudoku, pos, prolog, algo)
            resueltos += not ('.' in new_sudoku)
            celdas += sudoku.count('.') - new_sudoku.count('.')
            rellenables += sudoku.count('.')
            total_acciones += num_acciones
        
        salida += f" {resueltos} / {len(sudokus_0)}          | \
{' ' * (1 - celdas // 100)}{celdas} / {rellenables}          | {total_acciones}\n"

        resueltos_acum[idx] += resueltos
        resueltos_total[idx] += len(sudokus_0)
        rellenadas_acum[idx] += celdas
        rellenadas_total[idx] += rellenables
        acciones_total[idx] += total_acciones

    salida += "\n Sudokus Medios (1):\n"
    salida += "=========================================================================\n"
    salida += " Algoritmo   | Sudokus resueltos | Celdas rellenadas | Reglas aplicadas\n"
    salida += "-------------+-------------------+--------------------+------------------\n"

    for algo in algoritmos:
        idx = algoritmos.index(algo)

        resueltos, celdas, rellenables, total_acciones = 0, 0, 0, 0
        salida += f" {algo} {' ' * (12 - len(algo))}| "

        for sudoku in sudokus_1:
            pos = prolog.calcular_posibilidades(sudoku)
            new_sudoku, num_acciones = aplicar_reglas(sudoku, pos, prolog, algo)
            resueltos += not ('.' in new_sudoku)
            celdas += sudoku.count('.') - new_sudoku.count('.')
            rellenables += sudoku.count('.')
            total_acciones += num_acciones
        
        salida += f" {resueltos} / {len(sudokus_1)}          | \
{' ' * (1 - celdas // 100)}{celdas} / {rellenables}          | {total_acciones}\n"

        resueltos_acum[idx] += resueltos
        resueltos_total[idx] += len(sudokus_1)
        rellenadas_acum[idx] += celdas
        rellenadas_total[idx] += rellenables
        acciones_total[idx] += total_acciones


    salida += "\n Sudokus Dificiles (2):\n"
    salida += "=========================================================================\n"
    salida += " Algoritmo   | Sudokus resueltos | Celdas rellenadas | Reglas aplicadas\n"
    salida += "-------------+-------------------+--------------------+------------------\n"
    for algo in algoritmos:
        idx = algoritmos.index(algo)

        resueltos, celdas, rellenables = 0, 0, 0
        salida += f" {algo} {' ' * (12 - len(algo))}| "

        for sudoku in sudokus_2:
            pos = prolog.calcular_posibilidades(sudoku)
            new_sudoku, num_acciones = aplicar_reglas(sudoku, pos, prolog, algo)
            resueltos += not ('.' in new_sudoku)
            celdas += sudoku.count('.') - new_sudoku.count('.')
            rellenables += sudoku.count('.')
            total_acciones += num_acciones
        
        salida += f" {resueltos} / {len(sudokus_2) + len(sudokus_3)}          | \
{' ' * (1 - celdas // 100)}{celdas} / {rellenables}          | {total_acciones}\n"

        resueltos_acum[idx] += resueltos
        resueltos_total[idx] += len(sudokus_2) + len(sudokus_3)
        rellenadas_acum[idx] += celdas
        rellenadas_total[idx] += rellenables
        acciones_total[idx] += total_acciones
    
    salida += "\n Estadísticas totales:\n"
    salida += "=========================================================================\n"
    salida += " Algoritmo   | Sudokus resueltos | Celdas rellenadas | Reglas aplicadas\n"
    salida += "-------------+-------------------+--------------------+------------------\n"

    for algo in algoritmos:
        idx = algoritmos.index(algo)

        resueltos, celdas, rellenables, total_acciones = 0, 0, 0, 0
        salida += f" {algo} {' ' * (12 - len(algo))}| "

        for sudoku in sudokus_4:
            pos = prolog.calcular_posibilidades(sudoku)
            new_sudoku, num_acciones = aplicar_reglas(sudoku, pos, prolog, algo)
            resueltos += not ('.' in new_sudoku)
            celdas += sudoku.count('.') - new_sudoku.count('.')
            rellenables += sudoku.count('.')
            total_acciones += num_acciones

        resueltos_acum[idx] += resueltos
        resueltos_total[idx] += len(sudokus_4)
        rellenadas_acum[idx] += celdas
        rellenadas_total[idx] += rellenables
        acciones_total[idx] += total_acciones
        
        salida += f"{' ' * (1 - resueltos_acum[idx] // 10)} {resueltos_acum[idx]} / {resueltos_total[idx]}\
          | {rellenadas_acum[idx]} / {rellenadas_total[idx]}         | {acciones_total[idx]}\n"


    print(salida)


if __name__ == '__main__':
    main()