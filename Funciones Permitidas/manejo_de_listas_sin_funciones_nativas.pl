% Tutorial de Listas en Prolog sin funciones predefinidas

% 1. Obtener un elemento en la posicion N
obtener_n(0, [X|_], X).  % Caso base: si el indice es 0, devolvemos la cabeza.
obtener_n(N, [_|T], X) :-  
    N > 0,  
    N1 is N - 1,  
    obtener_n(N1, T, X).  % Recursion sobre la cola de la lista.

% Ejemplo de uso:
% ?- obtener_n(2, [a, b, c, d, e], X).
% X = c.



% 2. Recorrer una lista e imprimir cada elemento
imprimir_lista([]).  % Caso base: lista vacia, no hace nada.
imprimir_lista([X|T]) :-  
    write(X), nl,   % Escribe el elemento y salta de linea.
    imprimir_lista(T).  % Llamada recursiva para el resto de la lista.

% Ejemplo de uso:
% ?- imprimir_lista([1, 2, 3, 4, 5]).
% 1
% 2
% 3
% 4
% 5



% 3. Insertar un elemento en una posicion especifica
insertar_en_n(0, Elem, Lista, [Elem|Lista]).  % Caso base: Insertamos al inicio.
insertar_en_n(N, Elem, [X|T], [X|R]) :-  
    N > 0,  
    N1 is N - 1,  
    insertar_en_n(N1, Elem, T, R).  % Recursion sobre la cola.

% Ejemplo de uso:
% ?- insertar_en_n(2, x, [a, b, c, d], NuevaLista).
% NuevaLista = [a, b, x, c, d].



% 4. Eliminar un elemento de una posicion especifica
eliminar_n(0, [_|T], T).  % Caso base: Eliminamos el primer elemento.
eliminar_n(N, [X|T], [X|R]) :-  
    N > 0,  
    N1 is N - 1,  
    eliminar_n(N1, T, R).  % Recursion sobre la cola.

% Ejemplo de uso:
% ?- eliminar_n(2, [a, b, c, d], NuevaLista).
% NuevaLista = [a, b, d].



% 5. Obtener un elemento en una matriz (Fila, Columna)
obtener_elemento(F, C, Matriz, Elem) :-  
    obtener_n(F, Matriz, Fila),  
    obtener_n(C, Fila, Elem).

% Ejemplo de uso:
% ?- obtener_elemento(1, 2, [[1,2,3], [4,5,6], [7,8,9]], X).
% X = 6.



% 6. Imprimir una matriz
imprimir_matriz([]).  % Caso base: Si la matriz esta vacia, terminamos.
imprimir_matriz([Fila|Resto]) :-  
    imprimir_fila(Fila),  
    nl,  % Nueva linea despues de cada fila.
    imprimir_matriz(Resto).

imprimir_fila([]).  % Caso base: Si la fila esta vacia, terminamos.
imprimir_fila([X|T]) :-  
    write(X), write(' '),  % Imprime el numero con espacio.
    imprimir_fila(T).  % Llamada recursiva para el resto.

% Ejemplo de uso:
% ?- imprimir_matriz([[1,2,3], [4,5,6], [7,8,9]]).
% 1 2 3 
% 4 5 6 
% 7 8 9



% 7. Verificar si un elemento pertenece a una lista
pertenece(X, [X|_]).  % Caso base: el elemento es la cabeza de la lista
pertenece(X, [_|T]) :-  % Caso recursivo: buscar en la cola de la lista
    pertenece(X, T).

% Ejemplo de uso:
% ?- pertenece(b, [a, b, c, d]).
% true.

% ?- pertenece(x, [a, b, c, d]).
% false.
