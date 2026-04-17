from lector import leer_datos
import gurobipy as gp
import numpy as np


model = gp.Model()
x = []
n_plantas = 10
n_substation = 10
n_usuarios = 10

for i in range(n_substation):
    
    model.addVars(n_plantas, vtype=gp.GRB.CONTINUOUS, name=f"x{i}")

for i in range(n_usuarios):

    model.addVars(n_plantas, vtype=gp.GRB.CONTINUOUS, name=f"x{i}")

