% Regla 1: Si un número aparece solo en una lista de posibilidades de una unidad (fila, columna, bloque), fijarlo allí y eliminarlo de las demás.
regla1(P, NewP) :-
    %write("Estado inicial: "), write(P), nl,
    process_all_units(P, NewP),
    %write("Estado despues de aplicar Regla 1: "), write(NewP), nl,
    NewP \= P.

% Procesar todas las unidades (filas, columnas, bloques)
process_all_units(P, NewP) :-
    process_rows(P, TempP1),
    process_columns(TempP1, TempP2),
    process_blocks(TempP2, NewP).

% Procesar todas las filas
process_rows(P, NewP) :-
    %write("Procesando filas..."), nl,
    findall(RowIndices, row_indices(RowIndices), Rows),
    foldl(process_unit, Rows, P, NewP).

% Procesar todas las columnas
process_columns(P, NewP) :-
    %write("Procesando columnas..."), nl,
    findall(ColIndices, column_indices(ColIndices), Cols),
    foldl(process_unit, Cols, P, NewP).

% Procesar todos los bloques
process_blocks(P, NewP) :-
    %write("Procesando bloques..."), nl,
    findall(BlockIndices, block_indices(BlockIndices), Blocks),
    foldl(process_unit, Blocks, P, NewP).

row_indices(RowIndices) :-
    between(0, 8, Row),
    Start is Row * 9,
    End is Start + 8,
    numlist(Start, End, RowIndices).

% Obtener índices de una columna (0-8)
column_indices(ColIndices) :-
    between(0, 8, Col),
    findall(Index, (between(0,8,Row), Index is Col + Row*9), ColIndices).

% Obtener índices de un bloque (0-8)
block_indices(BlockIndices) :-
    between(0, 2, BR),
    between(0, 2, BC),
    StartRow is BR * 3,
    StartCol is BC * 3,
    findall(Index,
        (between(0, 2, DR), between(0, 2, DC),
        Row is StartRow + DR,
        Col is StartCol + DC,
        Index is Row * 9 + Col),
    BlockIndices).

% Procesar una unidad (fila, columna o bloque)
process_unit(UnitIndices, P, NewP) :-
    %write("Procesando unidad: "), write(UnitIndices), nl,
    collect_numbers_in_unit(UnitIndices, P, Numbers),
    %write("Numeros en la unidad: "), write(Numbers), nl,
    find_unique_numbers(Numbers, UniqueNumbers),
    %write("Numeros unicos en la unidad: "), write(UniqueNumbers), nl,
    apply_unique_changes(UniqueNumbers, UnitIndices, P, NewP).

% Recolectar todos los números de las posibilidades en la unidad (excluyendo celdas fijadas)
collect_numbers_in_unit(UnitIndices, P, Numbers) :-
    maplist(get_possible_numbers(P), UnitIndices, NestedNumbers),
    flatten(NestedNumbers, Numbers).

% Solo incluir números de celdas con múltiples posibilidades
get_possible_numbers(P, Index, Nums) :-
    nth0(Index, P, Poss),
    (is_list(Poss), length(Poss, L), L > 1 -> Nums = Poss ; Nums = []).

% Encontrar números que aparecen exactamente una vez
find_unique_numbers(Numbers, Unique) :-
    findall(X, (member(X, Numbers), count_member(X, Numbers, 1)), Unsorted),
    sort(Unsorted, Unique).

% Contar ocurrencias de un elemento en una lista
count_member(Element, List, Count) :-
    include(=(Element), List, Filtered),
    length(Filtered, Count).

% Aplicar cambios para los números únicos
apply_unique_changes([], _, P, P).
    %write('No hay mas numeros unicos por procesar'), nl.
apply_unique_changes([N|Ns], UnitIndices, P, NewP) :-
    %nl, write('=== Procesando numero unico: '), write(N), nl,
    %write('Estado actual de P: '), write(P), nl,
    (find_cell_with_number(N, UnitIndices, P, Cell)
    ->  (
            % write('Encontrado '), write(N), 
            % write(' en celda '), write(Cell), nl,
            % % write('Posibilidades originales en celda '), write(Cell), 
            % write(': '), nth0(Cell, P, Orig), write(Orig), nl,
            
            % Aplicar cambio en celda principal
            replace_possibility(Cell, [N], P, TempP),
            
            % write('Estado despues de fijar '), write(N), 
            % write(' en celda '), write(Cell), write(': '), 
            % write(TempP), nl,
            
            % Procesar siguientes números
            apply_unique_changes(Ns, UnitIndices, TempP, NewP)
        )
    ;   (
            % write('Numero '), write(N), 
            % write(' no encontrado en la unidad'), nl,
            apply_unique_changes(Ns, UnitIndices, P, NewP)
        )
    ).

% Encontrar la celda en la unidad que contiene el número N (solo en celdas no fijadas)
find_cell_with_number(N, UnitIndices, P, Cell) :-
    % write('Buscando '), write(N), write(' en unidad...'), nl,
    member(Cell, UnitIndices),
    nth0(Cell, P, Poss),
    is_list(Poss),
    length(Poss, L), L > 1,  % Asegurar que la celda no está fijada
    member(N, Poss).

replace_possibility(Index, NewVal, Old, New) :-
    % nl, write('>>> Reemplazando posibilidades en celda '), write(Index), nl,
    % write('Valor nuevo: '), write(NewVal), nl,
    replace_at_index(Index, NewVal, Old, TempP),
    (NewVal = [N] ->
        % write('Eliminando '), write(N), 
        % write(' de unidades relacionadas...'), nl,
        get_related_indices(Index, RelatedIndices),
        % write('Indices relacionados: '), write(RelatedIndices), nl,
        foldl(remove_number_from_cell(N), RelatedIndices, TempP, New)
        % write('Estado final despues de eliminaciones: '), write(New), nl
    ;   New = TempP
    ).

remove_number_from_cell(N, CellIndex, P, NewP) :-
    nth0(CellIndex, P, Poss),
    (is_list(Poss) ->
        (member(N, Poss) ->
            delete(Poss, N, NewPoss),
            replace_at_index(CellIndex, NewPoss, P, TempP),
            NewP = TempP
        ; NewP = P
        )
    ; NewP = P
    ).

replace_at_index(0, NewVal, [_|Tail], [NewVal|Tail]).
replace_at_index(Index, NewVal, [Head|Tail], [Head|NewTail]) :-
    Index > 0,
    NextIndex is Index - 1,
    replace_at_index(NextIndex, NewVal, Tail, NewTail).

get_related_indices(Index, RelatedIndices) :-
    Row is Index // 9,
    Col is Index mod 9,
    StartRow is Row * 9,
    EndRow is StartRow + 8,
    numlist(StartRow, EndRow, RowIndices),
    findall(ColIndex, (between(0,8,R), ColIndex is Col + R*9), ColIndices),
    BlockRow is Row // 3,
    BlockCol is Col // 3,
    StartBlockRow is BlockRow * 3,
    StartBlockCol is BlockCol * 3,
    findall(BlockIndex,
        (between(0,2,DR), between(0,2,DC),
        RBlock is StartBlockRow + DR,
        CBlock is StartBlockCol + DC,
        BlockIndex is RBlock*9 + CBlock),
        BlockIndices),
    append([RowIndices, ColIndices, BlockIndices], AllIndices),
    sort(AllIndices, UniqueIndices),
    delete(UniqueIndices, Index, RelatedIndices).
