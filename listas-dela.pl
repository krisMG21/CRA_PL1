eliminar_repetidos([],[]). %Caso base
eliminar_repetidos([X|Y],L) :-
    member(X,Y),
    eliminar_repetidos(Y,L).

eliminar_repetidos([X|Y], [X|T]) :-
    \+ member(X, Y), % Si H no está en el resto de la lista, lo mantenemos
    eliminar_repetidos(Y, T).

unir_lista(X,Y,L) :-
    append(X,Y,Z),
    sort(Z,L).

