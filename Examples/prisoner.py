#prisonner example (Halpern 2015)

from main import *

def compute_A(param):
    return param['Aexo']

def compute_B(param):
    return param['Bexo']

def compute_C(param):
    return param['Cexo']

def compute_D(param):
    return (param['A'] and param['B']) or param['C']


# Exogenous variables
U = {'Aexo':[False, True], \
    'Bexo':[False, True],\
    'Cexo':[False, True]}

# Endogenous variables
V = {'A':[False, True], \
    'B':[False, True], \
    'C':[False, True], \
    'D':[False, True]}

# Parent node for each endogenous variable
P = {'A':(['Aexo'],compute_A), \
    'B':(['Bexo'],compute_B), \
    'C':(['Cexo'],compute_C),\
    'D':(['A','B','C'],compute_D)}

C =  {'Aexo':['A'], \
    'Bexo':['B'], \
    'Cexo':['C'], \
    'A':['D'],\
    'B':['D'],\
    'C':['D']}

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(U,V,Graph)

u = {'Aexo': True,'Bexo':False,'Cexo':True}
v = dict()
for k in V.keys():
    v[k] = None

Sit = Situation(Mod,u,v)

Mu = copy.deepcopy(Sit)
Mu.set_val_v()

fact = {'D':True}

for d in actual_cause_generator_v2(fact,Mu):
    assert test_AC1(d,fact,Mu) == True
    assert test_AC2v2(d,fact,Mu) == True
    assert test_AC3v2(d,fact,Mu) == True

Mu.u['Bexo']=True
Mu.u['Cexo']=False
Mu.reset_val_v()
Mu.set_val_v()

for d in actual_cause_generator_v2(fact,Mu):
    assert test_AC1(d,fact,Mu) == True
    assert test_AC2v2(d,fact,Mu) == True
    assert test_AC3v2(d,fact,Mu) == True