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

    def aplicar_regla(self, regla, sudoku, posibilidades):
        # regla debe ser "regla0", "regla1", etc.
        sudoku_str = sudoku_to_prolog(sudoku)

        posibilidades_str = sudoku_to_prolog(posibilidades)  # en caso de ser lista plana o de listas
        query = f"{regla}({sudoku_str}, {posibilidades_str}, NuevoS)."
        resultados = list(self.prolog.query(query))
        if resultados:
            return resultados[0]['NuevoS']
        else:
            return sudoku

    def aplicar_reglas(self, sudoku, posibilidades):
        # Llama a aplicar_reglas(S, P, NewS, NewP) para resolver el sudoku
        sudoku_str = sudoku_to_prolog(sudoku)
        posibilidades_str = sudoku_to_prolog(posibilidades)
        query = f"aplicar_reglas({sudoku_str}, {posibilidades_str}, NuevoS, NuevoP)."
        resultados = list(self.prolog.query(query))
        if resultados:
            return resultados[0]['NuevoS'], resultados[0]['NuevoP']
        else:
            return sudoku, posibilidades

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
    
    if regla == "resolver":
        nuevo_sudoku, nuevas_poss = connector.aplicar_reglas(sudoku, posibilidades)
    else:
        nuevo_sudoku = connector.aplicar_regla(regla, sudoku, posibilidades)
        nuevas_poss = connector.calcular_posibilidades(nuevo_sudoku)
    
    st.session_state.sudoku = nuevo_sudoku
    st.session_state.posibilidades = nuevas_poss
    st.session_state.mensaje = {"tipo": "info", "texto": f"Se ha aplicado {regla} al sudoku"}
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

# -------------------------------
# Configuración y flujo principal de Streamlit
def main():
    st.set_page_config(page_title="Sudoku Solver", layout="wide")
    
    # Inicializamos variables del estado si no existen
    if 'board_key' not in st.session_state:
        st.session_state.board_key = 0
    
    if 'need_refresh' not in st.session_state:
        st.session_state.need_refresh = False
    
    if 'mensaje' not in st.session_state:
        st.session_state.mensaje = None
    
    # Inicializamos la conexión con Prolog (se hace una única vez)
    if 'connector' not in st.session_state:
        st.session_state.connector = PrologConnector()
    
    # Texto explicativo en la parte superior
    st.markdown("""
    # SudoQ
    Esta aplicación resuelve sudokus de 9x9 utilizando un motor de reglas implementado en Prolog.
    
    El sudoku se representa como una lista de 81 elementos. Las celdas vacías se indican con un punto ('.'). 
    Antes de mostrar el sudoku, se calculan las posibilidades de cada celda vacía. Podrás interactuar 
    ingresando números en las celdas vacías; se consultará Prolog para validar cada movimiento. Además, dispones de
    botones para aplicar reglas parciales (regla0, regla1, regla2 y regla3) y un botón para resolver el sudoku 
    automáticamente mediante la función aplicar_reglas.
    """)
    
    # Panel lateral para importar sudoku
    st.sidebar.header("Importar Sudoku")
    uploaded_file = st.sidebar.file_uploader("Sube un archivo .txt con el sudoku", 
                                             type=["txt"], 
                                             key=f"uploader_{st.session_state.board_key}")
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        sudoku = parse_sudoku_file(file_bytes)
        if sudoku is not None:
            st.session_state.sudoku = sudoku
            # Calculamos las posibilidades iniciales llamando a Prolog
            st.session_state.posibilidades = st.session_state.connector.calcular_posibilidades(sudoku)
            st.sidebar.success("Sudoku cargado correctamente.")
    
    # Si ya se cargó un sudoku, lo mostramos en el centro
    if 'sudoku' in st.session_state and 'posibilidades' in st.session_state:
        # Renderizamos el sudoku (centrado)
        render_sudoku()
        
        st.markdown("---")
        st.markdown("### Acciones")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Usamos on_click con callbacks para evitar reruns
        col1.button("Aplicar regla 0", 
                   key=f"regla0_{st.session_state.board_key}", 
                   on_click=on_regla, 
                   args=("regla0",))
        
        col2.button("Aplicar regla 1", 
                   key=f"regla1_{st.session_state.board_key}", 
                   on_click=on_regla, 
                   args=("regla1",))
        
        col3.button("Aplicar regla 2", 
                   key=f"regla2_{st.session_state.board_key}", 
                   on_click=on_regla, 
                   args=("regla2",))
        
        col4.button("Aplicar regla 3", 
                   key=f"regla3_{st.session_state.board_key}", 
                   on_click=on_regla, 
                   args=("regla3",))
        
        col5.button("Resolver Sudoku", 
                   key=f"resolver_{st.session_state.board_key}", 
                   on_click=on_regla, 
                   args=("resolver",))
    else:
        st.info("Por favor, sube un sudoku en el panel lateral para comenzar.")

if __name__ == '__main__':
    main()