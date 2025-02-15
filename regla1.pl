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
    aplicar_regla1_celdas(Vacias, S, P, NewS).

% Obtener índices de celdas vacías (donde S tiene '.')
obtener_indices_celdas_vacias(S, Vacias) :-
    findall(I, (nth0(I, S, '.'), I < 81), Vacias).

% Aplicar regla1 a cada celda vacía
aplicar_regla1_celdas([], S, _, S).
aplicar_regla1_celdas([I|Resto], S, P, NewS) :-
    % Si en la celda I hay posibles, encontrar uno unico en F C y Q
    (nth0(I, P, Posibles), Posibles \= '.', encontrar_numero_unico(I, P, Numero) ->
        replace(I, S, Numero, TempS)
    ;
        TempS = S
    ),
    aplicar_regla1_celdas(Resto, TempS, P, NewS).


encontrar_numero_unico(Indice, P, Numero) :-
    % Obtiene los posibles de la celda actual y busca un numero que solo sea posible una
    % vez en una F / C / Q
    nth0(Indice, P, MisPosibles),
    (get_fila(Indice, FilaIndices),buscar_en_grupo(MisPosibles, FilaIndices, P, Numero);
     get_columna(Indice, ColumnaIndices), buscar_en_grupo(MisPosibles, ColumnaIndices, P, Numero);
     get_cuadrante(Indice, CuadranteIndices), buscar_en_grupo(MisPosibles, CuadranteIndices, P, Numero)).

% Verifica si un número aparece solo una vez en un grupo (fila/columna/cuadrante)
buscar_en_grupo(MisPosibles, GrupoIndices, P, Numero) :-
    member(N, MisPosibles),
    findall(Lista, (member(I, GrupoIndices), nth0(I, P, Lista), Lista \= '.', member(N, Lista)), [_]),
    Numero = N.

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
