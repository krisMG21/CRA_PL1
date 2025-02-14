:- consult("regla0.pl").
:- consult("regla1.pl").
:- consult("regla2.pl").
:- consult("regla3.pl").

% Representación de un Sudoku
sudoku([
    '.','.', 9 ,   6 ,'.','.',  '.', 1 ,'.',
     8 ,'.','.',  '.','.', 1 ,  '.', 9 ,'.',
     7 ,'.','.',  '.','.','.',  '.','.', 8 ,

    '.', 3 ,'.',  '.', 6 ,'.',  '.','.','.',
    '.', 4 ,'.',   1 ,'.', 9 ,  '.','.', 5 ,
     9 ,'.','.',  '.','.','.',  '.','.','.',

    '.', 8 ,'.',   9 ,'.','.',   5 , 4 ,'.',
     6 ,'.','.',   7 , 1 ,'.',  '.','.', 3 ,
    '.','.', 5 ,  '.', 8 , 4 ,  '.','.', 9
]).
% REGLAS DE EJECUCIÓN.
% ?- sudoku(S), cuadrante(S,0,P).
% ?- sudoku(S), fila(S, 2, Fila).

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
    Pos > 0,
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
    eliminar_repetidos(T, R).

unir(X,Y,L) :-
    append(X,Y,ZR),
    eliminar_repetidos(ZR,Z),
    sort(Z,L).


/*presentes(S, Presentes):-
    length(S, 81),
    presentes_aux(S, 0, [], Presentes).

presentes_aux(_, 81, Acumulador, Presentes):-
    reverse(Acumulador, Presentes).
presentes_aux(S, Cont, Acumulador, Presentes) :-
    Cont < 81,
    fila(S, Cont // 9, F),
    columna(S, Cont mod 9, C),
    cuadrante(S, (Cont // 27) * 3 + ((Cont mod 9) // 3), Q),
    unir(F, C, FC), 
    unir(FC, Q, P),
    I is Cont + 1,
    presentes_aux(S, I, [P|Acumulador], Presentes).
*/

% NUMEROS PRESENTES QUE AFECTAN A CADA CASILLA
presentes(S, Presentes):-
    length(S, 81),
    presentes_aux(S, 0, [], Presentes).

presentes_aux(_, 81, Acumulador, Presentes):-
    reverse(Acumulador, Presentes).
presentes_aux(S, Cont, Acumulador, Presentes) :-
    Cont < 81,
    FilaIndex is Cont // 9,
    ColIndex is Cont mod 9,
    CuadIndex is (Cont // 27) * 3 + ((Cont mod 9) // 3),

    fila(S, FilaIndex, F),
    columna(S, ColIndex, C),
    cuadrante(S, CuadIndex, Q),

    unir(F,C,FC), unir(FC, Q, P),

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
main :-
    sudoku(S),
    write("Sudoku inicial:"), nl,
    mostrar_sudoku(S),
    posibles(S, P),
    resolver(S, P, FinalS),
    write("Sudoku resuelto (total o parcialmente):"), nl,
    mostrar_sudoku(FinalS).

resolver(S, P, FinalS) :-
    (aplicar_reglas(S, P, NewS, NewP) ->
        mostrar_sudoku(NewS),
        resolver(NewS, NewP, FinalS)
    ;
        FinalS = S  % No se aplicó ninguna regla, devolvemos el Sudoku actual
    ).

aplicar_reglas(S, P, NewS, NewP) :-
    (regla0(S, P, TempS), S \= TempS ->
        NewS = TempS,
        posibles(NewS, NewP),
        write("Regla 0 aplicada"), nl
    ;
    %regla 1, recursión si cambia el sudoku, cambia Sudoku
        (regla1(S, P, TempS), S \= TempS -> 
            NewS = TempS,
            posibles(NewS, NewP),
            write("Regla 1 aplicada"), nl
        ;
        %regla 2, recursión si cambia el sudoku, cambia Posibilidades
            (regla2(S, P, TempP), P \= TempP ->
                NewP = TempP,
                write("Regla 2 aplicada"), nl
            ;    
            %regla 3, recursión si cambia el sudoku, cambia Posibilidades
                (regla3(S, P, TempP), P \= TempP ->
                    NewP = TempP,
                    write("Regla 3 aplicada"), nl
                ;
                    false  % Si ninguna regla se aplicó, retornamos false               
                )                
            )
        )
    ).

% Definiciones de regla0, regla1, etc.


    /*
    S = News,
    regla1(S, P, NewS),
    (S \= NewS ->
        write("Regla 1"), nl,
        mostrar_sudoku(NewS),
        resolver(NewS, FinalS)        
        )
    */

    /*
    regla2()
    */
