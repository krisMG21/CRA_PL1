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

aplanar_filas([], []).
aplanar_filas([Row|Rows], Flat) :-  % FUNCIONA
    aplanar_filas(Rows, FlatRest),
    append(Row, FlatRest, Flat).

parejas_filas(P, NewP) :-       
    split_filas(P, Rows),
    procesar_listas(Rows, NewRows),
    aplanar_filas(NewRows, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 2. Eliminación sobre columnas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

transponer(Plano, Transpuesto) :-       % FUNCIONA
    split_filas(Plano, Matriz),
    transponer_matriz(Matriz, MatrizT),
    aplanar_filas(MatrizT, Transpuesto).

transponer_matriz([], []).              % FUNCIONA
transponer_matriz([[]|_], []).
transponer_matriz(Matriz, [Col|Cols]) :-
    maplist(descomponer_fila, Matriz, Col, RestMatrix),
    transponer_matriz(RestMatrix, Cols).

descomponer_fila([X|Xs], X, Xs).        % FUNCIONA
descomponer_fila('.', '.', []).

parejas_columnas(P, NewP) :-
    transponer(P, TP),
    split_filas(TP, Columns),
    procesar_listas(Columns, NewColumns),   % BUG
    aplanar_filas(NewColumns, NewTP),
    transponer(NewTP, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 3. Eliminación sobre cuadrantes
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

split_cuadrantes([], []).
split_cuadrantes([R1,R2,R3|Rest], [Q1,Q2,Q3|QuadsRest]) :-   % FUNCIONA
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

% The rest of the code (aplanar_cuadrantes, split_cuad_to_filas, etc.) remains unchanged.
aplanar_cuadrantes([], []).
aplanar_cuadrantes([Q1,Q2,Q3|Rest], [R1,R2,R3|Rows]) :- % FUNCIONA
    split_cuad_to_filas(Q1, R1a, R2a, R3a),
    split_cuad_to_filas(Q2, R1b, R2b, R3b),
    split_cuad_to_filas(Q3, R1c, R2c, R3c),
    append(R1a, R1b, R1ab), append(R1ab, R1c, R1),
    append(R2a, R2b, R2ab), append(R2ab, R2c, R2),
    append(R3a, R3b, R3ab), append(R3ab, R3c, R3),
    aplanar_cuadrantes(Rest, Rows).

split_cuad_to_filas([], [], [], []).    % FUNCIONA
split_cuad_to_filas([A,B,C,D,E,F,G,H,I|Rest], [A,B,C|R1], [D,E,F|R2], [G,H,I|R3]) :-
    split_cuad_to_filas(Rest, R1, R2, R3).

parejas_cuadrantes(P, NewP) :-
    split_filas(P, Rows),
    split_cuadrantes(Rows, Quads),
    procesar_listas(Quads, NewQuads),   % BUG
    aplanar_cuadrantes(NewQuads, NewRows),
    aplanar_filas(NewRows, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Procesamiento de grupos (filas/columnas/cuadrantes)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% procesar_listas([], []).
% procesar_listas([Group|Groups], [NewGroup|NewGroups]) :-
%     (Group = ['.','.','.','.','.','.','.','.','.'] ->
%         NewGroup = Group
%     ;
%         encontrar_parejas(Group, Pair),
%         (Pair = [] ->
%             NewGroup = Group
%         ;
%             eliminar_instancias(Group, Pair, NewGroup)
%         )
%     ),
%     procesar_listas(Groups, NewGroups).

% encontrar_parejas(Group, Pair) :-       % FUNCIONA
%     find_possible_pairs(Group, Pairs),
%     maplist(sort, Pairs, SortedPairs),
%     select_valid_pair(SortedPairs, Group, SortedPair),
%     Pair = SortedPair.

% find_possible_pairs(Group, Pairs) :-    % FUNCIONA
%     findall(
%         X,
%         (member(X, Group),
%          is_list(X),
%          length(X, 2)),
%         Pairs
%     ).

% select_valid_pair(Pairs, Group, Pair) :-    % FUNCIONA
%     member(SP, Pairs),
%     count_occurrences(SP, Group, 2),
%     Pair = SP.

count_occurrences(SortedPair, Group, Count) :-
    count_occurrences_helper(Group, SortedPair, 0, Count).

count_occurrences_helper([], _, Count, Count).
count_occurrences_helper([X|Rest], SortedPair, Acc, Count) :-
    (is_list(X), length(X, 2), sort(X, SX), SX == SortedPair ->
        NewAcc is Acc + 1
    ;
        NewAcc = Acc
    ),
    count_occurrences_helper(Rest, SortedPair, NewAcc, Count).

% eliminar_instancias([], _, []).
% eliminar_instancias([X|Rest], Pair, [NewX|NewRest]) :-
%     (is_list(X) ->
%         (length(X, 2) ->
%             sort(X, SortedX),
%             (SortedX == Pair ->
%                 NewX = X
%             ;
%                 subtract(X, Pair, NewX)
%             )
%         ;
%             subtract(X, Pair, NewX)
%         )
%     ;
%         NewX = X
%     ),
%     eliminar_instancias(Rest, Pair, NewRest).

procesar_listas([], []).
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
encontrar_todos_los_pares(Group, UniquePairs) :-
    findall(
        SP,
        (member(X, Group),
         is_list(X),
         length(X, 2),
         sort(X, SP),
         count_occurrences(SP, Group, 2)
    ), Pairs),
    list_to_set(Pairs, UniquePairs).  % Elimina duplicados

% Elimina los elementos de todos los pares encontrados en las celdas no pertenecientes a pares
eliminar_elementos_de_pares(Group, Pairs, NewGroup) :-
    % Recoge todos los elementos de los pares
    findall(E, (member(P, Pairs), member(E, P)), Elements),
    list_to_set(Elements, RemoveSet),  % Elimina duplicados
    maplist(eliminar_si_no_es_par(Pairs, RemoveSet), Group, NewGroup).

% Predicado auxiliar para eliminar elementos si la celda no es un par válido
eliminar_si_no_es_par(Pairs, RemoveSet, X, NewX) :-
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

% Resto del código (count_occurrences, split_filas, etc.) se mantiene igual.