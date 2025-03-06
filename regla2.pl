% REGLA2: Elimina de P (posibilidades) los candidatos de pares desnudos en filas, columnas y cuadrantes.
regla2(P, NewP) :-
    (parejas_filas(P, P1), P \= P1 ->
        write("regla2: Cambios aplicados en una fila"), nl,
        NewP = P1
    ;
        parejas_columnas(P, P2), P \= P2 ->
            write("regla2: Cambios aplicados en una columna"), nl,
            NewP = P2
    ;
        parejas_cuadrantes(P, P3), P \= P3 ->
            write("regla2: Cambios aplicados en un cuadrante"), nl,
            NewP = P3
    ;
        write("regla2: No ha aplicado cambios"), nl,
        NewP = P
    ).

    % parejas_filas(P, P1),
    % parejas_columnas(P1, P2),
    % parejas_cuadrantes(P2, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 1. Eliminación sobre filas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Separa la lista plana de 81 celdas en filas (cada fila con 9 celdas).
split_filas([], []).            % FUNCIONA
split_filas(P, [Row|Rows]) :-
    length(Row, 9),
    append(Row, Rest, P),
    split_filas(Rest, Rows).

% Vuelve a aplanar la lista de filas en una lista simple.
aplanar_filas([], []).          % FUNCIONA
aplanar_filas([Row|Rows], Flat) :-
    aplanar_filas(Rows, FlatRest),
    append(Row, FlatRest, Flat).

% Procesa cada fila aplicando la eliminación de pares desnudos.
parejas_filas(P, NewP) :-       
    split_filas(P, Rows),
    procesar_listas(Rows, NewRows),
    aplanar_filas(NewRows, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 2. Eliminación sobre columnas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Transpone una matriz (lista de listas).
transponer(Plano, Transpuesto) :-
    dividir_en_filas(Plano, Matriz),
    transponer_matriz(Matriz, MatrizT),
    aplanar_matriz(MatrizT, Transpuesto).

dividir_en_filas([], []).
dividir_en_filas(Lista, [Fila|Resto]) :-
    length(Fila, 9),
    append(Fila, RestoDeLista, Lista),
    dividir_en_filas(RestoDeLista, Resto).

transponer_matriz([], []).
transponer_matriz([[]|_], []).
transponer_matriz(Matriz, [Col|Cols]) :-
    maplist(descomponer_fila, Matriz, Col, RestMatrix),
    transponer_matriz(RestMatrix, Cols).

descomponer_fila([X|Xs], X, Xs).
descomponer_fila('.', '.', []).

aplanar_matriz([], []).
aplanar_matriz([Fila|Filas], Plano) :-
    append(Fila, RestoPlano, Plano),
    aplanar_matriz(Filas, RestoPlano).


% Aplica la eliminación en columnas: se transpone,
% se procesa como filas y se transpone de vuelta.
parejas_columnas(P, NewP) :-
    split_filas(P, Rows),
    transponer(Rows, Columns),
    procesar_listas(Columns, NewColumns),
    transponer(NewColumns, NewRows),
    aplanar_filas(NewRows, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 3. Eliminación sobre cuadrantes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Separa las filas en cuadrantes (cada cuadrante son 9 celdas).
split_cuadrantes([], []).
split_cuadrantes([R1,R2,R3|Rest], Quads) :-
    split_3_filas(R1, R2, R3, Q1, Q2, Q3),
    append([Q1,Q2,Q3], QuadsRest, Quads),
    split_cuadrantes(Rest, QuadsRest).

split_3_filas([], [], [], [], [], []).
split_3_filas([A,B,C|R1], [D,E,F|R2], [G,H,I|R3], [A,B,C,D,E,F,G,H,I|Q1], Q2, Q3) :-
    split_3_filas(R1, R2, R3, Q1, Q2, Q3).

% Aplica la eliminación en cuadrantes
parejas_cuadrantes(P, NewP) :-
    split_filas(P, Rows),
    split_cuadrantes(Rows, Quads),
    procesar_listas(Quads, NewQuads),
    aplanar_cuadrantes(NewQuads, NewRows),
    aplanar_filas(NewRows, NewP).

aplanar_cuadrantes([], []).
aplanar_cuadrantes([Q1,Q2,Q3|Rest], [R1,R2,R3|Rows]) :-
    split_cuad_to_filas(Q1, R1a, R2a, R3a),
    split_cuad_to_filas(Q2, R1b, R2b, R3b),
    split_cuad_to_filas(Q3, R1c, R2c, R3c),
    append(R1a, R1b, R1ab), append(R1ab, R1c, R1),
    append(R2a, R2b, R2ab), append(R2ab, R2c, R2),
    append(R3a, R3b, R3ab), append(R3ab, R3c, R3),
    aplanar_cuadrantes(Rest, Rows).

split_cuad_to_filas([], [], [], []).
split_cuad_to_filas([A,B,C,D,E,F,G,H,I|Rest], [A,B,C|R1], [D,E,F|R2], [G,H,I|R3]) :-
    split_cuad_to_filas(Rest, R1, R2, R3).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Procesamiento de grupos (filas/columnas/cuadrantes)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

procesar_listas([], []).
procesar_listas([Group|Groups], [NewGroup|NewGroups]) :-
    (Group = ['.','.','.','.','.','.','.','.','.'] ->
        NewGroup = Group  % Mantener grupo sin cambios si está vacío
    ;
        encontrar_parejas(Group, Pair),
        (Pair = [] ->
            NewGroup = Group  % Mantener grupo sin cambios si no se encuentra pareja
        ;
            eliminar_instancias(Group, Pair, NewGroup)
        )
    ),
    procesar_listas(Groups, NewGroups).


encontrar_parejas(Group, Pair) :-           %FUNCIONA
    find_possible_pairs(Group, Pairs),
    select_valid_pair(Pairs, Group, Pair).

find_possible_pairs(Group, Pairs) :-
    findall(
        X,
        (member(X, Group),
         is_list(X),
         length(X, 2)),
        Pairs
    ).

select_valid_pair(Pairs, Group, Pair) :-    %FUNCIONA
    member(Pair, Pairs),
    count_occurrences(Pair, Group, 2).

count_occurrences(Pair, Group, Count) :-    %FUNCIONA
    include(=(Pair), Group, Matching),
    length(Matching, Count).

% Versión mejorada de eliminar_instancias/3
eliminar_instancias([], _, []).
eliminar_instancias([X|Rest], Pair, [NewX|NewRest]) :-  %FUNCIONA
    (X \= Pair, is_list(X) 
     -> subtract(X, Pair, NewX) 
    ;  NewX = X),
    eliminar_instancias(Rest, Pair, NewRest).