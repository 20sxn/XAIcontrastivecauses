#Exemple simple avec output == v1 OR v2 == u1 OR u2

from main import *


def compute_v1(param):
    return param['u1']

def compute_v2(param):
    return param['u2']

def compute_output(param):
    return param['v1'] or param['v2']

# Exogenous variables
U = {'u1':[False, True], \
    'u2':[False, True]}

# Endogenous variables
V = {'v1':[False, True], \
    'v2':[False, True], \
    'output':[False, True]}

# Parent node for each endogenous variable
P = {'v1':(['u1'],compute_v1), \
    'v2':(['u2'],compute_v2), \
    'output':(['v1','v2'],compute_output)}

C =  {'u1':['v1'], \
    'u2':['v2'], \
    'v1':['output'], \
    'v2':['output']}

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(U,V,Graph)

u = {'u1': True,'u2':True}
v = dict()
for k in V.keys():
    v[k] = None

Sit = Situation(Mod,u,v)

Mu = copy.deepcopy(Sit)
Mu.set_val_v()

fact = {'output':True}

for d in actual_cause_generator_v2(fact,Mu):
    assert test_AC1(d,fact,Mu) == True
    assert test_AC2v2(d,fact,Mu) == True
    assert test_AC3v2(d,fact,Mu) == True

Mu.u['u2']=False
Mu.reset_val_v()
Mu.set_val_v()

for d in actual_cause_generator_v2(fact,Mu):
    assert test_AC1(d,fact,Mu) == True
    assert test_AC2v2(d,fact,Mu) == True
    assert test_AC3v2(d,fact,Mu) == True