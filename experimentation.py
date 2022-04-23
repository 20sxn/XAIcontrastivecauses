from main import *
import random

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
    v = dict()
    return Situation(Mod,u,v)
        