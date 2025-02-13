eliminar_repetidos([],[]). %Caso base

eliminar_repetidos([H|T],L) :-

    % H = primer elemento, T = el resto de elementos
    % L = variable donde se guarda la lista

    member(H,T),                    % Si H (head) no esta en el resto de la lista
                                    % T (Tail), lo mantenemos
    eliminar_repetidos(T,L).        % Analiza el resto de elementos buscando duplicados

eliminar_repetidos([H|T], [H|L]) :-

    % H = primer elemento, T = el resto de elementos
    % L = resto de la lista guardada

    \+ member(H, T),                % Si H (head) no esta en el resto de la lista
                                    % T (Tail), lo mantenemos
    eliminar_repetidos(T, L).       % Analiza el resto de elementos buscando duplicados

unir_lista(X,Y,L) :-

    % Esta funcion une dos listas X e Y, eliminando repetidos y ordenando la lista final L

    append(X,Y,Z),                  % Une las dos listas y las guarda en una variable intermedia
    sort(Z,L).                      % Ordena el resutlado y lo guarda en L

