import streamlit as st
import ast
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
        
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
    # Algoritmos disponibles
    algoritmos_disponibles = {
        "R0-1-2-3": "R0-1-2-3",
        "R0-2-3-1": "R0-2-3-1",
        "R1-2-3-0": "R1-2-3-0",
        "R2-3-1-0": "R2-3-1-0",
        "R0": "R0",
        "R0-1": "R0-1",
        "R0-2": "R0-2",
        "R0-3": "R0-3",
    }

    # Verificamos si el algoritmo existe
    if algoritmo not in algoritmos_disponibles:
        st.warning(f"Algoritmo '{algoritmo}' no reconocido. Usando algoritmo predeterminado.")
        algoritmo = "default"
    
    # Obtenemos la secuencia de reglas del algoritmo
    secuencia_algoritmo = algoritmos_disponibles[algoritmo]
    
    # Aplicamos el algoritmo
    nuevo_sudoku, nuevas_posibilidades, acciones = aplicar_algoritmo(
        secuencia_algoritmo, sudoku, posibilidades, connector)
    
    # Registramos las acciones en el historial
    for accion in acciones:
        # Creamos un registro para el historial
        registro = {
            "sudoku": accion["sudoku_despues"],
            "posibilidades": accion["posibilidades_despues"],
            "accion": f"{accion['regla']} ({algoritmo})",
            "tiempo_ejecucion": accion.get("tiempo_ejecucion", "N/A")
        }

        
        # Si es la regla0, añadimos información de celdas cambiadas
        if accion["regla"] == "regla0" and "celdas_cambiadas" in accion:
            registro["celdas_llenas"] = accion["celdas_cambiadas"]
        
        # Añadimos al historial
        historico = st.session_state.historico
        indice_actual = st.session_state.historico_indice
        
        # Si estamos en medio del historial, eliminamos los estados futuros
        if indice_actual < len(historico) - 1:
            st.session_state.historico = historico[:indice_actual + 1]
        
        # Añadimos el nuevo estado al historial
        
        st.session_state.historico.append(registro)
        # Actualizamos el índice actual
        st.session_state.historico_indice = len(st.session_state.historico) - 1
    
    return nuevo_sudoku, nuevas_posibilidades

# -------------------------------
# Función para parsear el archivo sudoku (formato: lista de 81 elementos)
def parse_sudoku_file(file_content):
    try:
        # Se espera que el contenido sea algo como:
        # [
        #     5 ,'.' , 4 ,  6 , 7 , 8 ,   9 , 1 , 2,
        #     6 , 7 , 2 ,  '.', 9 , 5 ,   3 , 4 , 8,
        #     ... (81 elementos)
        # ]
        sudoku = ast.literal_eval(file_content.decode("utf-8"))
        if isinstance(sudoku, list) and len(sudoku) == 81:
            return sudoku
        else:
            st.error("El sudoku debe ser una lista de 81 elementos.")
            return None
    except Exception as e:
        st.error(f"Error al parsear el archivo: {e}")
        return None

# -------------------------------
# Función para contar celdas llenas en un sudoku
def contar_celdas_llenas(sudoku):
    return sum(1 for celda in sudoku if celda != '.')

# -------------------------------
# Función para guardar el estado actual en el historial
def guardar_estado_en_historial(accion, celdas_llenas=None):
    actual_sudoku = st.session_state.sudoku.copy()
    actual_posibilidades = st.session_state.posibilidades
    
    # Si es una interacción de usuario o regla0, calculamos las celdas llenas
    if accion == "input_usuario" or accion == "regla0":
        if celdas_llenas is None:
            celdas_llenas = contar_celdas_llenas(actual_sudoku)
    
    # Creamos el registro del historial
    registro = {
        "sudoku": actual_sudoku,
        "posibilidades": actual_posibilidades,
        "accion": accion,
        "celdas_llenas": celdas_llenas
    }
    
    # Obtenemos el índice actual y el historial
    indice_actual = st.session_state.historico_indice
    historico = st.session_state.historico
    
    # Si estamos en medio del historial, eliminamos los estados futuros
    if indice_actual < len(historico) - 1:
        st.session_state.historico = historico[:indice_actual + 1]
    
    # Añadimos el nuevo estado al historial
    st.session_state.historico.append(registro)
    # Actualizamos el índice actual
    st.session_state.historico_indice = len(st.session_state.historico) - 1

# -------------------------------
# Callbacks para manejar cambios sin reruns
def on_cell_change(idx):
    # Esta función se llama cuando cambia el valor de una celda
    valor_ingresado = st.session_state[f"cell_{idx}"]
    
    if valor_ingresado == "":
        return
    
    sudoku = st.session_state.sudoku
    connector = st.session_state.connector
    
    try:
        valor_int = int(valor_ingresado)
        if valor_int < 1 or valor_int > 9:
            st.session_state.mensaje = {"tipo": "error", "texto": f"Celda {idx+1}: Debe ingresar un número entre 1 y 9"}
            return
    except ValueError:
        st.session_state.mensaje = {"tipo": "error", "texto": f"Celda {idx+1}: Debe ingresar un número entre 1 y 9"}
        return
    
    # Validamos el movimiento
    valido, mensaje = connector.validar_movimiento(sudoku, idx, valor_ingresado)
    
    if valido:
        # Actualizamos el sudoku
        sudoku[idx] = int(valor_ingresado)
        st.session_state.sudoku = sudoku
        # Recalculamos posibilidades
        posibilidades = connector.calcular_posibilidades(sudoku)
        st.session_state.posibilidades = posibilidades
        
        # Guardamos el estado en el historial
        celdas_actuales = contar_celdas_llenas(sudoku)
        guardar_estado_en_historial("input_usuario", celdas_actuales)
        
        # Guardamos el mensaje de éxito
        st.session_state.mensaje = {"tipo": "exito", "texto": f"Celda {idx+1}: {mensaje}"}
        # Marcamos que la UI necesita actualizarse
        st.session_state.need_refresh = True
        # Generamos una nueva clave única para forzar la recarga de widgets
        st.session_state.board_key = int(time.time() * 1000)
    else:
        # Si no es válido, guardamos el mensaje de error
        st.session_state.mensaje = {"tipo": "error", "texto": f"Celda {idx+1}: {mensaje}"}
        # Limpiamos el valor inválido
        st.session_state[f"cell_{idx}"] = ""

# Callbacks para los botones de reglas
def on_regla(regla):
    # Esta función se llama cuando se pulsa un botón de regla
    sudoku = st.session_state.sudoku
    posibilidades = st.session_state.posibilidades
    connector = st.session_state.connector
    
    celdas_antes = contar_celdas_llenas(sudoku)
    
    # Medimos el tiempo de ejecución
    import time
    tiempo_inicio = time.time()
    
    if regla == "resolver":
        # Obtenemos el algoritmo seleccionado del dropdown
        algoritmo = st.session_state.algoritmo_seleccionado
        # Registramos qué algoritmo se está usando en el historial
        accion = f"resolver ({algoritmo})"
        nuevo_sudoku, nuevas_poss = aplicar_reglas(sudoku, posibilidades, connector, algoritmo)
    elif regla == "regla0":
        accion = regla
        nuevo_sudoku = connector.aplicar_regla0(sudoku, posibilidades)
        nuevas_poss = connector.calcular_posibilidades(nuevo_sudoku) if sudoku != nuevo_sudoku else posibilidades
    elif regla == "regla1":
        accion = regla
        nuevo_sudoku = sudoku
        nuevas_poss = connector.aplicar_regla1(posibilidades)
    elif regla == "regla2":
        accion = regla
        nuevo_sudoku = sudoku
        nuevas_poss = connector.aplicar_regla2(posibilidades)
    elif regla == "regla3":
        accion = regla
        nuevo_sudoku = sudoku
        nuevas_poss = connector.aplicar_regla3(posibilidades)
    else:
        accion = regla
        nuevo_sudoku = connector.aplicar_regla(regla, sudoku, posibilidades)
        nuevas_poss = connector.calcular_posibilidades(nuevo_sudoku)
    
    # Calculamos el tiempo de ejecución en milisegundos
    tiempo_fin = time.time()
    tiempo_ejecucion = round((tiempo_fin - tiempo_inicio) * 1000, 0)  # en milisegundos
    st.session_state.tiempo_ejecucion = tiempo_ejecucion
    
    st.session_state.sudoku = nuevo_sudoku
    st.session_state.posibilidades = nuevas_poss
    
    # Guardamos el estado en el historial
    if regla == "regla0":
        celdas_despues = contar_celdas_llenas(nuevo_sudoku)
        celdas_llenadas = celdas_despues - celdas_antes
        guardar_estado_en_historial(accion, celdas_llenadas)
    elif "regla" in regla: 
        guardar_estado_en_historial(accion)
    
    st.session_state.mensaje = {"tipo": "info", "texto": f"Se ha aplicado {accion} al sudoku (tiempo: {tiempo_ejecucion} ms)"}
    st.session_state.need_refresh = True
    st.session_state.board_key = int(time.time() * 1000)

# Callbacks para los botones de navegación del histórico
def on_anterior():
    if st.session_state.historico_indice > 0:
        st.session_state.historico_indice -= 1
        cargar_estado_desde_historico()

def on_siguiente():
    if st.session_state.historico_indice < len(st.session_state.historico) - 1:
        st.session_state.historico_indice += 1
        cargar_estado_desde_historico()


def cargar_estado_desde_historico():
    indice = st.session_state.historico_indice
    registro = st.session_state.historico[indice]
    
    st.session_state.sudoku = registro["sudoku"]
    st.session_state.posibilidades = registro["posibilidades"]
    st.session_state.mensaje = {"tipo": "info", 
                               "texto": f"Cargado estado histórico #{indice+1} - Acción: {registro['accion']}"}
    st.session_state.need_refresh = True
    st.session_state.board_key = int(time.time() * 1000)

# -------------------------------
def format_posibilidades(posibles):
    if posibles == '.':
        return ""
    return "[" + ",".join(map(str, posibles)) + "]"

# -------------------------------
def render_sudoku():
    st.markdown(
        """
        <style>
        /* Centrar el texto en todos los inputs */
        input {
            text-align: center;
        }
        /* Para inputs deshabilitados (celdas ya validadas) */
        input:disabled {
            font-weight: bold;
            color: white;
            background-color: #333;
            text-align: center;
        }
        /* Nuevos estilos para ajustar espaciado */
        .main .block-container {
            padding-right: 2rem !important;
        }
        
        /* Aumentar espacio entre columnas del sudoku */
        [data-testid="column"] {
            margin: 0px 5px !important;
        }
        
        /* Reducir padding en inputs */
        .stTextInput input {
            padding: 4px 8px !important;
        }
        
        /* Ajustar ancho de columnas del sudoku */
        div[data-testid="column"]:nth-of-type(1),
        div[data-testid="column"]:nth-of-type(5),
        div[data-testid="column"]:nth-of-type(9) {
            width: calc(11.11% - 5px) !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("### Sudoku")
    
    # Recuperamos los datos del estado
    sudoku = st.session_state.sudoku
    posibilidades = st.session_state.posibilidades
    
    # Muestra mensaje si existe
    if 'mensaje' in st.session_state and st.session_state.mensaje:
        if st.session_state.mensaje["tipo"] == "exito":
            st.success(st.session_state.mensaje["texto"])
        elif st.session_state.mensaje["tipo"] == "error":
            st.warning(st.session_state.mensaje["texto"])
        elif st.session_state.mensaje["tipo"] == "info":
            st.info(st.session_state.mensaje["texto"])
        
        # Limpiamos el mensaje después de mostrarlo
        st.session_state.mensaje = None
    
    # Función para mapear la columna j a la columna real en st.columns
    def map_col(j):
        if j < 3:
            return j
        elif j < 6:
            return j + 1  # Salta una columna fina
        else:
            return j + 2  # Salta dos columnas finas
    
    # Se recorre la grilla de 9x9 celdas
    for i in range(9):
        if i in [3, 6]:
            st.write("")  # Separador entre bloques
        cols = st.columns([1,1,1, 0.2, 1,1,1, 0.2, 1,1,1], gap="small")
        for j in range(9):
            idx = i * 9 + j
            col_index = map_col(j)
            esta_vacia = (sudoku[idx] == '.')
            
            with cols[col_index]:
                if esta_vacia:
                    # Construimos el placeholder con las posibilidades actuales
                    placeholder = format_posibilidades(posibilidades[idx])
                    
                    # Para las celdas vacías, mostramos un input con las posibilidades como placeholder
                    st.text_input(
                        label=f"Input for cell {idx+1}",
                        value="",
                        key=f"cell_{idx}",
                        placeholder=placeholder,
                        on_change=on_cell_change,
                        args=(idx,),
                        label_visibility="collapsed"
                    )
                else:
                    # Para celdas ya completadas, mostramos un input deshabilitado
                    st.text_input(
                        label=f"Input for cell {idx+1}",
                        value=str(sudoku[idx]),
                        key=f"cell_{idx}",
                        disabled=True,
                        label_visibility="collapsed"
                    )

def plot_historial_data():
    if len(st.session_state.historico) > 0:

        # Extraemos los datos para el gráfico
        datos = []
        for i, registro in enumerate(st.session_state.historico):
            accion = registro["accion"]
            
            # Calculamos el número de posibilidades con un solo valor
            posibilidades_un_valor = 0
            if "posibilidades" in registro:
                for pos in registro["posibilidades"]:
                    if pos != '.' and isinstance(pos, list) and len(pos) == 1:
                        posibilidades_un_valor += 1
            
            # Calculamos casillas resueltas
            if i == 0:
                casillas_resueltas = contar_celdas_llenas(registro["sudoku"])
            else:
                prev_sudoku = st.session_state.historico[i-1]["sudoku"]
                casillas_resueltas = contar_celdas_llenas(registro["sudoku"]) - contar_celdas_llenas(prev_sudoku)
            
            # Añadimos el tiempo de ejecución (si existe)
            tiempo_ejecucion = registro.get("tiempo_ejecucion", 0)
            if tiempo_ejecucion == "N/A":
                tiempo_ejecucion = 0

            datos.append({
                "Paso": i + 1,
                "Acción": accion,
                "Posibilidades 1 valor": posibilidades_un_valor,
                "Casillas resueltas": casillas_resueltas,
                "Tiempo (ms)": tiempo_ejecucion
            })
        
        # Creamos un DataFrame
        df = pd.DataFrame(datos)
        
        # Añadimos columnas acumuladas para los valores que lo requieren
        df["Posibilidades 1 valor (acumulado)"] = df["Posibilidades 1 valor"].cumsum()
        df["Tiempo (ms) (acumulado)"] = df["Tiempo (ms)"].cumsum()
        
        # Extraemos la regla básica (R0, R1, R2, R3, etc.)
        df["Regla base"] = df["Acción"].apply(lambda x: x.split()[0] if len(x.split()) > 0 else x)
        
        # Creamos un DataFrame resumido por regla
        df_por_regla = df.groupby("Regla base").agg({
            "Posibilidades 1 valor": "sum",
            "Tiempo (ms)": "sum"
        }).reset_index()
        
        # Calculamos la eficiencia (posibilidades/ms) por regla
        df_por_regla["Eficiencia (pos/ms)"] = df_por_regla["Posibilidades 1 valor"] / df_por_regla["Tiempo (ms)"]
        # Reemplazamos NaN o inf por 0
        df_por_regla["Eficiencia (pos/ms)"] = df_por_regla["Eficiencia (pos/ms)"].fillna(0).replace([np.inf, -np.inf], 0)
        
        # Ofrecemos la visualización
        st.markdown("### Visualización de datos")
        
        # Opciones de visualización
        opcion_grafico = st.selectbox(
            "Selecciona un tipo de gráfico:",
            ["Posibilidades", "Tiempo de ejecución", "Posibilidades por regla", "Eficiencia por regla"]
        )
        
        # Configuración común para los gráficos
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Generamos el gráfico seleccionado
        if opcion_grafico == "Posibilidades":
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Gráfico para posibilidades con 1 valor (acumulado)
            ax.plot(df["Paso"], df["Posibilidades 1 valor (acumulado)"], 
                    marker='o', linestyle='-', linewidth=2, markersize=8, 
                    color='#1f77b4', label='Posibilidades con 1 valor (acumulado)')
            
            # Gráfico para posibilidades con 1 valor (por paso)
            ax2 = ax.twinx()
            ax2.plot(df["Paso"], df["Posibilidades 1 valor"], 
                    marker='o', linestyle='--', linewidth=1, markersize=5, 
                    color='#17becf', label='Posibilidades con 1 valor (por paso)')
            
            # Configuramos los ejes
            ax.set_xlabel("Paso", fontsize=12)
            ax.set_ylabel("Posibilidades acumuladas", fontsize=12)
            ax2.set_ylabel("Posibilidades por paso", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Configuramos los límites de los ejes
            ax.set_xlim(0.5, len(df) + 0.5)
            ax.set_xticks(np.arange(1, len(df) + 1))
            
            # Combinamos las leyendas de ambos ejes
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
            
            # Título del gráfico
            plt.title("Evolución de posibilidades con un solo valor", fontsize=14)
            
        elif opcion_grafico == "Tiempo de ejecución":
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Gráfico para tiempo de ejecución (acumulado)
            ax.plot(df["Paso"], df["Tiempo (ms) (acumulado)"], 
                    marker='o', linestyle='-', linewidth=2, markersize=8, 
                    color='#1f77b4', label='Tiempo de ejecución (acumulado)')
            
            # Gráfico para tiempo de ejecución (por paso)
            ax2 = ax.twinx()
            ax2.plot(df["Paso"], df["Tiempo (ms)"], 
                    marker='o', linestyle='--', linewidth=1, markersize=5, 
                    color='#17becf', label='Tiempo de ejecución (por paso)')
            
            # Añadimos etiquetas con los valores en cada punto para el tiempo por paso
            for i, txt in enumerate(df["Tiempo (ms)"]):
                if txt > 0:  # Solo mostramos etiquetas para valores positivos
                    ax2.annotate(f"{txt} ms", 
                                (df["Paso"][i], df["Tiempo (ms)"][i]),
                                textcoords="offset points", 
                                xytext=(0,10), 
                                ha='center',
                                fontsize=9)
            
            # Configuramos los ejes
            ax.set_xlabel("Paso", fontsize=12)
            ax.set_ylabel("Tiempo acumulado (ms)", fontsize=12)
            ax2.set_ylabel("Tiempo por paso (ms)", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Configuramos los límites de los ejes
            ax.set_xlim(0.5, len(df) + 0.5)
            ax.set_xticks(np.arange(1, len(df) + 1))
            
            # Combinamos las leyendas de ambos ejes
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
            
            # Título del gráfico
            plt.title("Evolución del tiempo de ejecución", fontsize=14)
            
        elif opcion_grafico == "Posibilidades por regla":
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Ordenamos las reglas para que se muestren en orden lógico
            orden_reglas = ['regla0', 'regla1', 'regla2', 'regla3', 'resolver', 'input_usuario']
            df_por_regla_ordenado = df_por_regla.copy()
            
            # Asignamos un índice numérico para ordenar
            def get_order(regla):
                try:
                    return orden_reglas.index(regla)
                except ValueError:
                    return len(orden_reglas)
            
            df_por_regla_ordenado['orden'] = df_por_regla_ordenado['Regla base'].apply(get_order)
            df_por_regla_ordenado = df_por_regla_ordenado.sort_values('orden')
            
            # Creamos el histograma
            bars = ax.bar(df_por_regla_ordenado["Regla base"], 
                         df_por_regla_ordenado["Posibilidades 1 valor"],
                         color='#1f77b4', alpha=0.8)
            
            # Añadimos etiquetas con los valores en cada barra
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{int(height)}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)
            
            # Configuramos los ejes
            ax.set_xlabel("Regla", fontsize=12)
            ax.set_ylabel("Posibilidades con 1 valor (total)", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7, axis='y')
            
            # Título del gráfico
            plt.title("Posibilidades con 1 valor generadas por cada regla", fontsize=14)
            
        else:  # Eficiencia por regla
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Ordenamos las reglas para que se muestren en orden lógico
            orden_reglas = ['regla0', 'regla1', 'regla2', 'regla3', 'resolver', 'input_usuario']
            df_por_regla_ordenado = df_por_regla.copy()
            
            # Asignamos un índice numérico para ordenar
            def get_order(regla):
                try:
                    return orden_reglas.index(regla)
                except ValueError:
                    return len(orden_reglas)
            
            df_por_regla_ordenado['orden'] = df_por_regla_ordenado['Regla base'].apply(get_order)
            df_por_regla_ordenado = df_por_regla_ordenado.sort_values('orden')
            
            # Creamos el histograma
            bars = ax.bar(df_por_regla_ordenado["Regla base"], 
                         df_por_regla_ordenado["Eficiencia (pos/ms)"],
                         color='#2ca02c', alpha=0.8)
            
            # Añadimos etiquetas con los valores en cada barra
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 puntos de desplazamiento vertical
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9)
            
            # Configuramos los ejes
            ax.set_xlabel("Regla", fontsize=12)
            ax.set_ylabel("Eficiencia (posibilidades/ms)", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7, axis='y')
            
            # Título del gráfico
            plt.title("Eficiencia de cada regla (posibilidades por ms)", fontsize=14)
        
        # Ajustamos el layout para que no se corten los elementos
        plt.tight_layout()
        
        # Mostramos el gráfico
        st.pyplot(fig)
        
        # Ofrecemos el DataFrame para análisis adicional
        st.subheader("Datos por paso")
        st.dataframe(df)
        
        st.subheader("Resumen por regla")
        st.dataframe(df_por_regla)

def guardar_estado_en_historial(accion, celdas_llenas=None):
    actual_sudoku = st.session_state.sudoku.copy()
    actual_posibilidades = st.session_state.posibilidades
    
    # Si es una interacción de usuario o regla0, calculamos las celdas llenas
    if accion == "input_usuario" or accion == "regla0":
        if celdas_llenas is None:
            celdas_llenas = contar_celdas_llenas(actual_sudoku)
    
    # Creamos el registro del historial
    registro = {
        "sudoku": actual_sudoku,
        "posibilidades": actual_posibilidades,
        "accion": accion,
        "celdas_llenas": celdas_llenas,
        "tiempo_ejecucion": st.session_state.get("tiempo_ejecucion", "N/A")
    }
    
    # Obtenemos el índice actual y el historial
    indice_actual = st.session_state.historico_indice
    historico = st.session_state.historico
    
    # Si estamos en medio del historial, eliminamos los estados futuros
    if indice_actual < len(historico) - 1:
        st.session_state.historico = historico[:indice_actual + 1]
    
    # Añadimos el nuevo estado al historial
    st.session_state.historico.append(registro)
    # Actualizamos el índice actual
    st.session_state.historico_indice = len(st.session_state.historico) - 1

def set_hist_index(target_idx):
    st.session_state.historico_indice = target_idx
    cargar_estado_desde_historico()

def render_historial():
    st.markdown("### Historial de transformaciones")
    
    indice_actual = st.session_state.historico_indice
    total_estados = len(st.session_state.historico)
    
    # Información del estado actual
    if total_estados > 0:
        estado_actual = st.session_state.historico[indice_actual]
        info_col1, info_col2, info_col3 = st.columns(3)
        
        with info_col1:
            st.metric("Estado actual", f"{indice_actual + 1} de {total_estados}")
        
        with info_col2:
            accion = estado_actual["accion"]
            st.metric("Acción aplicada", accion)
        
        with info_col3:
            if "celdas_llenas" in estado_actual and estado_actual["celdas_llenas"] is not None:
                metric_value = (estado_actual["celdas_llenas"] 
                              if estado_actual["accion"] == "regla0" 
                              else contar_celdas_llenas(estado_actual["sudoku"]))
                st.metric("Celdas llenas", metric_value)
    
    # Botones de navegación
    col1, col2 = st.columns(2)
    with col1:
        st.button("◀ Anterior", 
                on_click=on_anterior,
                disabled=(indice_actual <= 0),
                use_container_width=True)
    
    with col2:
        st.button("Siguiente ▶", 
                on_click=on_siguiente,
                disabled=(indice_actual >= total_estados - 1),
                use_container_width=True)
    
    # Nueva tabla con botones
    if total_estados > 0:
        st.markdown("#### Resumen de acciones")
        
        # Encabezados de la tabla
        cols = st.columns([2,3,4,4,5])
        with cols[0]: st.markdown("**Paso**")
        with cols[1]: st.markdown("**Acción**")
        with cols[2]: st.markdown("**Posibilidades únicas**")
        with cols[3]: st.markdown("**Tiempo (ms)**")
        with cols[4]: st.markdown("**Detalles**")
        
        # Filas con botones
        for original_idx in reversed(range(len(st.session_state.historico))):
            registro = st.session_state.historico[original_idx]
            is_current = original_idx == indice_actual
            
            # Cálculo de métricas
            posibilidades_un_valor = sum(1 for pos in registro["posibilidades"] 
                                    if isinstance(pos, list) and len(pos) == 1)
            
            celdas_resueltas = (registro["celdas_llenas"] 
                               if registro["accion"] == "regla0" 
                               else 0)
            
            tiempo = registro.get("tiempo_ejecucion", "N/A")
            
            # Crear fila
            cols = st.columns([2,3,4,4,5])
            with cols[0]:
                # Botón de navegación con estilo condicional
                btn_style = "primary" if is_current else "secondary"
                st.button(
                    str(original_idx + 1),
                    key=f"hist_{original_idx}",
                    on_click=set_hist_index,
                    args=(original_idx,),
                    type=btn_style,
                    use_container_width=True
                )
            
            # Resto de columnas
            with cols[1]: st.write(registro["accion"])
            with cols[2]: st.write(posibilidades_un_valor)
            with cols[3]: st.write(f"{tiempo} ms" if isinstance(tiempo, (int, float)) else tiempo)
            with cols[4]: 
                if registro["accion"] == "regla0":
                    st.write(f"Resueltas: {celdas_resueltas}")
                elif registro["accion"] == "input_usuario":
                    st.write(f"Celda modificada: {registro.get('celda', '')}")

        # Mantener funcionalidad de exportación
        if st.button("Exportar historial como CSV"):
            import pandas as pd
            datos = []
            for i, registro in enumerate(st.session_state.historico):
                datos.append({
                    "Paso": i+1,
                    "Acción": registro["accion"],
                    "Posibilidades Únicas": sum(1 for pos in registro["posibilidades"] 
                                              if isinstance(pos, list) and len(pos) == 1),
                    "Celdas Resueltas": registro.get("celdas_llenas", 0),
                    "Tiempo (ms)": registro.get("tiempo_ejecucion", "N/A")
                })
            df = pd.DataFrame(datos)
            st.download_button(
                label="Descargar CSV",
                data=df.to_csv(index=False),
                file_name="sudoku_historial.csv",
                mime="text/csv"
            )
# -------------------------------
# Configuración y flujo principal de Streamlit
def main():
    # Configurar página con dos barras laterales
    st.set_page_config(page_title="Sudoku Solver", layout="wide", initial_sidebar_state="expanded")
    
    # Inicializamos variables del estado si no existen
    if 'board_key' not in st.session_state:
        st.session_state.board_key = 0
    
    if 'need_refresh' not in st.session_state:
        st.session_state.need_refresh = False
    
    if 'mensaje' not in st.session_state:
        st.session_state.mensaje = None
    
    # Inicializamos las variables del histórico
    if 'historico' not in st.session_state:
        st.session_state.historico = []
    
    if 'historico_indice' not in st.session_state:
        st.session_state.historico_indice = -1
    
    # Inicializamos la variable para el algoritmo seleccionado
    if 'algoritmo_seleccionado' not in st.session_state:
        st.session_state.algoritmo_seleccionado = "default"
    
    # Inicializamos la variable para el tiempo de ejecución
    if 'tiempo_ejecucion' not in st.session_state:
        st.session_state.tiempo_ejecucion = "N/A"
    
    # Inicializamos la conexión con Prolog (se hace una única vez)
    if 'connector' not in st.session_state:
        st.session_state.connector = PrologConnector()
    
    # Panel lateral izquierdo para importar sudoku
    with st.sidebar:
        st.header("Importar Sudoku")
        uploaded_file = st.file_uploader("Sube un archivo .txt con el sudoku", 
                                        type=["txt"], 
                                        key=f"uploader_{st.session_state.board_key}")
        
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            sudoku = parse_sudoku_file(file_bytes)
            if sudoku is not None:
                st.session_state.sudoku = sudoku
                # Calculamos las posibilidades iniciales llamando a Prolog
                st.session_state.posibilidades = st.session_state.connector.calcular_posibilidades(sudoku)
                
                # Reiniciamos el histórico y añadimos el estado inicial
                st.session_state.historico = []
                st.session_state.historico_indice = 0
                
                # Guardamos el estado inicial en el histórico
                # guardar_estado_en_historial("inicial", contar_celdas_llenas(sudoku))
                
                st.success("Sudoku cargado correctamente.")
    
    # Crear columnas para el contenido principal y la barra lateral derecha
    main_col, right_sidebar_col = st.columns([4, 1], gap="large")
    
    with main_col:
        # Texto explicativo en la parte superior
        st.markdown("""
        # SudoQ
        """)
        
        # Si ya se cargó un sudoku, lo mostramos
        if 'sudoku' in st.session_state and 'posibilidades' in st.session_state:
            # Renderizamos el sudoku
            render_sudoku()
            
            # Renderizamos el historial debajo del sudoku
            render_historial()
            
            # Añadimos la sección de visualización de datos
            with st.expander("Visualización de datos para gráficos", expanded=False):
                plot_historial_data()
        else:
            st.info("Por favor, sube un sudoku en el panel lateral para comenzar.")
    
    # Panel lateral derecho para los botones de acción
    with right_sidebar_col:
        st.markdown("""
        <style>
            div[data-testid="column"]:nth-of-type(2) {
                padding: 0px 5px 0px 5px !important;
            }
        </style>
        """, unsafe_allow_html=True)

        if 'sudoku' in st.session_state and 'posibilidades' in st.session_state:

            st.markdown("""
            ### Descripción de Reglas
            
            - **Regla 0**: Completa celdas con una única posibilidad
            - **Regla 1**: Reduce posibilidades en filas
            - **Regla 2**: Reduce posibilidades en columnas
            - **Regla 3**: Reduce posibilidades en bloques 3x3
            """)
            st.markdown("### Acciones")
            st.button("Aplicar regla 0", 
                    key=f"regla0_{st.session_state.board_key}", 
                    on_click=on_regla, 
                    args=("regla0",),
                    use_container_width=True)
            
            st.button("Aplicar regla 1", 
                    key=f"regla1_{st.session_state.board_key}", 
                    on_click=on_regla, 
                    args=("regla1",),
                    use_container_width=True)
            
            st.button("Aplicar regla 2", 
                    key=f"regla2_{st.session_state.board_key}", 
                    on_click=on_regla, 
                    args=("regla2",),
                    use_container_width=True)
            
            st.button("Aplicar regla 3", 
                    key=f"regla3_{st.session_state.board_key}", 
                    on_click=on_regla, 
                    args=("regla3",),
                    use_container_width=True)
            
            st.markdown("---")
            
            # Dropdown para seleccionar el algoritmo de resolución
            st.markdown("### Algoritmo de resolución")
            algoritmos = {
                "R0-1-2-3": "R0-1-2-3",
                "R0-2-3-1": "R0-2-3-1",
                "R1-2-3-0": "R1-2-3-0",
                "R2-3-1-0": "R2-3-1-0",
                "R0": "R0",
                "R0-1": "R0-1",
                "R0-2": "R0-2",
                "R0-3": "R0-3",
            }
            
            st.selectbox(
                "Selecciona un algoritmo:",
                options=list(algoritmos.keys()),
                format_func=lambda x: algoritmos[x],
                key="algoritmo_seleccionado",
                index=0
            )
            
            st.button("Resolver Sudoku", 
                    key=f"resolver_{st.session_state.board_key}", 
                    on_click=on_regla, 
                    args=("resolver",),
                    use_container_width=True,
                    type="primary")

if __name__ == '__main__':
    main()
  