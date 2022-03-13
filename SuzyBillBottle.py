#Suzy, Bill and bottle example from Halpern 2015
#maybe delete STexo and BTexo and put ST and BT as endogenous

from main import *

def compute_ST(param):
    return param['STexo']

def compute_BT(param):
    return param['BTexo']

def compute_BS(param):
    return param['SH'] or param['BH']

def compute_SH(param):
    return param['ST']

def compute_BH(param):
    return param['BT'] and not(param['SH'])

# Exogenous variables
U = {'STexo':[False, True], \
    'BTexo':[False, True]}

# Endogenous variables
V = {'ST':[False, True], \
    'BT':[False, True], \
    'BS':[False, True], \
    'SH':[False, True], \
    'BH':[False, True]}

# Parent node for each endogenous variable
P = {'ST':(['STexo'],compute_ST), \
    'BT':(['BTexo'],compute_BT), \
    'BS':(['SH','BH'],compute_BS),\
    'SH':(['ST'],compute_SH),\
    'BH':(['BT','SH'],compute_BH)}

C =  {'STexo':['ST'], \
    'BTexo':['BT'], \
    'BH':['BS'], \
    'SH':['BS','BH'],\
    'ST':['SH'],\
    'BT':['BH']}

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(U,V,Graph)

u = {'STexo': True,'BTexo':True}
v = dict()
for k in V.keys():
    v[k] = None

Sit = Situation(Mod,u,v)

Mu = copy.deepcopy(Sit)
Mu.set_val_v()

fact = {'BS':True}

for d in actual_cause_generator_v2(fact,Mu):
    assert test_AC2v2(d,fact,Mu) == True