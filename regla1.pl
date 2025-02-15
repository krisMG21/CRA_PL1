/*

Regla 1: Si un número aparece en una única celda dentro de una fila, columna o cuadrante, se coloca allí
Esta regla se aplica a nivel de grupo (fila, columna o cuadrante). Un número es único dentro de un grupo de celdas vacías, así que debe ir en esa celda.
Ejemplo en una fila: P = [[1,4,5], [1,4,5], 3, [4,6], 2, [4,6], 7, [8], [1,8]]. -> Aquí, el número 8 solo aparece en una de las celdas como [8]. Por lo tanto, esa celda debe ser 8.

La Regla 1 usa los posibles valores (P) calculados en main, pero no directamente para hacer una decisión individual en cada celda.
En cambio, revisa P en toda una fila, columna o cuadrante para encontrar valores únicos en un grupo.
Si encuentra un número que solo aparece en una celda de un grupo, lo coloca en S.

get_fila/2, get_columna/2 y get_cuadrante/2 solo se usan directamente en la Regla 1.
En posibles/2, se usan indirectamente dentro de presentes/2 para encontrar los números ocupados.
La diferencia clave es que en posibles/2 solo descartamos números ocupados, mientras que en la Regla 1 buscamos números únicos en grupos.

*/

regla1(S, P, NewS) :-
    obtener_indices_celdas_vacias(S, Vacias),  % Obtener índices de celdas vacías
    aplicar_regla1_celdas(Vacias, S, P, TempS),
    (TempS \= S -> NewS = TempS ; NewS = S).  % Solo actualiza si hubo cambios

% Obtener índices de celdas vacías (donde S tiene '.')
obtener_indices_celdas_vacias(S, Vacias) :-
    findall(I, (nth0(I, S, '.'), between(0, 80, I)), Vacias).

% Aplicar regla1 a cada celda vacía
aplicar_regla1_celdas([], S, _, S).
aplicar_regla1_celdas([I|Resto], S, P, NewS) :-
    nth0(I, P, Posibles),  % Posibles valores de la celda I
    (Posibles \= '.',  % Si la celda está vacía y tiene posibles
     encontrar_numero_unico(I, P, Numero) ->  % Buscar número único
        replace(I, S, Numero, TempS),  % Asignar número a la celda
        aplicar_regla1_celdas(Resto, TempS, P, NewS)
    ;
        aplicar_regla1_celdas(Resto, S, P, NewS)
    ).

% Buscar número único en fila, columna o cuadrante
encontrar_numero_unico(Indice, P, Numero) :-
    get_fila(Indice, FilaIndices),  % Índices de la fila
    get_columna(Indice, ColumnaIndices),  % Índices de la columna
    get_cuadrante(Indice, CuadranteIndices),  % Índices del cuadrante
    
    nth0(Indice, P, MisPosibles),  % Posibles de la celda actual
    
    % Buscar único en FILA
    (buscar_en_grupo(MisPosibles, FilaIndices, P, Numero) -> true ;
    % Buscar único en COLUMNA
    (buscar_en_grupo(MisPosibles, ColumnaIndices, P, Numero) -> true ;
    % Buscar único en CUADRANTE
    buscar_en_grupo(MisPosibles, CuadranteIndices, P, Numero))).

% Verifica si un número aparece solo una vez en un grupo (fila/columna/cuadrante)
buscar_en_grupo(MisPosibles, GrupoIndices, P, Numero) :-
    member(N, MisPosibles),
    list_posibles_grupo(GrupoIndices, P, ListasGrupo),
    count_ocurrencias(N, ListasGrupo, 1),
    Numero = N.

% Obtener todas las listas de posibles de un grupo
list_posibles_grupo(Indices, P, Listas) :-
    findall(Lista, (member(I, Indices), nth0(I, P, Lista)), Listas).

% Contar ocurrencias de N en listas de posibles (excluyendo la celda actual)
count_ocurrencias(N, Listas, Count) :-
    include(contains(N), Listas, Filtered),
    length(Filtered, Count).

contains(N, Lista) :- member(N, Lista).

% Helpers para obtener índices de fila/columna/cuadrante
% Helpers para obtener índices de fila/columna/cuadrante
get_fila(Indice, FilaIndices) :-
    Fila is Indice // 9,
    Start is Fila * 9,
    End is Start + 8,
    numlist(Start, End, FilaIndices).

get_columna(Indice, ColumnaIndices) :-
    Columna is Indice mod 9,
    findall(I, (between(0, 8, F), I is F*9 + Columna), ColumnaIndices).

get_cuadrante(Indice, CuadranteIndices) :-
    FilaStart is (Indice // 27) * 3,
    ColStart is ((Indice mod 9) // 3) * 3,
    findall(I, 
        (between(0, 2, DF), 
        between(0, 2, DC),
        I is (FilaStart + DF)*9 + (ColStart + DC)), 
        CuadranteIndices).
% Reemplazar elemento en lista
replace(Index, List, Elem, NewList) :-
    nth0(Index, List, _, Temp),
    nth0(Index, NewList, Elem, Temp).
