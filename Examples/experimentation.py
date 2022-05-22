from main import *
import random
import time
from matplotlib import pyplot as plt

def gen_fun(inp):
    def F(param):
        return param[inp]
    return F

def gen_output_fun(N,mode):
    assert mode in ["AND","OR"]
    if mode == "AND":
        def OF(param):
            a = True
            for i in range(N):
                a = a and param[str(i)]
            return a
    elif mode == "OR":
        def OF(param):
            a = False
            for i in range(N):
                a = a or param[str(i)]
            return a
    return OF

def gen_graph(N,mode):
    LF = []
    for i in range(N):
        f = gen_fun("exo"+str(i))
        LF.append(f)
    of = gen_output_fun(N,mode)
    LF.append(of)
    P = {str(i):(["exo"+str(i)],LF[i]) for i in range(N)}
    P["output"] = ([str(i) for i in range(N)],LF[N])
    C = {str(i):["output"] for i in range(N)}
    for i in range(N):
        C["exo"+str(i)] = str(i)
    return CausalGraph(P,C)

def gen_model(N,mode):
    U = dict()
    V = dict()
    for i in range(N):
        U["exo"+str(i)] = [False,True]
        V[str(i)] = [False,True]
    V["output"] = [False,True]
    Graph = gen_graph(N,mode)
    return Model(U,V,Graph)

def gen_sit(N,mode,u=dict()):
    Mod = gen_model(N,mode)
    if len(u) != N:
        u = {"exo"+str(i):bool(random.getrandbits(1)) for i in range(N)}
    print("u",u,"\n")
    v = dict()
    return Situation(Mod,u,v)

#temps d'exécution en fonction du nombre de variables.
d = []
for i in range(1,15):
    G = gen_graph(i,"AND")
    M = gen_model(i,"AND")
    S = gen_sit(i,"AND")
    S.set_val_v()
    fact = {'output':S.v['output']}
    foil =  {'output':not(S.v['output'])}
    start = time.time()
    actual_cause_generator(fact,S)
    #counterfactual_cause_generator(fact,foil,S)
    end = time.time()
    duree = end - start
    d.append(duree)
print(d)

#############################Profondeur###################################
S
def gen_output_fun2(N,D,mode):
    assert mode in ["AND","OR"]
    if mode == "AND":
        def OF(param):
            a = True
            for i in range(1,N+1):
                a = a and param[str(i)+str(D-1)]
            return a
    elif mode == "OR":
        def OF(param):
            a = False
            for i in range(1,N+1):
                a = a or param[str(i)+str(D-1)]
            return a
    return OF
def gen_graph_2(N,D,mode):
    LF = []
    cpt = 0
    endo = []
    for i in range(1,N+1):
        tmp = []
        for j in range(0,D-1):
            f = gen_fun(str(i)+str(j))
            tmp.append(f)
        LF.append(tmp)
    #functions = [[F10,F11,F12,F13,F14....F1(D-1)],[[20,21,22,23,24....2(D-1)]]]
    #variables = [[10,11,12,13,14],[20,21,22,23,24],[30,31,32,33,34]] n0 ==> variable exogène numero n 
    of = gen_output_fun2(N,D,mode)
    LF.append([of])
    P = {}
    C = {}
    for i in range(1,N+1): 
        for j in range(D-1):
            P[str(i)+str(j+1)]= [str(i)+str(j)],LF[i-1][j]
            C[str(i)+str(j)]=[str(i)+str(j+1)] 
    P["output"] = ([str(i)+str(D-1) for i in range(1,N+1)],LF[N][0])
    for i in range(1,N+1):
        C[str(i)+str(D-1)]= ["output"]
    return CausalGraph(P,C)

def gen_model_2(N,D,mode):
    U = dict()
    V = dict()
    for i in range(1,N+1):
        U[str(i)+"0"] = [False,True]
        for j in range(1,D):
            V[str(i)+str(j)] = [False,True]
    V["output"] = [False,True]
    Graph = gen_graph_2(N,D,mode)
    return Model(U,V,Graph)

def gen_sit_2(N,D,mode,u=dict()):
    Mod = gen_model_2(N,D,mode)
    if len(u) != N:
        u = {str(i)+"0":bool(random.getrandbits(1)) for i in range(1,N+1)}
    v = dict()
    return Situation(Mod,u,v) 

def main_test(N,D,mode):
    G = gen_graph_2(N,D,mode)
    M = gen_model_2(N,D,mode)
    S = gen_sit_2(N,D,mode)
    S.set_val_v()
    fact = {'output':S.v['output']}
    foil =  {'output':not(S.v['output'])}
    start = time.time()
    #actual_cause_generator(fact,S)
    print(counterfactual_cause_generator(fact,foil,S))
    end = time.time()
    duree = end - start
    return duree

