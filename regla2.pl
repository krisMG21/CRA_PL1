regla2(P, NewP):-
    % TODO: Si, en posibilidades, dos numeros aparecen ellos solos( 7,9 | 7,9)
    % los borramos de las posibilidades del resto de la fila/columna/cuadrante

    
    % Iterar sobre filas
        % Coger lista de primera casilla
        % Avanzar, comprobando si ocurre una vez más y solo una vez
        % - Lo encuentra, devolverlo
        % - No lo encuentra, probar sobre siguiente casillas

    % Iterar sobre columnas
        % Anterior proceso aplicado a columna
    % Iterar sobre cuadrantes
        % Anterior proceso aplicado a cuadrante

    false.