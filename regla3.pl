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
    aplanar_filas(NewRows, NewP).

% Aplica la eliminación en columnas: se transpone,
% se procesa como filas y se transpone de vuelta.
tripletas_columnas(P, NewP) :-
    split_filas(P, Rows),
    transponer(Rows, Columns),
    procesar_listas_3(Columns, NewColumns),
    transponer(NewColumns, NewRows),
    aplanar_filas(NewRows, NewP).

% Aplica la eliminación en cuadrantes
tripletas_cuadrantes(P, NewP) :-
    split_filas(P, Rows),
    split_cuadrantes(Rows, Quads),
    procesar_listas_3(Quads, NewQuads),
    aplanar_cuadrantes(NewQuads, NewRows),
    aplanar_filas(NewRows, NewP).


encontrar_tripletas(Group, Triplet) :-           %FUNCIONA
    find_possible_triplets(Group, Triplets),
    select_valid_triplet(Triplets, Group, Triplet).

find_possible_triplets(Group, Triplets) :-        %FUNCIONA
    findall(
        [A,B,C], 
        (member(X, Group), 
         is_list(X), 
         length(X, 3), 
         X = [A,B,C]), 
        Triplets
    ).

select_valid_triplet(Triplets, Group, Triplet) :-    %FUNCIONA
    member(Triplet, Triplets),
    count_occurrences_3(Triplet, Group, 3).

count_occurrences_3(Triplet, Group, Count) :-    %FUNCIONA
    include(=(Triplet), Group, Matching),
    length(Matching, Count).

% Versión mejorada de eliminar_instancias/3
eliminar_instancias_3([], _, []).
eliminar_instancias_3([X|Rest], Triplet, [NewX|NewRest]) :-  %FUNCIONA
    (X \= Triplet, is_list(X) 
     -> subtract(X, Triplet, NewX) 
     ;  NewX = X),
    eliminar_instancias_3(Rest, Triplet, NewRest).

procesar_listas_3([], []).                    %FUNCIONA
procesar_listas_3([['.','.','.','.','.','.','.','.','.']|Groups],[NewGroup|NewGroups]) :-
    procesar_listas_3(Groups,NewGroups),
    NewGroup = ['.','.','.','.','.','.','.','.','.'].
procesar_listas_3([Group|_], [NewGroup|_]) :-
    encontrar_tripletas(Group,Triplet),
    eliminar_instancias_3(Group,Triplet,NewGroup).
    