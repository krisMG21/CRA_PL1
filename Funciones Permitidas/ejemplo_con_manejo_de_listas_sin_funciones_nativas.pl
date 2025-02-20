% Importar las funciones definidas previamente
% Obtener un elemento en la posición N
obtener_n(0, [X|_], X).  
obtener_n(N, [_|T], X) :-  
    N > 0,  
    N1 is N - 1,  
    obtener_n(N1, T, X).  

% Recorrer una lista e imprimir cada elemento
imprimir_lista([]).  
imprimir_lista([X|T]) :-  
    write(X), nl,   
    imprimir_lista(T).  

% Insertar un elemento en una posición específica
insertar_en_n(0, Elem, Lista, [Elem|Lista]).  
insertar_en_n(N, Elem, [X|T], [X|R]) :-  
    N > 0,  
    N1 is N - 1,  
    insertar_en_n(N1, Elem, T, R).  

% Eliminar un elemento de una posición específica
eliminar_n(0, [_|T], T).  
eliminar_n(N, [X|T], [X|R]) :-  
    N > 0,  
    N1 is N - 1,  
    eliminar_n(N1, T, R).  

% Obtener un elemento en una matriz (Fila, Columna)
obtener_elemento(F, C, Matriz, Elem) :-  
    obtener_n(F, Matriz, Fila),  
    obtener_n(C, Fila, Elem).  

% Imprimir una matriz
imprimir_matriz([]).  
imprimir_matriz([Fila|Resto]) :-  
    imprimir_fila(Fila),  
    nl,  
    imprimir_matriz(Resto).

imprimir_fila([]).  
imprimir_fila([X|T]) :-  
    write(X), write(' '),  
    imprimir_fila(T).  

% Procedimiento principal para probar las funciones
gestor_listas_matrices :-
    % Definir una lista de ejemplo
    ListaOriginal = ["rojo", "verde", "azul", "amarillo", "negro"],

    % Imprimir la lista original
    write("Lista original: "), nl,
    imprimir_lista(ListaOriginal), nl,
    
    % Obtener el tercer elemento (posición 2)
    obtener_n(2, ListaOriginal, ColorObtenido),
    
    % Insertar "blanco" en la posición 1
    insertar_en_n(1, "blanco", ListaOriginal, ListaConBlanco),
    
    % Eliminar el cuarto elemento (posición 3)
    eliminar_n(3, ListaConBlanco, ListaFinal),
    
    % Imprimir resultados de la lista
    write("Elemento en posición 2: "), write(ColorObtenido), nl,
    write("Lista después de insertar 'blanco': "), nl,
    imprimir_lista(ListaConBlanco), nl,
    write("Lista después de eliminar el cuarto elemento: "), nl,
    imprimir_lista(ListaFinal), nl,
    
    % Definir una matriz de ejemplo
    Matriz = [
        ["rojo", "verde", "azul"],
        ["amarillo", "negro", "blanco"],
        ["morado", "cian", "gris"]
    ],

    % Imprimir la matriz original
    write("Imprimir la matriz original: "), nl, imprimir_matriz(Matriz), nl,

    
    % Obtener el elemento en fila 2, columna 1 (recordando que en Prolog el índice comienza en 0)
    obtener_elemento(1, 2, Matriz, ElementoMatriz), nl,
    
    % Imprimir la matriz completa
    write("Elemento en la posición (1,2) de la matriz: "), write(ElementoMatriz).
