from lector import leer_datos
import gurobipy as gp
import sys

path = sys.argv[1]
P, P_R, S, S_R, S_M, C, d, d_r, c_p, e_min, e_max, o_min, o_max, LR, t_ps, q_sc = leer_datos(path)

model = gp.Model()

# Por default addVars pone un lower_bound = 0
# Variables
x = {}
# Flujo de O a P
x["O"] = model.addVars([f"p_{i}" for i in P], vtype=gp.GRB.CONTINUOUS, name="O -> P")

# Flujo de P a S
for i in P:
    if i in P_R:
        x[f"p_{i}"] = model.addVars([f"s_{j}r" for j in S], name=f"p_{i} -> S")
    else:
        x[f"p_{i}"] = model.addVars([f"s_{j}c" for j in S_M], name=f"p_{i} -> Sc")

# Flujo de S a S auxiliar
for i in S:
    x[f"s_{i}r"] = model.addVars([f"s_{i}ra"], name=f"s_{i}r -> s_{i}ra")
    if i in S_M:
        x[f"s_{i}c"] = model.addVars([f"s_{i}ca"], name=f"s_{i}c -> s_{i}ca")

# Flujo de S auxiliar a U
for i in S:
    x[f"s_{i}ra"] = model.addVars([f"u_{j}r" for j in C], name=f"s_{i}ra -> Ur")
    if i in S_M:
        x[f"s_{i}ca"] = model.addVars([f"u_{j}" for j in C],  name=f"s_{i}ca -> U")

# Flujo de U renovable a U
for i in C:
    x[f"u_{i}r"] = model.addVars([f"u_{i}"], name=f"u_{i}r -> u_{i}")


# Función objetivo
funcion_1 = (x[f"p_{i}"][f"s_{j}r"] * (c_p[i] + t_ps[(i, j)]) for j in S for i in P if i in P_R)
funcion_2 = (x[f"p_{i}"][f"s_{j}c"] * (c_p[i] + t_ps[(i, j)]) for j in S_M for i in P if i not in P_R)
funcion_3 = (x[f"s_{i}ra"][f"u_{j}r"] * q_sc[(i, j)] for j in C for i in S)
funcion_4 = (x[f"s_{i}ca"][f"u_{j}"] * q_sc[(i, j)] for j in C for i in S_M)
funcion_completa = gp.quicksum(funcion_1) + gp.quicksum(funcion_2) + gp.quicksum(funcion_3) + gp.quicksum(funcion_4)
model.setObjective(funcion_completa, gp.GRB.MINIMIZE)


# Igualdades de flujos.
model.addConstrs((x["O"][f"p_{i}"] - ( gp.quicksum(x[f"p_{i}"][f"s_{j}c"] for j in S_M if i not in P_R) + gp.quicksum(x[f"p_{i}"][f"s_{j}r"] for j in S if i in P_R) ) == 0 for i in P))

model.addConstrs((gp.quicksum(x[f"p_{j}"][f"s_{i}c"] for j in P if j not in P_R) - x[f"s_{i}c"][f"s_{i}ca"] == 0 for i in S_M))

model.addConstrs((gp.quicksum(x[f"p_{j}"][f"s_{i}r"] for j in P_R) - x[f"s_{i}r"][f"s_{i}ra"] == 0 for i in S))

model.addConstrs((x[f"s_{i}c"][f"s_{i}ca"] - gp.quicksum(x[f"s_{i}ca"][f"u_{j}"] for j in C) == 0 for i in S_M))

model.addConstrs((x[f"s_{i}r"][f"s_{i}ra"] - gp.quicksum(x[f"s_{i}ra"][f"u_{j}r"] for j in C) == 0 for i in S))

model.addConstrs((gp.quicksum(x[f"s_{i}ra"][f"u_{j}r"] for i in S) - x[f"u_{j}r"][f"u_{j}"] == 0 for j in C))

model.addConstrs((x[f"u_{i}r"][f"u_{i}"] + gp.quicksum(x[f"s_{j}ca"][f"u_{i}"] for j in S_M) == d[i] for i in C))

# Restricciones de carga por cada flujo.


for i in P:
    x["O"][f"p_{i}"].lb = e_min[i]
    x["O"][f"p_{i}"].ub = e_max[i]

for i in S_M:
    x[f"s_{i}r"][f"s_{i}ra"].ub = LR[i]
    x[f"s_{i}c"][f"s_{i}ca"].ub = o_max[i]

for i in S_R:
    x[f"s_{i}r"][f"s_{i}ra"].lb = o_min[i]
    x[f"s_{i}r"][f"s_{i}ra"].ub = o_max[i]

for i in C:
    x[f"u_{i}r"][f"u_{i}"].lb = d_r[i]

model.addConstrs((x[f"s_{i}r"][f"s_{i}ra"] + x[f"s_{i}c"][f"s_{i}ca"] <= o_max[i] for i in S_M))
model.addConstrs((x[f"s_{i}r"][f"s_{i}ra"] + x[f"s_{i}c"][f"s_{i}ca"] >= o_min[i] for i in S_M))

model.Params.Method = 0
model.Params.NetworkAlg = 1

model.optimize()
