### Example of Miller with anthopods

from main import *

# Functions to compute endogenous variables
def compute_nb_legs(Sit):
    U = Sit.u['U']
    if U == "Spider":
        return 8
    elif U == "Beetle":
        return 6
    elif U == "Bee":
        return 6
    elif U == "Fly":
        return 6
    else:
        return None

def compute_stinger(Sit):
    U = Sit.u['U']
    if U == "Spider":
        return False
    elif U == "Beetle":
        return False
    elif U == "Bee":
        return True
    elif U == "Fly":
        return False
    else:
        return None

def compute_nb_eyes(Sit):
    U = Sit.u['U']
    if U == "Spider":
        return 8
    elif U == "Beetle":
        return 2
    elif U == "Bee":
        return 5
    elif U == "Fly":
        return 5
    else:
        return None

def compute_compound_eyes(Sit):
    U = Sit.u['U']
    if U == "Spider":
        return False
    elif U == "Beetle":
        return True
    elif U == "Bee":
        return True
    elif U == "Fly":
        return True
    else:
        return None

def compute_wings(Sit):
    U = Sit.u['U']
    if U == "Spider":
        return 0
    elif U == "Beetle":
        return 2
    elif U == "Bee":
        return 4
    elif U == "Fly":
        return 2
    else:
        return None

def compute_output(Sit):
    (nb_legs,stinger,nb_eyes,compound_eyes,wings) = (Sit.v["nb_legs"],Sit.v["stinger"],Sit.v["nb_eyes"],Sit.v["compound_eyes"],Sit.v["wings"],)
    if (nb_legs,stinger,nb_eyes,compound_eyes,wings) == (8,False,8,False,0):
        return "Spider"
    elif (nb_legs,stinger,nb_eyes,compound_eyes,wings) == (6,False,2,True,2):
        return "Beetle"
    elif (nb_legs,stinger,nb_eyes,compound_eyes,wings) == (6,False,5,True,4):
        return "Bee"
    elif (nb_legs,stinger,nb_eyes,compound_eyes,wings) == (6,False,5,True,2):
        return "Fly"
    else:
        return "Unknown"

# Exogenous variables
U = {'U': ["Spider", "Beetle", "Bee", "Fly"]}

# Endogenous variables
V = {'nb_legs' : [6, 8], \
    'stinger' : [True, False], \
    'nb_eyes' : [2, 5, 8], \
    'compound_eyes' : [True, False], \
    'wings' : [0, 2, 4], \
    'output': ["Spider", "Beetle", "Bee", "Fly","Unknown"]}

# Parent node for each endogenous variable
P = {'nb_legs' : (['U'],compute_nb_legs), \
    'stinger' : (['U'],compute_stinger), \
    'nb_eyes' : (['U'],compute_nb_eyes), \
    'compound_eyes' : (['U'],compute_compound_eyes), \
    'wings' : (['U'],compute_wings), \
    'output' : (['nb_legs'],compute_output)}

C =  {'U' : ['nb_legs'], \
    'nb_legs' : ['output'], \
    'stinger' : ['output'], \
    'nb_eyes' : ['output'], \
	'compound_eyes' : ['output'], \
    'wings' : ['output'],\
	'output' : []}

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(U,V,Graph)

u = {'U': "Spider"}
v = {'nb_legs' : 8, \
    'stinger' : False, \
    'nb_eyes' : 8, \
    'compound_eyes' : False, \
    'wings' : 0, \
    'output': "Spider"}

Sit = Situation(Mod,u,v)



# Test de value
assert(value("wings",Sit)==0)
assert(not(value("wings",Sit)==2))
assert(value("output",Sit)=="Spider")


# Test de check
phi = {"wings" : 0, "stinger" : False}
assert(check(phi,Sit)==True)

phi = {"wings" : 0, "stinger" : True}
assert(check(phi,Sit)==False)

phi = {"output" : "Spider"}
assert(check(phi,Sit)==True)

phi = {"output" : "Bee"}
assert(check(phi,Sit)==False)


# Test de AC1
u = {'U': "Bee"}
v = {'nb_legs' : 6, \
    'stinger' : False, \
    'nb_eyes' : 5, \
    'compound_eyes' : True, \
    'wings' : 4, \
    'output': "Bee"}

Sit = Situation(Mod,u,v)

x = {"nb_legs" : 6}
fact = {"output" : "Bee"}
assert(test_AC1(x,fact,Sit))

x = {"nb_legs" : 4}
fact = {"output" : "Bee"}
assert(test_AC1(x,fact,Sit)==False)


# Test de AC2
#print(test_AC2(x,fact,Sit))
