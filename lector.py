def leer_datos(filename):
    """
    Lee una instancia del problema de planificación energética desde un archivo de texto.

    Parámetros
    ----------
    filename : str
        Ruta al archivo de datos.

    Retorna
    -------
    Una tupla con los siguientes elementos, en orden:

    Conjuntos
    ---------
    P : list[int]
        Lista de índices de todas las plantas generadoras.
    P_R : list[int]
        Lista de índices de las plantas de energía renovable.
    S : list[int]
        Lista de índices de todas las subestaciones.
    S_R : list[int]
        Lista de índices de las subestaciones exclusivamente renovables.
    S_M : list[int]
        Lista de índices de las subestaciones mixtas (S_M = S \\ S_R).
    C : list[int]
        Lista de índices de todos los clientes (usuarios finales).

    Parámetros de clientes
    ----------------------
    d : dict[int, float]
        d[u] es la demanda total de energía (MWh) del cliente u.
    d_r : dict[int, float]
        d_r[u] es la demanda mínima de energía renovable (MWh) del cliente u.
        Se garantiza d_r[u] <= d[u] para todo u en C.

    Parámetros de plantas
    ---------------------
    c_p : dict[int, float]
        c_p[p] es el costo de generación por MWh en la planta p.
    e_min : dict[int, float]
        e_min[p] es la cantidad mínima de MWh que debe generar la planta p.
    e_max : dict[int, float]
        e_max[p] es la cantidad máxima de MWh que puede generar la planta p.

    Parámetros de subestaciones
    ---------------------------
    o_min : dict[int, float]
        o_min[s] es el nivel mínimo de operación (MWh recibidos) de la subestación s.
    o_max : dict[int, float]
        o_max[s] es la capacidad máxima de distribución (MWh) de la subestación s.
    LR : dict[int, float]
        LR[s] es el límite de energía renovable (MWh) que puede procesar la subestación s.
        Solo es relevante para subestaciones mixtas (s in S_M); para s in S_R su valor
        coincide con o_max[s].

    Parámetros de costo
    -------------------
    t_ps : dict[tuple[int,int], float]
        t_ps[(p, s)] es el costo de transmisión por MWh enviado de la planta p
        a la subestación s.
    q_sc : dict[tuple[int,int], float]
        q_sc[(s, u)] es el costo de distribución por MWh enviado de la subestación s
        al cliente u.

    Ejemplo de uso
    --------------
    >>> P, P_R, S, S_R, S_M, C, d, d_r, c_p, e_min, e_max, o_min, o_max, LR, t_ps, q_sc = leer_datos()
    >>> print(f"Plantas: {len(P)}, Clientes: {len(C)}")
    """
    P, P_R, S, S_R, S_M, C = [], [], [], [], [], []

    d, d_r = {}, {}
    c_p, e_min, e_max = {}, {}, {}
    o_min, o_max, LR = {}, {}, {}
    t_ps, q_sc = {}, {}

    with open(filename) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue

            parts = line.strip().split()
            key = parts[0]

            if key == "P":
                P = eval(" ".join(parts[1:]))
            elif key == "P_R":
                P_R = list(eval(" ".join(parts[1:])))
            elif key == "S":
                S = eval(" ".join(parts[1:]))
            elif key == "S_R":
                S_R = list(eval(" ".join(parts[1:])))
            elif key == "S_M":
                S_M = list(eval(" ".join(parts[1:])))
            elif key == "C":
                C = eval(" ".join(parts[1:]))

            elif key == "d":
                d[int(parts[1])] = float(parts[2])
            elif key == "d_r":
                d_r[int(parts[1])] = float(parts[2])

            elif key == "c_p":
                c_p[int(parts[1])] = float(parts[2])
            elif key == "e_min":
                e_min[int(parts[1])] = float(parts[2])
            elif key == "e_max":
                e_max[int(parts[1])] = float(parts[2])

            elif key == "o_min":
                o_min[int(parts[1])] = float(parts[2])
            elif key == "o_max":
                o_max[int(parts[1])] = float(parts[2])
            elif key == "LR":
                LR[int(parts[1])] = float(parts[2])

            elif key == "t_ps":
                t_ps[(int(parts[1]), int(parts[2]))] = float(parts[3])
            elif key == "q_sc":
                q_sc[(int(parts[1]), int(parts[2]))] = float(parts[3])

    return P, P_R, S, S_R, S_M, C, d, d_r, c_p, e_min, e_max, o_min, o_max, LR, t_ps, q_sc
