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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 1. Eliminación sobre filas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

split_filas([], []).
split_filas(P, [Row|Rows]) :-       % FUNCIONA
    length(Row, 9),
    append(Row, Rest, P),
    split_filas(Rest, Rows).

parejas_filas(P, NewP) :-       
    split_filas(P, Rows),
    procesar_listas(Rows, NewRows),
    split_filas(NewP, NewRows).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 2. Eliminación sobre columnas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

transponer(Plano, Transpuesto) :-       % FUNCIONA
    split_filas(Plano, Matriz),
    transponer_matriz(Matriz, MatrizT),
    split_filas(Transpuesto, MatrizT).

transponer_matriz([], []).              % FUNCIONA
transponer_matriz([[]|_], []).
transponer_matriz(Matriz, [Col|Cols]) :-
    maplist(descomponer_fila, Matriz, Col, RestMatrix),
    transponer_matriz(RestMatrix, Cols).

descomponer_fila([X|Xs], X, Xs).        % FUNCIONA
descomponer_fila('.', '.', []).

parejas_columnas(P, NewP) :-    % FUNCIONA
    transponer(P, TP),
    parejas_filas(TP, NewTP),
    transponer(NewTP, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 3. Eliminación sobre cuadrantes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

split_cuadrantes([], []).    % FUNCIONA
split_cuadrantes([R1,R2,R3|Rest], [Q1,Q2,Q3|QuadsRest]) :- 
    split_3_filas(R1, R2, R3, Q1, Q2, Q3),
    split_cuadrantes(Rest, QuadsRest).

split_3_filas(R1, R2, R3, Q1, Q2, Q3) :-    % FUNCIONA
    split_row(R1, R1_Q1, R1_Q2, R1_Q3),
    split_row(R2, R2_Q1, R2_Q2, R2_Q3),
    split_row(R3, R3_Q1, R3_Q2, R3_Q3),
    append(R1_Q1, R2_Q1, Temp1),
    append(Temp1, R3_Q1, Q1),
    append(R1_Q2, R2_Q2, Temp2),
    append(Temp2, R3_Q2, Q2),
    append(R1_Q3, R2_Q3, Temp3),
    append(Temp3, R3_Q3, Q3).

split_row(Row, Q1, Q2, Q3) :-   % FUNCIONA
    length(Q1, 3),
    length(Q2, 3),
    length(Q3, 3),
    append(Q1, Q2, Temp),
    append(Temp, Q3, Row).

split_cuad_to_filas([], [], [], []).    % FUNCIONA
split_cuad_to_filas([A,B,C,D,E,F,G,H,I|Rest], [A,B,C|R1], [D,E,F|R2], [G,H,I|R3]) :-
    split_cuad_to_filas(Rest, R1, R2, R3).

parejas_cuadrantes(P, NewP) :-  % FUNCIONA
    split_filas(P, Rows),
    split_cuadrantes(Rows, Quads),
    procesar_listas(Quads, NewQuads),
    split_cuadrantes(NewRows, NewQuads),
    split_filas(NewP, NewRows).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Procesamiento de grupos (filas/columnas/cuadrantes)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

procesar_listas([], []).    % FUNCIONA
procesar_listas([Group|Groups], [NewGroup|NewGroups]) :-
    (Group = ['.','.','.','.','.','.','.','.','.'] ->
        NewGroup = Group
    ;
        encontrar_todos_los_pares(Group, Pairs),
        (Pairs = [] ->
            NewGroup = Group
        ;
            eliminar_elementos_de_pares(Group, Pairs, NewGroup)
        )
    ),
    procesar_listas(Groups, NewGroups).

% Encuentra todos los pares desnudos únicos en el grupo
encontrar_todos_los_pares(Group, UniquePairs) :-    % FUNCIONA
    findall(
        SP,
        (member(X, Group),
         is_list(X),
         length(X, 2),
         sort(X, SP),
         count_occurrences(SP, Group, 2)
    ), Pairs),
    eliminar_repetidos(Pairs, UniquePairs).  % Elimina duplicados

% Elimina los elementos de todos los pares encontrados en las celdas no pertenecientes a pares
eliminar_elementos_de_pares(Group, Pairs, NewGroup) :-  % FUNCIONA
    % Recoge todos los elementos de los pares
    findall(E, (member(P, Pairs), member(E, P)), Elements),
    eliminar_repetidos(Elements, RemoveSet),
    maplist(eliminar_si_no_es_par(Pairs, RemoveSet), Group, NewGroup).

% Predicado auxiliar para eliminar elementos si la celda no es un par válido
eliminar_si_no_es_par(Pairs, RemoveSet, X, NewX) :-     % FUNCIONA
    (is_list(X) ->
        (length(X, 2) ->
            sort(X, SortedX),
            (member(SortedX, Pairs) ->
                NewX = X  % Mantiene el par intacto
            ;
                subtract(X, RemoveSet, NewX))  % Elimina elementos del par
        ;
            subtract(X, RemoveSet, NewX)  % Celdas con >2 elementos
        )
    ;
        NewX = X  % Celdas resueltas (no listas)
    ).


count_occurrences(SortedPair, Group, Count) :-  % FUNCIONA
    count_occurrences_helper(Group, SortedPair, 0, Count).

count_occurrences_helper([], _, Count, Count).  % FUNCIONA
count_occurrences_helper([X|Rest], SortedPair, Acc, Count) :-   
    (is_list(X), length(X, 2), sort(X, SX), SX == SortedPair ->
        NewAcc is Acc + 1
    ;
        NewAcc = Acc
    ),
    count_occurrences_helper(Rest, SortedPair, NewAcc, Count).