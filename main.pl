/**
CONTENIDO
Este archivo Prolog contiene todo lo que respecta a:

* Consultas de filas, columnas y cuadrantes sobre el sudoku
* Lectura de numeros presentes en las filas, columnas y cuadrantes adyacentes a una
celda
* Cálculo de numeros posibles en una casilla vacía en base a los presentes
* Uso de reglas para resolver un sudoku dado (reglas importadas dede reglai.pl)

MODO DE USO
Para elegir comodamente el sudoku a resolver, lo asignaremos desde consola y lo introduciremos
al main tal que:

?- sudoku_x(S), main(S).

*/


% IMPORT REGLAS
:- consult("sudokus.pl").
:- consult("regla0.pl").
:- consult("regla1.pl").
:- consult("regla2.pl").
:- consult("regla3.pl").

% REGLAS DE EJECUCIÓN.
% ?- sudoku(S), cuadrante(S,0,P).
% ?- sudoku(S), fila(S, 2, Fila).

% Mostrar el Sudoku en formato 9x9
mostrar_sudoku(Sudoku) :-
    mostrar_filas(Sudoku, 1).

% Caso base: lista vacía
mostrar_filas([], _).

% Mostrar filas con formato
mostrar_filas(Sudoku, FilaNum) :-
    % Extraer primera fila (9 elementos)
    append(Fila, Resto, Sudoku),
    length(Fila, 9),
    
    % Mostrar fila actual con formato
    write(' '),
    mostrar_fila(Fila),
    
    % Imprimir separador horizontal cada 3 filas
    (FilaNum mod 3 =:= 0, FilaNum < 9 -> 
        write('-------+-------+-------'), nl
    ; true),
    
    % Procesar siguiente fila
    Siguiente is FilaNum + 1,
    mostrar_filas(Resto, Siguiente).

% Mostrar una fila dividida en 3 grupos de 3 elementos
mostrar_fila(Fila) :-
    append(G1, Resto1, Fila), length(G1, 3),
    append(G2, G3, Resto1), length(G2, 3),
    mostrar_grupo(G1), write('|'),
    mostrar_grupo(G2), write('|'),
    mostrar_grupo(G3), nl.

% Mostrar grupo de 3 elementos con espacios
mostrar_grupo([A,B,C]) :-
    format(' ~w ~w ~w ', [A,B,C]).

% DEVOLVER FILA DE SUDOKU
fila([A, B, C, D, E, F, G, H, I |_], 0, [A, B, C, D, E, F, G, H , I]).
fila([_, _, _, _, _, _, _, _, _ | Cola], Pos, Fila) :-
    Pos > 0,
    P is Pos - 1,
    fila(Cola, P, Fila).

% Por si os mola mas
/*
fila(Sudoku, Pos, Fila) :-
    length(Fila, 9),
    Offset is Pos * 9,
    append(Prefijo, Resto, Sudoku),
    length(Prefijo, Offset),
    append(Fila, _, Resto).
*/

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

% DEVOLVER CUADRANTE DE SUDOKU
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
    nth0(I1, Sudoku, E1),    nth0(I2, Sudoku, E2),    nth0(I3, Sudoku, E3),
    nth0(I4, Sudoku, E4),    nth0(I5, Sudoku, E5),    nth0(I6, Sudoku, E6),
    nth0(I7, Sudoku, E7),    nth0(I8, Sudoku, E8),    nth0(I9, Sudoku, E9),
    
    Elementos = [E1, E2, E3, E4, E5, E6, E7, E8, E9].

% UNIR NUMEROS SIN REPETIR
eliminar_repetidos([], []).
eliminar_repetidos([H|T], R) :-
    member(H, T), % Si H está en el resto de la lista, lo ignoramos
    eliminar_repetidos(T, R).    
eliminar_repetidos([H|T], [H|R]) :-
    \+ member(H, T), % Si H no está en el resto de la lista, lo mantenemos
    eliminar_repetidos(T, R).

unir(X,Y,L) :-
    append(X,Y,ZR),
    eliminar_repetidos(ZR,Z),
    sort(Z,L).

% NUMEROS PRESENTES QUE AFECTAN A CADA CASILLA
presentes(S, Presentes):-
    length(S, 81),
    presentes_aux(S, 0, [], Presentes).

presentes_aux(_, 81, Acumulador, Presentes):-
    reverse(Acumulador, Presentes), 
    !.
presentes_aux(S, Cont, Acumulador, Presentes) :-
    Cont < 81,
    FilaIndex is Cont // 9,
    ColIndex is Cont mod 9,
    CuadIndex is (Cont // 27) * 3 + ((Cont mod 9) // 3),

    fila(S, FilaIndex, F),
    columna(S, ColIndex, C),
    cuadrante(S, CuadIndex, Q),
    unir(F,C,FC), unir(FC, Q, P),

    !,

    I is Cont + 1,
    presentes_aux(S, I, [P|Acumulador], Presentes).

% NUMEROS POSIBLES POR CASILLA
posibles(S, Posibles) :-
    presentes(S, Presentes),
    maplist(posibles_aux, S, Presentes, Posibles).

posibles_aux(Casilla, Presentes, Posibles) :-
    (Casilla \= '.' ->
        Posibles = '.'
    ;
        findall(N, (between(1,9,N), \+ member(N, Presentes)), Posibles)
    ).


% MAIN EXECUTIONS
% TEST REGLA 0
main(S) :-
    write("Sudoku inicial:"), nl,
    mostrar_sudoku(S),
    posibles(S, P),
    %mostrar_sudoku(P),     % mostrar posibilidades
    resolver(S, P, FinalS),
    (member('.', FinalS) ->
        write("Sudoku resuelto parcialmente:"), nl

    ;
        write("Sudoku resuelto totalmente:"), nl
    ),
    mostrar_sudoku(FinalS).

resolver(S, P, FinalS) :-
    (aplicar_reglas(S, P, NewS, NewP), % Aplica todas las reglas en 1 iteración
     (S \= NewS ; P \= NewP) % ¿Hubo cambios?
    ->
        mostrar_sudoku(NewS),
        resolver(NewS, NewP, FinalS) % Nueva iteración
    ;
        FinalS = S % Fin: no hay cambios
    ).

aplicar_reglas(S, P, NewS, NewP) :-
    % Paso 1: Aplicar Regla 0 (celdas obvias)
    (regla0(S, P, TempS), S \= TempS ->
        write('REGLA 0 APLICADA!'), nl,
        posibles(TempS, TempP), % Recalcular posibilidades
        NewS = TempS,
        NewP = TempP
    ;
        % Paso 2: Si no hubo cambios en S, aplicar Regla 1
        (regla1(P, TempP1), P \= TempP1 ->
            write('REGLA 1 APLICADA!'), nl,
            NewS = S,
            NewP = TempP1
        ;
            mostrar_sudoku(P),
            % Paso 3: Si no hubo cambios en P, aplicar Regla 2
            (regla2(P, TempP2), P \= TempP2 ->
                write('REGLA 2 APLICADA!'), nl,
                NewS = S,
                NewP = TempP2
            ;
                % Paso 4: Si no hubo cambios, aplicar Regla 3
                (regla3(P, TempP3), P \= TempP3 ->
                    write('REGLA 3 APLICADA!'), nl,
                    NewS = S,
                    NewP = TempP3
                ;
                    % Ninguna regla aplicó cambios
                    write('NINGUNA REGLA APLICADA!'), nl,
                    NewS = S,
                    NewP = P
                )
            )
        )
    ).

test_regla2() :-
    p_regla2(P),
    regla2(P, P1),
    regla2(P1, P2),
    regla2(P2, P3),
    mostrar_sudoku(P3).

test_regla3() :-
    p_regla3(P),
    regla3(P, P1),
    regla3(P1, P2),
    regla3(P2, P3),
    mostrar_sudoku(P3).