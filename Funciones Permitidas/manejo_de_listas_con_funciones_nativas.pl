% Resumen
% 1. member/2 (Nativo)
% 2. append/3 (Nativo)
% 3. nth0/3 (Nativo)
% 4. last/2 (Nativo)
% 5. length/2 (Nativo)
% 6. reverse/2 (Nativo)
% 7. permutation/2 (Nativo)
% 8. sum_list/2 (Nativo)
% 9. max_list/2 (Nativo)


% Tutorial de predicados nativos en Prolog
% 1. member/2 (Nativo)
% Este predicado verifica si un elemento pertenece a una lista.
% Ejemplo de uso:
% ?- member(3, [1, 2, 3, 4]).
% true.
% ?- member(5, [1, 2, 3, 4]).
% false.

% 2. append/3 (Nativo)
% Este predicado concatena dos listas.
% Ejemplo de uso:
% ?- append([1, 2], [3, 4], Result).
% Result = [1, 2, 3, 4].

% 3. nth0/3 (Nativo)
% Este predicado obtiene el elemento en un índice específico de la lista (los índices empiezan en 0).
% Ejemplo de uso:
% ?- nth0(2, [a, b, c, d], Element).
% Element = c.
% ?- nth0(0, [a, b, c, d], Element).
% Element = a.

% 4. last/2 (Nativo)
% Este predicado obtiene el último elemento de una lista.
% Ejemplo de uso:
% ?- last([a, b, c, d], Element).
% Element = d.
% ?- last([1, 2, 3], Element).
% Element = 3.

% 5. length/2 (Nativo)
% Este predicado calcula la longitud de una lista.
% Ejemplo de uso:
% ?- length([a, b, c, d], Length).
% Length = 4.
% ?- length([], Length).
% Length = 0.

% 6. reverse/2 (Nativo)
% Este predicado invierte el orden de los elementos en una lista.
% Ejemplo de uso:
% ?- reverse([1, 2, 3, 4], Reversed).
% Reversed = [4, 3, 2, 1].
% ?- reverse([a, b, c], Reversed).
% Reversed = [c, b, a].

% 7. permutation/2 (Nativo)
% Este predicado genera una permutación de una lista.
% Ejemplo de uso:
% ?- permutation([1, 2, 3], Perm).
% Perm = [1, 2, 3] ;
% Perm = [1, 3, 2] ;
% Perm = [2, 1, 3] ;
% Perm = [2, 3, 1] ;
% Perm = [3, 1, 2] ;
% Perm = [3, 2, 1] ;
% false.

% 8. sum_list/2 (Nativo)
% Este predicado calcula la suma de los elementos de una lista numérica.
% Ejemplo de uso:
% ?- sum_list([1, 2, 3, 4], Sum).
% Sum = 10.
% ?- sum_list([0, 5, 10], Sum).
% Sum = 15.

% 9. max_list/2 (Nativo)
% Este predicado encuentra el valor máximo en una lista.
% Ejemplo de uso:
% ?- max_list([1, 2, 3, 4], Max).
% Max = 4.
% ?- max_list([7, 3, 5, 8], Max).
% Max = 8.
