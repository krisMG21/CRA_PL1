regla0(S, P, NewS) :-
    aux0(S, P, 0, [], NewS).

aux0(_, _, 81, Acc, NewS) :-
    reverse(Acc, NewS).
aux0([HS|ColaS], [HP|ColaP], Cont, Acc, NewS):-
    Cont < 81,
    (HP = '.' ->
        S = HS
    ; is_list(HP) ->
        (length(HP, 1) ->
            [S] = HP
        ;
            S = HS
        )
    ; 
        S = HP
    ),
    C is Cont + 1,
    aux0(ColaS, ColaP, C, [S|Acc], NewS).
