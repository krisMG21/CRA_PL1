import streamlit as st
import ast
from pyswip import Prolog
import json
import time

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
        # Consultamos los archivos de reglas y el main.pl
        self.prolog.consult("sudokus.pl")
        self.prolog.consult("regla0.pl")
        self.prolog.consult("regla1.pl")
        self.prolog.consult("regla2.pl")
        self.prolog.consult("regla3.pl")
        self.prolog.consult("main.pl")
    
    def calcular_posibilidades(self, sudoku):
        # Llama a: posibles(S, Posibles).
        sudoku_str = sudoku_to_prolog(sudoku)
        query = f"posibles({sudoku_str}, Posibles)."
        resultados = list(self.prolog.query(query))
        if resultados:
            # Se espera que Posibles sea una lista de 81 elementos (cada uno: '.' o lista de números)
            return resultados[0]['Posibles']
        else:
            return None

    def aplicar_regla0(self, sudoku, posibilidades):
        # regla debe ser "regla0", "regla1", etc.
        sudoku_str = sudoku_to_prolog(sudoku)

        posibilidades_str = sudoku_to_prolog(posibilidades)  # en caso de ser lista plana o de listas
        query = f"regla0({sudoku_str}, {posibilidades_str}, NuevoS)."
        resultados = list(self.prolog.query(query))
        if resultados:
            return resultados[0]['NuevoS']
        else:
            return sudoku
        
    def aplicar_regla1(self, posibilidades):
        posibilidades_str = sudoku_to_prolog(posibilidades)  # en caso de ser lista plana o de listas
        query = f"regla1({posibilidades_str}, NuevoP)."
        resultados = list(self.prolog.query(query))
        if resultados:
            return resultados[0]['NuevoP']
        else:
            return posibilidades
        
    def aplicar_regla2(self, posibilidades):
        posibilidades_str = sudoku_to_prolog(posibilidades)  # en caso de ser lista plana o de listas
        query = f"regla2({posibilidades_str}, NuevoP)."
        resultados = list(self.prolog.query(query))
        if resultados:
            return resultados[0]['NuevoP']
        else:
            return posibilidades
        
    def aplicar_regla3(self, posibilidades):
        posibilidades_str = sudoku_to_prolog(posibilidades)  # en caso de ser lista plana o de listas
        query = f"regla3({posibilidades_str}, NuevoP)."
        resultados = list(self.prolog.query(query))
        if resultados:
            return resultados[0]['NuevoP']
        else:
            return posibilidades


    def aplicar_reglas(self, sudoku, posibilidades, algoritmo="default"):
        """
        Aplica reglas para resolver el sudoku según el algoritmo seleccionado
        
        Args:
            sudoku: Lista con el sudoku actual
            posibilidades: Lista con las posibilidades para cada celda
            algoritmo: String que define el algoritmo a utilizar
            
        Returns:
            nuevo_sudoku, nuevas_posibilidades
        """
        # Comportamiento predeterminado (algoritmo original)
        if algoritmo == "default":
            sudoku_str = sudoku_to_prolog(sudoku)
            posibilidades_str = sudoku_to_prolog(posibilidades)
            query = f"aplicar_reglas({sudoku_str}, {posibilidades_str}, NuevoS, NuevoP)."
            resultados = list(self.prolog.query(query))
            if resultados:
                return resultados[0]['NuevoS'], resultados[0]['NuevoP']
            else:
                return sudoku, posibilidades
        
        # Algoritmo de fuerza bruta
        elif algoritmo == "fuerza_bruta":
            # Implementación de placeholder - aquí iría la verdadera implementación
            # de un algoritmo de fuerza bruta
            st.session_state.mensaje = {"tipo": "info", "texto": "Utilizando algoritmo de fuerza bruta"}
            return self.aplicar_reglas(sudoku, posibilidades)  # Por ahora, usa el método default
        
        # Algoritmo de backtracking
        elif algoritmo == "backtracking":
            # Implementación de placeholder - aquí iría la verdadera implementación
            # de un algoritmo de backtracking
            st.session_state.mensaje = {"tipo": "info", "texto": "Utilizando algoritmo de backtracking"}
            return self.aplicar_reglas(sudoku, posibilidades)  # Por ahora, usa el método default
        
        # Algoritmo de dancing links
        elif algoritmo == "dancing_links":
            # Implementación de placeholder - aquí iría la verdadera implementación
            # de un algoritmo de dancing links (DLX)
            st.session_state.mensaje = {"tipo": "info", "texto": "Utilizando algoritmo de Dancing Links (DLX)"}
            return self.aplicar_reglas(sudoku, posibilidades)  # Por ahora, usa el método default
        
        # Algoritmo de simulated annealing
        elif algoritmo == "simulated_annealing":
            # Implementación de placeholder - aquí iría la verdadera implementación
            # de un algoritmo de simulated annealing
            st.session_state.mensaje = {"tipo": "info", "texto": "Utilizando algoritmo de Simulated Annealing"}
            return self.aplicar_reglas(sudoku, posibilidades)  # Por ahora, usa el método default
        
        # Si el algoritmo no es reconocido, usar el default
        else:
            st.warning(f"Algoritmo '{algoritmo}' no reconocido. Usando algoritmo predeterminado.")
            return self.aplicar_reglas(sudoku, posibilidades)

    def validar_movimiento(self, sudoku, index, valor):
        """
        Para validar un movimiento, primero se calculan las posibilidades y se comprueba
        que el valor ingresado se encuentre entre las opciones de la celda.
        """
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
        nuevo_sudoku, nuevas_poss = connector.aplicar_reglas(sudoku, posibilidades, algoritmo)
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
    tiempo_ejecucion = round((tiempo_fin - tiempo_inicio) * 1000, 2)  # en milisegundos
    st.session_state.tiempo_ejecucion = tiempo_ejecucion
    
    st.session_state.sudoku = nuevo_sudoku
    st.session_state.posibilidades = nuevas_poss
    
    # Guardamos el estado en el historial
    if regla == "regla0":
        celdas_despues = contar_celdas_llenas(nuevo_sudoku)
        celdas_llenadas = celdas_despues - celdas_antes
        guardar_estado_en_historial(accion, celdas_llenadas)
    else:
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
                    print(posibilidades)
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
        import pandas as pd
        import matplotlib.pyplot as plt
        import numpy as np
        
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
            casillas_resueltas = 0
            if accion == "regla0" and "celdas_llenas" in registro:
                casillas_resueltas = registro["celdas_llenas"]
            
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
        df["Casillas resueltas (acumulado)"] = df["Casillas resueltas"].cumsum()
        
        # Ofrecemos la visualización
        st.markdown("### Visualización de datos")
        
        # Opciones de visualización
        opcion_grafico = st.selectbox(
            "Selecciona un tipo de gráfico:",
            ["Posibilidades y Casillas (acumulado)", "Tiempo de ejecución"]
        )
        
        # Configuración común para los gráficos
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Generamos el gráfico seleccionado
        if opcion_grafico == "Posibilidades y Casillas (acumulado)":
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Gráfico para posibilidades con 1 valor (acumulado)
            ax.plot(df["Paso"], df["Posibilidades 1 valor (acumulado)"], 
                    marker='o', linestyle='-', linewidth=2, markersize=8, 
                    color='#1f77b4', label='Posibilidades con 1 valor (acumulado)')
            
            # Gráfico para casillas resueltas (acumulado)
            ax.plot(df["Paso"], df["Casillas resueltas (acumulado)"], 
                    marker='s', linestyle='-', linewidth=2, markersize=8, 
                    color='#ff7f0e', label='Casillas resueltas (acumulado)')
            
            # Añadimos los valores no acumulados como puntos más pequeños
            ax2 = ax.twinx()
            ax2.plot(df["Paso"], df["Posibilidades 1 valor"], 
                    marker='o', linestyle='--', linewidth=1, markersize=5, 
                    color='#17becf', label='Posibilidades con 1 valor (por paso)')
            ax2.plot(df["Paso"], df["Casillas resueltas"], 
                    marker='s', linestyle='--', linewidth=1, markersize=5, 
                    color='#d62728', label='Casillas resueltas (por paso)')
            
            # Configuramos los ejes
            ax.set_xlabel("Paso", fontsize=12)
            ax.set_ylabel("Valores acumulados", fontsize=12)
            ax2.set_ylabel("Valores por paso", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Configuramos los límites de los ejes
            ax.set_xlim(0.5, len(df) + 0.5)
            ax.set_xticks(np.arange(1, len(df) + 1))
            
            # Combinamos las leyendas de ambos ejes
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
            
            # Título del gráfico
            plt.title("Evolución de posibilidades y casillas resueltas", fontsize=14)
            
        else:  # Tiempo de ejecución
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Gráfico para tiempo de ejecución (no acumulado)
            ax.plot(df["Paso"], df["Tiempo (ms)"], 
                    marker='o', linestyle='-', linewidth=2, markersize=8, 
                    color='#2ca02c', label='Tiempo de ejecución')
            
            # Añadimos etiquetas con los valores en cada punto
            for i, txt in enumerate(df["Tiempo (ms)"]):
                if txt > 0:  # Solo mostramos etiquetas para valores positivos
                    ax.annotate(f"{txt} ms", 
                                (df["Paso"][i], df["Tiempo (ms)"][i]),
                                textcoords="offset points", 
                                xytext=(0,10), 
                                ha='center',
                                fontsize=9)
            
            # Configuramos los ejes
            ax.set_xlabel("Paso", fontsize=12)
            ax.set_ylabel("Tiempo (ms)", fontsize=12)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Configuramos los límites de los ejes
            ax.set_xlim(0.5, len(df) + 0.5)
            ax.set_xticks(np.arange(1, len(df) + 1))
            
            # Añadimos las acciones realizadas en cada paso como etiquetas en el eje x
            plt.xticks(rotation=45, ha='right')
            
            # Leyenda
            ax.legend(loc='upper left', fontsize=10)
            
            # Título del gráfico
            plt.title("Tiempo de ejecución por paso", fontsize=14)
        
        # Ajustamos el layout para que no se corten los elementos
        plt.tight_layout()
        
        # Mostramos el gráfico
        st.pyplot(fig)
        
        # Ofrecemos el DataFrame para análisis adicional
        st.dataframe(df)

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
        cols = st.columns([1,3,3,3,3,4])
        with cols[0]: st.markdown("**Paso**")
        with cols[1]: st.markdown("**Acción**")
        with cols[2]: st.markdown("**Posibilidades únicas**")
        with cols[3]: st.markdown("**Celdas resueltas**")
        with cols[4]: st.markdown("**Tiempo (ms)**")
        with cols[5]: st.markdown("**Detalles**")
        
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
            cols = st.columns([1,3,3,3,3,4])
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
            with cols[3]: st.write(celdas_resueltas if registro["accion"] == "regla0" else "-")
            with cols[4]: st.write(f"{tiempo} ms" if isinstance(tiempo, (int, float)) else tiempo)
            with cols[5]: 
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
                guardar_estado_en_historial("inicial", contar_celdas_llenas(sudoku))
                
                st.success("Sudoku cargado correctamente.")
    
    # Crear columnas para el contenido principal y la barra lateral derecha
    main_col, right_sidebar_col = st.columns([3, 1])
    
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
                "R1-2-3-0": "R1-2-3-0",
                "R1-0-2-0-3-0": "R1-0-2-0-3-0",
                "R3-0-2-0-1-0": "R3-0-2-0-1-0",
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
  