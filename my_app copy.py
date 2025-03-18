import streamlit as st
import ast
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Prolog_connector import PrologConnector

def aplicar_algoritmo(nombre_algoritmo, sudoku, posibilidades, connector):
    """Aplica un algoritmo de resolución del sudoku basado en una secuencia de reglas."""
    secuencia = nombre_algoritmo.split("-")
    cambio = True
    sudoku_actual, posibilidades_actual = sudoku.copy(), posibilidades.copy()
    acciones_realizadas = []
    indice = 0
    
    while cambio and indice < len(secuencia):
        regla = secuencia[indice]
        sudoku_nuevo, posibilidades_nuevo = sudoku_actual.copy(), posibilidades_actual.copy()
        tiempo_inicio = time.time()
        
        if regla in ["R0", "0"]:
            sudoku_nuevo = connector.aplicar_regla0(sudoku_actual, posibilidades_actual)
            posibilidades_nuevo = connector.calcular_posibilidades(sudoku_nuevo)
        elif regla in ["R1", "1"]:
            posibilidades_nuevo = connector.aplicar_regla1(posibilidades_actual)
        elif regla in ["R2", "2"]:
            posibilidades_nuevo = connector.aplicar_regla2(posibilidades_actual)
        elif regla in ["R3", "3"]:
            posibilidades_nuevo = connector.aplicar_regla3(posibilidades_actual)
            
        tiempo_ejecucion = int((time.time() - tiempo_inicio) * 1000)
        cambio_detectado = sudoku_nuevo != sudoku_actual or posibilidades_nuevo != posibilidades_actual
        
        if cambio_detectado:
            accion = {
                "regla": f"regla{regla[-1]}",
                "sudoku_antes": sudoku_actual.copy(),
                "sudoku_despues": sudoku_nuevo.copy(),
                "posibilidades_antes": posibilidades_actual.copy(),
                "posibilidades_despues": posibilidades_nuevo.copy(),
                "tiempo_ejecucion": tiempo_ejecucion
            }
            
            if regla in ["R0", "0"]:
                accion["celdas_cambiadas"] = sum(1 for i in range(len(sudoku_actual)) if sudoku_actual[i] != sudoku_nuevo[i])
                
            acciones_realizadas.append(accion)
            sudoku_actual, posibilidades_actual = sudoku_nuevo.copy(), posibilidades_nuevo.copy()
            indice = 0  # Reiniciamos para volver a la primera regla
        else:
            indice += 1
            cambio = indice < len(secuencia)
    
    return sudoku_actual, posibilidades_actual, acciones_realizadas

def aplicar_reglas(sudoku, posibilidades, connector, algoritmo="default"):
    algoritmos_disponibles = {
        "default": "R0-1-2-3", "R0-1-2-3": "R0-1-2-3", "R0-2-3-1": "R0-2-3-1", 
        "R0-3-2-1": "R0-3-2-1", "R1-2-3-0": "R1-2-3-0", "R2-3-1-0": "R2-3-1-0", 
        "R3-2-1-0": "R3-2-1-0", "R0-1": "R0-1", "R0-2": "R0-2", "R0-3": "R0-3",
        "R1-0-2-0-3-0": "R1-0-2-0-3-0", "R3-0-2-0-1-0": "R3-0-2-0-1-0"
    }
    
    if algoritmo not in algoritmos_disponibles:
        st.warning(f"Algoritmo '{algoritmo}' no reconocido. Usando algoritmo predeterminado.")
        algoritmo = "default"
    
    nuevo_sudoku, nuevas_posibilidades, acciones = aplicar_algoritmo(
        algoritmos_disponibles[algoritmo], sudoku, posibilidades, connector)
    
    # Registramos las acciones en el historial
    historico = st.session_state.historico
    indice_actual = st.session_state.historico_indice
    
    if indice_actual < len(historico) - 1:
        st.session_state.historico = historico[:indice_actual + 1]
    
    for accion in acciones:
        registro = {
            "sudoku": accion["sudoku_despues"],
            "posibilidades": accion["posibilidades_despues"],
            "accion": f"{accion['regla']} ({algoritmo})",
            "tiempo_ejecucion": accion.get("tiempo_ejecucion", "N/A")
        }
        
        if accion["regla"] == "regla0" and "celdas_cambiadas" in accion:
            registro["celdas_llenas"] = accion["celdas_cambiadas"]
        
        st.session_state.historico.append(registro)
    
    # Si no hubo acciones, añadimos una entrada indicando que no hubo cambios
    if not acciones:
        st.session_state.historico.append({
            "sudoku": nuevo_sudoku,
            "posibilidades": nuevas_posibilidades,
            "accion": f"Sin cambios ({algoritmo})",
            "tiempo_ejecucion": "N/A"
        })
    
    st.session_state.historico_indice = len(st.session_state.historico) - 1
    return nuevo_sudoku, nuevas_posibilidades

def parse_sudoku_file(file_content):
    try:
        sudoku = ast.literal_eval(file_content.decode("utf-8"))
        if isinstance(sudoku, list) and len(sudoku) == 81:
            return sudoku
        else:
            st.error("El sudoku debe ser una lista de 81 elementos.")
            return None
    except Exception as e:
        st.error(f"Error al parsear el archivo: {e}")
        return None

def contar_celdas_llenas(sudoku):
    return sum(1 for celda in sudoku if celda != '.')

def guardar_estado_en_historial(accion, celdas_llenas=None):
    # Creamos el registro del historial
    if accion in ["input_usuario", "regla0"] and celdas_llenas is None:
        celdas_llenas = contar_celdas_llenas(st.session_state.sudoku)
    
    registro = {
        "sudoku": st.session_state.sudoku.copy(),
        "posibilidades": st.session_state.posibilidades,
        "accion": accion,
        "celdas_llenas": celdas_llenas,
        "tiempo_ejecucion": st.session_state.get("tiempo_ejecucion", "N/A")
    }
    
    # Si estamos en medio del historial, eliminamos los estados futuros
    if st.session_state.historico_indice < len(st.session_state.historico) - 1:
        st.session_state.historico = st.session_state.historico[:st.session_state.historico_indice + 1]
    
    st.session_state.historico.append(registro)
    st.session_state.historico_indice = len(st.session_state.historico) - 1

def on_cell_change(idx):
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
    
    valido, mensaje = connector.validar_movimiento(sudoku, idx, valor_ingresado)
    
    if valido:
        sudoku[idx] = int(valor_ingresado)
        st.session_state.sudoku = sudoku
        st.session_state.posibilidades = connector.calcular_posibilidades(sudoku)
        guardar_estado_en_historial("input_usuario", contar_celdas_llenas(sudoku))
        st.session_state.mensaje = {"tipo": "exito", "texto": f"Celda {idx+1}: {mensaje}"}
        st.session_state.need_refresh = True
        st.session_state.board_key = int(time.time() * 1000)
    else:
        st.session_state.mensaje = {"tipo": "error", "texto": f"Celda {idx+1}: {mensaje}"}
        st.session_state[f"cell_{idx}"] = ""

def on_regla(regla):
    sudoku = st.session_state.sudoku
    posibilidades = st.session_state.posibilidades
    connector = st.session_state.connector
    celdas_antes = contar_celdas_llenas(sudoku)
    tiempo_inicio = time.time()
    
    if regla == "resolver":
        algoritmo = st.session_state.algoritmo_seleccionado
        accion = f"resolver ({algoritmo})"
        nuevo_sudoku, nuevas_poss = aplicar_reglas(sudoku, posibilidades, connector, algoritmo)
    elif regla == "regla0":
        accion = regla
        nuevo_sudoku = connector.aplicar_regla0(sudoku, posibilidades)
        nuevas_poss = connector.calcular_posibilidades(nuevo_sudoku) if sudoku != nuevo_sudoku else posibilidades
    elif regla == "regla1":
        accion = regla
        nuevo_sudoku, nuevas_poss = sudoku, connector.aplicar_regla1(posibilidades)
    elif regla == "regla2":
        accion = regla
        nuevo_sudoku, nuevas_poss = sudoku, connector.aplicar_regla2(posibilidades)
    elif regla == "regla3":
        accion = regla
        nuevo_sudoku, nuevas_poss = sudoku, connector.aplicar_regla3(posibilidades)
    else:
        accion = regla
        nuevo_sudoku = connector.aplicar_regla(regla, sudoku, posibilidades)
        nuevas_poss = connector.calcular_posibilidades(nuevo_sudoku)
    
    tiempo_ejecucion = round((time.time() - tiempo_inicio) * 1000, 0)
    st.session_state.tiempo_ejecucion = tiempo_ejecucion
    st.session_state.sudoku = nuevo_sudoku
    st.session_state.posibilidades = nuevas_poss
    
    if regla == "regla0":
        celdas_despues = contar_celdas_llenas(nuevo_sudoku)
        guardar_estado_en_historial(accion, celdas_despues - celdas_antes)
    elif "regla" in regla:
        guardar_estado_en_historial(accion)
    
    st.session_state.mensaje = {"tipo": "info", "texto": f"Se ha aplicado {accion} al sudoku (tiempo: {tiempo_ejecucion} ms)"}
    st.session_state.need_refresh = True
    st.session_state.board_key = int(time.time() * 1000)

def cargar_estado_desde_historico():
    indice = st.session_state.historico_indice
    registro = st.session_state.historico[indice]
    st.session_state.sudoku = registro["sudoku"]
    st.session_state.posibilidades = registro["posibilidades"]
    st.session_state.mensaje = {"tipo": "info", "texto": f"Cargado estado histórico #{indice+1} - Acción: {registro['accion']}"}
    st.session_state.need_refresh = True
    st.session_state.board_key = int(time.time() * 1000)

def format_posibilidades(posibles):
    return "" if posibles == '.' else "[" + ",".join(map(str, posibles)) + "]"

def render_sudoku():
    st.markdown("""
        <style>
        input { text-align: center; }
        input:disabled { font-weight: bold; color: white; background-color: #333; text-align: center; }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown("### Sudoku")
    sudoku = st.session_state.sudoku
    posibilidades = st.session_state.posibilidades
    
    if 'mensaje' in st.session_state and st.session_state.mensaje:
        tipo_mensaje = st.session_state.mensaje["tipo"]
        texto_mensaje = st.session_state.mensaje["texto"]
        if tipo_mensaje == "exito":
            st.success(texto_mensaje)
        elif tipo_mensaje == "error":
            st.warning(texto_mensaje)
        else:
            st.info(texto_mensaje)
        st.session_state.mensaje = None
    
    # Función para mapear la columna j a la columna real en st.columns
    def map_col(j):
        return j + (1 if j >= 3 else 0) + (1 if j >= 6 else 0)
    
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
                    placeholder = format_posibilidades(posibilidades[idx])
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
            posibilidades_un_valor = sum(1 for pos in registro.get("posibilidades", []) 
                                        if pos != '.' and isinstance(pos, list) and len(pos) == 1)
            
            # Calculamos casillas resueltas
            casillas_resueltas = registro.get("celdas_llenas", 0) if accion == "regla0" else 0
            
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
        df["Posibilidades 1 valor (acumulado)"] = df["Posibilidades 1 valor"].cumsum()
        df["Casillas resueltas (acumulado)"] = df["Casillas resueltas"].cumsum()
        
        # Opciones de visualización
        st.markdown("### Visualización de datos")
        opcion_grafico = st.selectbox(
            "Selecciona un tipo de gráfico:",
            ["Posibilidades y Casillas (acumulado)", "Tiempo de ejecución"]
        )
        
        plt.style.use('seaborn-v0_8-darkgrid')
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if opcion_grafico == "Posibilidades y Casillas (acumulado)":
            # Gráfico para valores acumulados
            ax.plot(df["Paso"], df["Posibilidades 1 valor (acumulado)"], 
                   marker='o', linestyle='-', linewidth=2, markersize=8, 
                   color='#1f77b4', label='Posibilidades con 1 valor (acumulado)')
            ax.plot(df["Paso"], df["Casillas resueltas (acumulado)"], 
                   marker='s', linestyle='-', linewidth=2, markersize=8, 
                   color='#ff7f0e', label='Casillas resueltas (acumulado)')
            
            # Valores no acumulados como puntos más pequeños (eje secundario)
            ax2 = ax.twinx()
            ax2.plot(df["Paso"], df["Posibilidades 1 valor"], 
                    marker='o', linestyle='--', linewidth=1, markersize=5, 
                    color='#17becf', label='Posibilidades con 1 valor (por paso)')
            ax2.plot(df["Paso"], df["Casillas resueltas"], 
                    marker='s', linestyle='--', linewidth=1, markersize=5, 
                    color='#d62728', label='Casillas resueltas (por paso)')
            
            ax.set_xlabel("Paso", fontsize=12)
            ax.set_ylabel("Valores acumulados", fontsize=12)
            ax2.set_ylabel("Valores por paso", fontsize=12)
            
            # Combinamos las leyendas
            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
            plt.title("Evolución de posibilidades y casillas resueltas", fontsize=14)
        else:  # Tiempo de ejecución
            ax.plot(df["Paso"], df["Tiempo (ms)"], 
                   marker='o', linestyle='-', linewidth=2, markersize=8, 
                   color='#2ca02c', label='Tiempo de ejecución')
            
            # Añadimos etiquetas con los valores
            for i, txt in enumerate(df["Tiempo (ms)"]):
                if txt > 0:
                    ax.annotate(f"{txt} ms", 
                               (df["Paso"][i], df["Tiempo (ms)"][i]),
                               textcoords="offset points", 
                               xytext=(0,10), 
                               ha='center',
                               fontsize=9)
            
            ax.set_xlabel("Paso", fontsize=12)
            ax.set_ylabel("Tiempo (ms)", fontsize=12)
            ax.legend(loc='upper left', fontsize=10)
            plt.title("Tiempo de ejecución por paso", fontsize=14)
        
        # Configuración común
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(0.5, len(df) + 0.5)
        ax.set_xticks(np.arange(1, len(df) + 1))
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        st.pyplot(fig)
        st.dataframe(df)

def set_hist_index(target_idx):
    st.session_state.historico_indice = target_idx
    cargar_estado_desde_historico()

def render_historial():
    st.markdown("### Historial de transformaciones")
    indice_actual = st.session_state.historico_indice
    total_estados = len(st.session_state.historico)
    
    if total_estados > 0:
        estado_actual = st.session_state.historico[indice_actual]
        info_cols = st.columns(3)
        
        with info_cols[0]:
            st.metric("Estado actual", f"{indice_actual + 1} de {total_estados}")
        with info_cols[1]:
            st.metric("Acción aplicada", estado_actual["accion"])
        with info_cols[2]:
            if "celdas_llenas" in estado_actual and estado_actual["celdas_llenas"] is not None:
                valor_metrica = (estado_actual["celdas_llenas"] 
                              if estado_actual["accion"] == "regla0" 
                              else contar_celdas_llenas(estado_actual["sudoku"]))
                st.metric("Celdas llenas", valor_metrica)
    
    # Botones de navegación
    col1, col2 = st.columns(2)
    with col1:
        st.button("◀ Anterior", on_click=lambda: set_hist_index(indice_actual-1),
                disabled=(indice_actual <= 0), use_container_width=True)
    with col2:
        st.button("Siguiente ▶", on_click=lambda: set_hist_index(indice_actual+1),
                disabled=(indice_actual >= total_estados - 1), use_container_width=True)
    
    if total_estados > 0:
        st.markdown("#### Resumen de acciones")
        
        # Encabezados de la tabla
        cols = st.columns([2,3,4,4,5])
        for i, header in enumerate(["**Paso**", "**Acción**", "**Posibilidades únicas**", "**Tiempo (ms)**", "**Detalles**"]):
            with cols[i]: st.markdown(header)
        
        # Filas con botones
        for original_idx in reversed(range(total_estados)):
            registro = st.session_state.historico[original_idx]
            is_current = original_idx == indice_actual
            
            # Métricas
            posibilidades_un_valor = sum(1 for pos in registro["posibilidades"] 
                                       if isinstance(pos, list) and len(pos) == 1)
            celdas_resueltas = registro.get("celdas_llenas", 0) if registro["accion"] == "regla0" else 0
            tiempo = registro.get("tiempo_ejecucion", "N/A")
            
            # Crear fila
            row_cols = st.columns([2,3,4,4,5])
            with row_cols[0]:
                btn_style = "primary" if is_current else "secondary"
                st.button(str(original_idx + 1), key=f"hist_{original_idx}",
                         on_click=set_hist_index, args=(original_idx,),
                         type=btn_style, use_container_width=True)
            
            with row_cols[1]: st.write(registro["accion"])
            with row_cols[2]: st.write(posibilidades_un_valor)
            with row_cols[3]: st.write(f"{tiempo} ms" if isinstance(tiempo, (int, float)) else tiempo)
            with row_cols[4]: 
                if registro["accion"] == "regla0":
                    st.write(f"Resueltas: {celdas_resueltas}")
                elif registro["accion"] == "input_usuario":
                    st.write(f"Celda modificada: {registro.get('celda', '')}")

        # Exportación CSV
        if st.button("Exportar historial como CSV"):
            datos_export = [{
                "Paso": i+1,
                "Acción": reg["accion"],
                "Posibilidades Únicas": sum(1 for pos in reg["posibilidades"] 
                                           if isinstance(pos, list) and len(pos) == 1),
                "Celdas Resueltas": reg.get("celdas_llenas", 0),
                "Tiempo (ms)": reg.get("tiempo_ejecucion", "N/A")
            } for i, reg in enumerate(st.session_state.historico)]
            
            df_export = pd.DataFrame(datos_export)
            st.download_button(
                label="Descargar CSV",
                data=df_export.to_csv(index=False),
                file_name="sudoku_historial.csv",
                mime="text/csv"
            )

def main():
    # Configuración de página
    st.set_page_config(page_title="Sudoku Solver", layout="wide", initial_sidebar_state="expanded")
    
    # Inicialización de variables de estado
    for key, default_value in {
        'board_key': 0,
        'need_refresh': False,
        'mensaje': None,
        'historico': [],
        'historico_indice': -1,
        'algoritmo_seleccionado': "default",
        'tiempo_ejecucion': "N/A",
        'connector': PrologConnector()
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Panel lateral izquierdo
    with st.sidebar:
        st.header("Importar Sudoku")
        uploaded_file = st.file_uploader("Sube un archivo .txt con el sudoku", 
                                       type=["txt"], 
                                       key=f"uploader_{st.session_state.board_key}")
        
        if uploaded_file is not None:
            sudoku = parse_sudoku_file(uploaded_file.read())
            if sudoku is not None:
                st.session_state.sudoku = sudoku
                st.session_state.posibilidades = st.session_state.connector.calcular_posibilidades(sudoku)
                st.session_state.historico = []
                st.session_state.historico_indice = 0
                st.success("Sudoku cargado correctamente.")
    
    # Estructura principal
    main_col, right_sidebar_col = st.columns([3, 1])
    
    with main_col:
        st.markdown("# SudoQ")
        
        if 'sudoku' in st.session_state and 'posibilidades' in st.session_state:
            render_sudoku()
            render_historial()
            with st.expander("Visualización de datos para gráficos", expanded=False):
                plot_historial_data()
        else:
            st.info("Por favor, sube un sudoku en el panel lateral para comenzar.")
    
    # Panel lateral derecho
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
            for regla in ["regla0", "regla1", "regla2", "regla3"]:
                st.button(f"Aplicar {regla}", key=f"{regla}_{st.session_state.board_key}", 
                        on_click=on_regla, args=(regla,), use_container_width=True)
            
            st.markdown("---")
            st.markdown("### Algoritmo de resolución")
            
            algoritmos = {
                "R0-1-2-3": "R0-1-2-3",
                "R1-2-3-0": "R1-2-3-0",
                "R1-0-2-0-3-0": "R1-0-2-0-3-0",
                "R3-0-2-0-1-0": "R3-0-2-0-1-0",
            }
            
            st.selectbox("Selecciona un algoritmo:", options=list(algoritmos.keys()),
                       format_func=lambda x: algoritmos[x], key="algoritmo_seleccionado")
            
            st.button("Resolver Sudoku", key=f"resolver_{st.session_state.board_key}", 
                    on_click=on_regla, args=("resolver",), use_container_width=True, type="primary")

if __name__ == '__main__':
    main()