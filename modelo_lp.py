from lector import leer_datos
import gurobipy as gp
import sys

path = sys.argv[1]
P, P_R, S, S_R, S_M, C, d, d_r, c_p, e_min, e_max, o_min, o_max, LR, t_ps, q_sc = leer_datos(path)

model = gp.Model()
x = {}
y = {}
n_plantas = 10
n_substation = 10
n_usuarios = 10

# Por default addVars pone un lower_bound = 0
for i in P:

    columna = model.addVars(S, vtype=gp.GRB.CONTINUOUS, name=f"x{i}")
    x[i] = columna

for i in S:

    columna = model.addVars(C, vtype=gp.GRB.CONTINUOUS, name=f"y{i}")
    y[i] = columna

# Anular ciertas variables
for s in S_R:
    for p in P:
        if p not in P_R:
            x[p][s].UB = 0

# Función objetivo
funcion_1 = (x[p][s] * (c_p[p] + t_ps[(p, s)]) for s in S for p in P)
funcion_2 = (y[s][u] * q_sc[(s, u)] for u in C for s in S)
model.setObjective(gp.quicksum(funcion_1) + gp.quicksum(funcion_2), gp.GRB.MINIMIZE)

# e_min y e_max de cada planta
model.addConstrs((gp.quicksum(x[p][s] for s in S) == [e_min[p], e_max[p]] for p in P), "e_max y e_min")

# O_min y O_max de cada subestación
model.addConstrs((gp.quicksum(x[p][s] for p in P) == [o_min[s], o_max[s]] for s in S), "o_max y o_min")


# Energía renovable máxima de cada subestación mixta
model.addConstrs((gp.quicksum(x[p][s] for p in P_R) <= LR[s] for s in S_M), "max_mixtos")

# Demanda normal de cada usuario
model.addConstrs((d[u] == gp.quicksum(y[s][u] for s in S) for u in C), "demanda_n")

# Demanda renovable de cada usuario
model.addConstrs((d_r[u] <= gp.quicksum(y[s][u] for s in S_R) for u in C), "demanda_n")

# Balance de masa
model.addConstrs((gp.quicksum(x[p][s] for p in P) == gp.quicksum(y[s][u] for u in C) for s in S), "Balance_xy")

model.optimize()
