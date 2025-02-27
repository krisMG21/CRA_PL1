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

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 1. Eliminación sobre filas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Separa la lista plana de 81 celdas en filas (cada fila con 9 celdas).
split_filas([], []).
split_filas(P, [Row|Rows]) :-
    length(Row, 9),
    append(Row, Rest, P),
    split_filas(Rest, Rows).

% Vuelve a aplanar la lista de filas en una lista simple.
aplanar_filas([], []).
aplanar_filas([Row|Rows], Flat) :-
    aplanar_filas(Rows, FlatRest),
    append(Row, FlatRest, Flat).

% Procesa cada fila aplicando la eliminación de pares desnudos.
tripletas_filas(P, NewP) :-
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
tripletas_columnas(P, NewP) :-
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
tripletas_cuadrantes(P, NewP) :-
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

procesar_listas([], []).                     %FUNCIONA
procesar_listas([Group|Groups], [NewGroup|NewGroups]) :-
    ( Group \= '.' ->
        encontrar_parejas(Group, Triplet),
        eliminar_instancias(Group, Triplet, NewGroup)
    ),
    procesar_listas(Groups, NewGroups).

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
    count_occurrences(Triplet, Group, 3).

count_occurrences(Triplet, Group, Count) :-    %FUNCIONA
    include(=(Triplet), Group, Matching),
    length(Matching, Count).

% Versión mejorada de eliminar_instancias/3
eliminar_instancias([], _, []).
eliminar_instancias([X|Rest], Triplet, [NewX|NewRest]) :-  %FUNCIONA
    (X \= Triplet, is_list(X) 
     -> subtract(X, Triplet, NewX) 
     ;  NewX = X),
    eliminar_instancias(Rest, Triplet, NewRest).