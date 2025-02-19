import streamlit as st
import ast
from pyswip import Prolog
import json

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
        print(resultados)
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
# Función para renderizar el sudoku (con bordes destacados y celdas interactivas)
def render_sudoku(sudoku, posibilidades, connector):
    st.markdown("### Sudoku")
    print(posibilidades)
    # Usamos un contenedor para la grilla
    for i in range(9):
        cols = st.columns(9)
        for j in range(9):
            idx = i * 9 + j
            # Definimos estilos para los bordes (más gruesos para subcuadrantes)
            top_border    = "2px solid black" if i % 3 == 0 else "1px solid grey"
            bottom_border = "2px solid black" if i == 8 or (i+1) % 3 == 0 else "1px solid grey"
            left_border   = "2px solid black" if j % 3 == 0 else "1px solid grey"
            right_border  = "2px solid black" if j == 8 or (j+1) % 3 == 0 else "1px solid grey"
            cell_style = f"""
                padding: 10px;
                text-align: center;
                font-size: 24px;
                border-top: {top_border};
                border-bottom: {bottom_border};
                border-left: {left_border};
                border-right: {right_border};
                min-width: 60px;
                min-height: 60px;
            """
            # Si la celda está llena, mostramos el número; si no, mostramos un input y las posibilidades
            if sudoku[idx] != '.':
                cols[j].markdown(f"<div style='{cell_style}'>{sudoku[idx]}</div>", unsafe_allow_html=True)
            else:
                # Mostramos el input y debajo las posibilidades (en letra pequeña y color claro)
                # Usamos text_input; su valor se captura en session_state con clave única "cell_{idx}"
                # Se incluye un placeholder que muestra las opciones.
                key_name = f"cell_{idx}"
                # Se crea un contenedor para la celda con un div y luego se inserta el text_input (debido a las limitaciones de Streamlit, se
                # usará el input sin estilos extra; el div lo usamos para marcar la celda)
                print(cols[j])
                valor_ingresado = cols[j].text_input("", value="", key=key_name, placeholder="|".join(map(str, posibilidades[idx])))
                # Si se ingresa un valor (y es distinto de la cadena vacía), se valida mediante Prolog
                if valor_ingresado != "":
                    valido, mensaje = connector.validar_movimiento(sudoku, idx, valor_ingresado)
                    if valido:
                        sudoku[idx] = int(valor_ingresado)
                        st.success(f"Celda {idx+1}: {mensaje}")
                        # Se puede recalcular las posibilidades después de cada movimiento
                        nuevas_poss = connector.calcular_posibilidades(sudoku)
                        posibilidades[idx] = nuevas_poss[idx]
                        # Se limpia el input
                        st.session_state[key_name] = ""
                    else:
                        st.warning(f"Celda {idx+1}: {mensaje}")
                # Finalmente, se muestra la caja con las posibilidades en formato pequeño
                cols[j].markdown(f"<div style='font-size: 10px; color: #777;'>{posibilidades[idx]}</div>", unsafe_allow_html=True)

# -------------------------------
# Configuración y flujo principal de Streamlit
def main():
    st.set_page_config(page_title="Sudoku Solver", layout="wide")
    
    # Texto explicativo en la parte superior
    st.markdown("""
    # Resolvedor de Sudokus 9x9
    Esta aplicación resuelve sudokus de 9x9 utilizando un motor de reglas implementado en Prolog.
    
    El sudoku se representa como una lista de 81 elementos. Las celdas vacías se indican con un punto ('.'). 
    Antes de mostrar el sudoku, se calculan las posibilidades de cada celda vacía. Podrás interactuar 
    ingresando números en las celdas vacías; se consultará Prolog para validar cada movimiento. Además, dispones de
    botones para aplicar reglas parciales (regla0, regla1, regla2 y regla3) y un botón para resolver el sudoku 
    automáticamente mediante la función aplicar_reglas.
    """)

    # Inicializamos la conexión con Prolog (se hace una única vez)
    if 'connector' not in st.session_state:
        st.session_state.connector = PrologConnector()

    connector = st.session_state.connector

    # Panel lateral para importar sudoku
    st.sidebar.header("Importar Sudoku")
    uploaded_file = st.sidebar.file_uploader("Sube un archivo .txt con el sudoku", type=["txt"])
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        sudoku = parse_sudoku_file(file_bytes)
        if sudoku is not None:
            st.session_state.sudoku = sudoku
            # Calculamos las posibilidades iniciales llamando a Prolog
            st.session_state.posibilidades = connector.calcular_posibilidades(sudoku)
            st.sidebar.success("Sudoku cargado correctamente.")

    # Si ya se cargó un sudoku, lo mostramos en el centro
    if 'sudoku' in st.session_state and 'posibilidades' in st.session_state:
        sudoku = st.session_state.sudoku
        posibilidades = st.session_state.posibilidades
        
        # Renderizamos el sudoku (centrado)
        render_sudoku(sudoku, posibilidades, connector)
        
        st.markdown("---")
        st.markdown("### Acciones")
        col1, col2, col3, col4, col5 = st.columns(5)
        if col1.button("Aplicar regla 0"):
            nuevo_sudoku = connector.aplicar_regla("regla0", sudoku, posibilidades)
            st.session_state.sudoku = nuevo_sudoku
            st.session_state.posibilidades = connector.calcular_posibilidades(nuevo_sudoku)
            st.experimental_rerun()
        if col2.button("Aplicar regla 1"):
            nuevo_sudoku = connector.aplicar_regla("regla1", sudoku, posibilidades)
            st.session_state.sudoku = nuevo_sudoku
            st.session_state.posibilidades = connector.calcular_posibilidades(nuevo_sudoku)
            st.experimental_rerun()
        if col3.button("Aplicar regla 2"):
            nuevo_sudoku = connector.aplicar_regla("regla2", sudoku, posibilidades)
            st.session_state.sudoku = nuevo_sudoku
            st.session_state.posibilidades = connector.calcular_posibilidades(nuevo_sudoku)
            st.experimental_rerun()
        if col4.button("Aplicar regla 3"):
            nuevo_sudoku = connector.aplicar_regla("regla3", sudoku, posibilidades)
            st.session_state.sudoku = nuevo_sudoku
            st.session_state.posibilidades = connector.calcular_posibilidades(nuevo_sudoku)
            st.experimental_rerun()
        if col5.button("Resolver Sudoku"):
            nuevo_sudoku, nuevas_poss = connector.aplicar_reglas(sudoku, posibilidades)
            st.session_state.sudoku = nuevo_sudoku
            st.session_state.posibilidades = nuevas_poss
            st.experimental_rerun()
    else:
        st.info("Por favor, sube un sudoku en el panel lateral para comenzar.")

if __name__ == '__main__':
    main()
