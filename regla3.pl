% REGLA3: Elimina de P (posibilidades) los candidatos de tripletas desnudas en filas, columnas y cuadrantes.
regla3(P, NewP) :-
    (tripletas_filas(P, P1), P \= P1 ->
        write("regla3: Cambios aplicados en una fila"), nl,
        NewP = P1
    ;
        tripletas_columnas(P, P2), P \= P2 ->
            write("regla3: Cambios aplicados en una columna"), nl,
            NewP = P2
    ;
        tripletas_cuadrantes(P, P3), P \= P3 ->
            write("regla3: Cambios aplicados en un cuadrante"), nl,
            NewP = P3
    ;
        write("regla3: No ha aplicado cambios"), nl,
        NewP = P
    ).

    % tripletas_filas(P, P1),
    % tripletas_columnas(P1, P2),
    % tripletas_cuadrantes(P2, NewP).

% Procesa cada fila aplicando la eliminación de pares desnudos.
tripletas_filas(P, NewP) :-
    split_filas(P, Rows),
    procesar_listas_3(Rows, NewRows),
    split_filas(NewP, NewRows).

% Aplica la eliminación en columnas: se transpone,
% se procesa como filas y se transpone de vuelta.
tripletas_columnas(P, NewP) :-
    transponer(P, TP),
    split_filas(TP, Columns),
    procesar_listas_3(Columns, NewColumns),
    split_filas(NewTP, NewColumns),
    transponer(NewTP, NewP).

% Aplica la eliminación en cuadrantes
tripletas_cuadrantes(P, NewP) :-
    split_filas(P, Rows),
    split_cuadrantes(Rows, Quads),
    procesar_listas_3(Quads, NewQuads),
    split_cuadrantes(NewRows, NewQuads),
    split_filas(NewP, NewRows).

procesar_listas_3([], []).
procesar_listas_3([Group|Groups], [NewGroup|NewGroups]) :-
    (Group = ['.','.','.','.','.','.','.','.','.'] ->
        NewGroup = Group
    ;
        encontrar_todas_las_tripletas(Group, Triplets),
        (Triplets = [] ->
            NewGroup = Group
        ;
            eliminar_elementos_de_tripletas(Group, Triplets, NewGroup)
        )
    ),
    procesar_listas_3(Groups, NewGroups).

% Encuentra todas las tripletas desnudas únicas en el grupo
encontrar_todas_las_tripletas(Group, UniqueTriplets) :-
    findall(
        ST,
        (member(X, Group),
         is_list(X),
         length(X, 3),
         sort(X, ST),
         count_occurrences_3(ST, Group, 3)
    ), Triplets),
    list_to_set(Triplets, UniqueTriplets).  % Elimina duplicados

% Elimina los elementos de las tripletas válidas en celdas no pertenecientes a tripletas
eliminar_elementos_de_tripletas(Group, Triplets, NewGroup) :-
    findall(E, (member(T, Triplets), member(E, T)), Elements),
    list_to_set(Elements, RemoveSet),
    maplist(eliminar_si_no_es_tripleta(Triplets, RemoveSet), Group, NewGroup).

% Predicado auxiliar para eliminar elementos
eliminar_si_no_es_tripleta(Triplets, RemoveSet, X, NewX) :-
    (is_list(X) ->
        (length(X, 3) ->
            sort(X, SortedX),
            (member(SortedX, Triplets) ->
                NewX = X  % Mantiene la tripleta
            ;
                subtract(X, RemoveSet, NewX)  % Elimina elementos
            )
        ;
            subtract(X, RemoveSet, NewX)  % Celdas con >3 elementos
        )
    ;
        NewX = X  % Celdas resueltas
    ).

% Cuenta ocurrencias de una tripleta ordenada
count_occurrences_3(SortedTriplet, Group, Count) :-
    count_occurrences_helper_3(Group, SortedTriplet, 0, Count).

count_occurrences_helper_3([], _, Count, Count).
count_occurrences_helper_3([X|Rest], SortedTriplet, Acc, Count) :-
    (is_list(X), length(X, 3), sort(X, SX), SX == SortedTriplet ->
        NewAcc is Acc + 1
    ;
        NewAcc = Acc
    ),
    count_occurrences_helper_3(Rest, SortedTriplet, NewAcc, Count).