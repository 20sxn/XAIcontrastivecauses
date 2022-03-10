### Implementation of an example

from main import *


# Functions to compute endogenous variables
def compute_prix_plein(param):
    return param['prix_carburant'] * param['capacite_carburant'] #prix_carburant*capacite_carburant

def compute_prix_assurance(param):
    return 10000*(1/(2022-param['annee_prod'])**2)

def compute_prix_Carburant(param):
    carbu = param['type_carburant']
    if carbu == 'Diesel': #type_carburant
    	return 1.50
    elif carbu == 'Essence': #type_carburant
    	return 1.6
    else:
    	return 0.72

def compute_capacite_carburant(param):
	return param['longueur']*param['hauteur']*20 #longueur*hauteur*20

def compute_output(param):
    #tmp = 20 * nb_places + nb_chevaux + prix_plein//2 + annee_prod//10 + prix_assurance
    tmp = 20 * param['nb_places'] + param['nb_chevaux'] + param['prix_plein']//2 + param['annee_prod']//10 + param['prix_assurance']
    tmp -= 250 #tmp in [0,550]
    tmp = tmp//130 #tmp in [0,4]
    if tmp == 0:
        return 'peu cher'
    elif tmp == 1:
        return 'cher'
    elif tmp == 2:
        return 'très cher'
    elif tmp >= 3:
        return 'très très cher'

# Exogenous variables
U = {'nb_places':[1,2,3,4,5,6,7], \
    'nb_chevaux':[20,30,40,50,60,70,80,90,100,120], \
    'longueur':[1.5,2,3,4], \
    'hauteur':[1.6,1.7,1.8,1.9], \
    'type_carburant':['Diesel','Essence','Gazeux'], \
    'annee_prod':[1930,1940,1950,1960,1970,1980,1990,2000,2010,2020]}

# Endogenous variables
V = {'prix_carburant':[1.50,1.6,0.72], \
    'prix_plein':[72.0, 76.5, 81.0, 85.5, 102.0, 108.0, 114.0, 144.0, 153.0, 162.0, 171.0, 192.0, 204.0, 216.0, 228.0, 76.8, 81.6, 86.4, 91.2, 102.4,
108.8, 115.2, 121.6, 153.6, 163.2, 172.8, 182.4, 204.8, 217.6, 230.4, 243.2, 34.56, 36.72, 38.88, 41.04, 46.08, 48.96,
51.84, 54.72, 69.12, 73.44, 77.76, 82.08, 92.16, 97.92, 103.68, 109.44], \
    'prix_assurance':[1.18, 1.49, 1.93, 2.60, 3.7, 5.67, 9.77, 20.66, 69.44, 250], \
    'capacite_carburant':[48, 51, 54, 57, 64, 68, 72, 76, 96, 102, 108, 114, 128, 136, 144, 152], \
    'output':['peu cher','cher','très cher','très très cher']}

# Parent node for each endogenous variable
P = {'prix_carburant':(['type_carburant'],compute_prix_Carburant), \
    'prix_plein':(['prix_carburant','capacite_carburant'],compute_prix_plein), \
    'prix_assurance':(['annee_prod'],compute_prix_assurance), \
    'capacite_carburant':(['longueur','hauteur'],compute_capacite_carburant), \
    'output':(['nb_places','nb_chevaux','prix_plein','annee_prod','prix_assurance'],compute_output)}

C =  {'type_carburant':['prix_carburant'], \
    'prix_carburant':['prix_plein'], \
    'annee_prod':['prix_assurance','output'], \
    'longueur':['capacite_carburant'], \
	'hauteur':['capacite_carburant'], \
    'nb_places':['output'],\
	'nb_chevaux':['output'],\
	'prix_plein':['output'],\
	'prix_assurance':['output']}

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(U,V,Graph)

u = {'nb_places': 3,'nb_chevaux':30,'longueur' : 3,'hauteur': 1.8, 'type_carburant' : 'Diesel', 'annee_prod': 1980 }
v = dict()
for k in V.keys():
    v[k] = None

Sit = Situation(Mod,u,v)


# Test de value
assert(value("prix_carburant",Sit)==1.5)
assert(value("prix_plein",Sit)==162.0)


# Test de check
phi = {'prix_carburant' : 1.5}
assert(check(phi,Sit))

phi = {'prix_plein' : 162.0}
assert(check(phi,Sit))

phi = {'prix_plein' : 162.0, 'prix_carburant' : 1.5}
assert(check(phi,Sit))

phi = {'prix_plein' : 162.0, 'prix_carburant' : 5}
assert(not(check(phi,Sit)))


# Test de AC1
for k in Sit.v.keys():
    Sit.v[k] = value(k,Sit)
#print(Sit.v)

x = {"nb_chevaux" : 30}
fact = {"output" : "peu cher"}
assert(test_AC1(x,fact,Sit))

x = {"prix_plein" : 0}
fact = {"output" : "peu cher"}
assert(not(test_AC1(x,fact,Sit)))
