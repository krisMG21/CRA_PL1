% LONGITUD BASIC
longitud(0, []).
longitud(Longitud, [_|Cola]) :- longitud(L,Cola), Longitud is L+1.

% LONGITUD ACUMULADOR
longitud_acu(Longitud, Acumulador, [_|Cola]) :- A is Acumulador+1, longitud_acu(Longitud, A, Cola).
longitud_acu(Longitud, Longitud, []).
longitud2(Longitud, Lista) :- longitud_acu(Longitud, 0, Lista).

% MAXIMO
max_acu(Maximo, Acumulador, [Cabeza|Cola]) :-
    (Cabeza < Acumulador ->
        max_acu(Maximo, Acumulador, Cola)
    ;
        max_acu(Maximo, Cabeza, Cola)
    ).

max_acu(Acumulador, Acumulador, []).
max(Maximo, [Cabeza|Cola]) :- max_acu(Maximo, Cabeza, [Cabeza|Cola]).

% MINIMO
min_acu(Minimo, Acumulador, [Cabeza|Cola]) :-
    (Cabeza > Acumulador ->
        min_acu(Minimo, Acumulador, Cola)
    ;
        min_acu(Minimo, Cabeza, Cola)
    ).

min_acu(Acumulador, Acumulador, []).
min(Minimo, [Cabeza|Cola]) :- min_acu(Minimo, Cabeza, [Cabeza|Cola]).

% MIEMBRO
miembro(X, [X|_]).
miembro(X, [_|Cola]) :- miembro(X, Cola).

% CHECK LISTAS EJEMPLOS
igual([], []).
igual([X|Cola1], [X|Cola2]) :- igual(Cola1, Cola2).

% CONCATENA
concatena([], L, L).
concatena([Cabeza|Cola], L2, [Cabeza|L3]) :- concatena(Cola, L2, L3).

% Existe: append(L1, L2, Res)

% encuentra prefijos
prefijo(Prefijo, L) :- concatena(Prefijo, _, L).

% encuentra sufijos
sufijo(Sufijo, L) :- concatena(_, Sufijo, L).

% SUBLISTA: prefijo de un sufijo de una lista
sublista(SubL, L) :- sufijo(Sufijo, L), prefijo(SubL, Sufijo).

% INVIERTE NAIVE
invierte_n([], []).
invierte_n([Cabeza|Cola], Inv) :- invierte_n(Cola, ColaI), concatena(ColaI, [Cabeza], Inv).

% INVIERTE
invierte([], Acumulador, Acumulador).
invierte([Cabeza|Cola], Acumulador, LInv) :- invierte(Cola, [Cabeza|Acumulador], LInv).

% GET POS SIMPLE
get([Cabeza|_], 0, Cabeza).
get([_|Cola], Pos, Valor) :- P is Pos - 1, get(Cola, P, Valor).

% GET POS + ENUM
enum(Lista) :- enum(Lista, 0).

enum([], _).
enum([Cabeza|Cola], Indice) :-
    write(Indice),  write(' - '), write(Cabeza), write('\n'),
    Next is Indice + 1,
    enum(Cola, Next).