% Representación de un Sudoku
sudoku([
    '.', '.', 3, '.', 2, '.', 7, '.', '.',
    5, '.', '.', '.', '.', '.', 4, '.', 3,
    '.', '.', 3, '.', '.', '.', 2, 5, '.',
    '.', 5, '.', 1, '.', 6, '.', '.', '.',
    '.', '.', 4, 8, '.', 7, '.', '.', '.',
    2, 3, 7, 6, '.', 4, 8, '.', '.',
    '.', 8, '.', '.', '.', 2, '.', 7, '.',
    3, '.', '.', 4, '.', '.', 2, '.', 8,
    '.', '.', 9, '.', '.', '.', '.', 6, '.'
]).
% REGLAS DE EJECUCIÓN.
% sudoku(S), cuadrante(S,0,P).
% sudoku(S), fila(S, 2, Fila).
% Mostrar el Sudoku en formato 9x9
mostrar_sudoku([]) :- nl.
mostrar_sudoku(Sudoku) :-
    mostrar_filas(Sudoku, 1).

mostrar_filas([], _).
mostrar_filas(Sudoku, Fila) :-
    length(FilaActual, 9), % Tomar 9 elementos
    append(FilaActual, Resto, Sudoku),
    write(FilaActual), nl,
    SiguienteFila is Fila + 1,
    mostrar_filas(Resto, SiguienteFila).

% DEVOLVER FILA DE SUDOKU
fila([A, B, C, D, E, F, G, H, I |_], 0, [A, B, C, D, E, F, G, H , I]).
fila([_, _, _, _, _, _, _, _, _ | Cola], Pos, Fila) :-
    P is Pos - 1,
    fila(Cola, P, Fila).

% DEVOLVER COLUMNA DE SUDOKU
columna(Matriz, Pos, Columna) :-
    columna_aux(Matriz, Pos, 9, [], Columna).
columna_aux(_, _, 0, Acumulador, Columna) :-
    reverse(Acumulador, Columna).
columna_aux(Matriz, Indice, Restantes, Acumulador, Columna) :-
    nth0(Indice, Matriz, Elemento),
    I is Indice + 9,
    R is Restantes - 1,
    columna_aux(Matriz, I, R, [Elemento|Acumulador], Columna).

% UNIR POSIBILIDADES
eliminar_repetidos([], []).
eliminar_repetidos([H|T], R) :-
    member(H, T), % Si H está en el resto de la lista, lo ignoramos
    eliminar_repetidos(T, R).
eliminar_repetidos([H|T], [H|R]) :-
    \+ member(H, T), % Si H no está en el resto de la lista, lo mantenemos
    eliminar_repetidos(T, R).

unir(X,Y,L) :-
    append(X,Y,ZR),
    eliminar_repetidos(ZR,Z),
    sort(Z,L).

cuadrante(Sudoku, NumCuadrante, Elementos) :-
    % Obtener fila y columna base
    FilaBase is (NumCuadrante // 3) * 3,
    ColBase is (NumCuadrante mod 3) * 3,
    
    % Calcular índice base
    Base is (FilaBase * 9) + ColBase,
    
    % Calcular todos los índices necesarios
    I1 is Base,      I2 is Base + 1,     I3 is Base + 2,
    I4 is Base + 9,  I5 is Base + 10,    I6 is Base + 11,
    I7 is Base + 18, I8 is Base + 19,    I9 is Base + 20,
    
    % Extraer elementos usando índices calculados
    nth0(I1, Sudoku, E1),    nth0(I2, Sudoku, E2),     nth0(I3, Sudoku, E3),
    nth0(I4, Sudoku, E4),    nth0(I5, Sudoku, E5),     nth0(I6, Sudoku, E6),
    nth0(I7, Sudoku, E7),    nth0(I8, Sudoku, E8),     nth0(I9, Sudoku, E9),
    
    Elementos = [E1, E2, E3, E4, E5, E6, E7, E8, E9].
