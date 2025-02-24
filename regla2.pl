% REGLA2: Elimina de P (posibilidades) los candidatos de pares desnudos en filas, columnas y cuadrantes.
regla2(P, NewP) :-
    parejas_filas(P, P1),
    parejas_columnas(P1, P2),
    parejas_cuadrantes(P2, NewP).

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
parejas_filas(P, NewP) :-
    split_filas(P, Rows),
    procesar_lista(Rows, NewRows),
    aplanar_filas(NewRows, NewP).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% 2. Eliminación sobre columnas
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Transpone una matriz (lista de listas).
transponer([], []).
transponer([[]|_], []).
transponer(Matrix, [Row|Rows]) :-
    extraer_primera_col(Matrix, Row, RestMatrix),
    transponer(RestMatrix, Rows).

extraer_primera_col([], [], []).
extraer_primera_col([[H|T]|Rows], [H|Hs], [T|Ts]) :-
    extraer_primera_col(Rows, Hs, Ts).

% Aplica la eliminación en columnas: se transpone,
% se procesa como filas y se transpone de vuelta.
parejas_columnas(P, NewP) :-
    split_filas(P, Rows),
    transponer(Rows, Columns),
    procesar_lista(Columns, NewColumns),
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
    procesar_lista(Quads, NewQuads),
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

procesar_lista([], []).
procesar_lista([Group|Groups], [NewGroup|NewGroups]) :-
    encontrar_parejas(Group, Pair),
    (Pair = [] -> NewGroup = Group ; eliminar_instancias(Group, Pair, NewGroup)),
    procesar_lista(Groups, NewGroups).

encontrar_parejas([X,Y|Rest], Pair) :-
    (X = [A,B], Y = [A,B] -> Pair = [A,B] ; encontrar_parejas([Y|Rest], Pair)).
encontrar_parejas([_], []).
encontrar_parejas([], []).

eliminar_instancias([], _, []).
eliminar_instancias([[A,B]|Rest], [A,B], [[A,B]|NewRest]) :-
    eliminar_instancias(Rest, [A,B], NewRest).
eliminar_instancias([X|Rest], Pair, [NewX|NewRest]) :-
    X \= Pair,
    eliminar_de_lista(X, Pair, NewX),
    eliminar_instancias(Rest, Pair, NewRest).

eliminar_de_lista([], _, []).
eliminar_de_lista([X|Xs], Pair, NewXs) :-
    (member(X, Pair) -> eliminar_de_lista(Xs, Pair, NewXs) ; NewXs = [X|Rest], eliminar_de_lista(Xs, Pair, Rest)).
