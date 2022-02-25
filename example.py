### Implementation of an example

from main import *


# Functions to compute endogenous variables
def compute_prix_plein(prix_carburant,capacite_carburant):
    return prix_carburant*capacite_carburant

def compute_prix_assurance(annee_prod):
    return 10000*(1/(2022-annee_prod)**2)

def compute_prix_Carburant(type_carburant):
	if(type_carburant=='Diesel'):
		return 1.50
	if(type_carburant=='Essence'):
		return 1.6
	else:
		return 0.72
def compute_capacite_carburant(longueur,hauteur):
	return longueur*hauteur*20

def compute_output(nb_places,nb_chevaux,prix_plein,annee_prod,prix_assurance):
	return 0 #a faire

	
# Exogenous variables
U = {'nb_places':[1,2,3,4,5,6,7], \
    'nb_chevaux':[20,30,40,50,60,70,80,90,100,120], \
    'longueur':[1.5,2,3,4], \
    'hauteur':[1.6,1.7,1.8,1.9], \
    'type_carburant':['Diesel','Essence','Gazeux'], \
    'annee_prod':[1930,1940,1950,1960,1970,1980,1990,2000,2010,2020]}

# Endogenous variables
V = {'prix_carburant':[1.50,1.6,0.72], \
    'prix_plein':[72.00000000000001,76.5,81.0,85.4999999999999996,102.0,108.0,114.0,144.00000000000003,153.0,162.0,170.99999999999997,192.0,204.0,216.0,228.0,76.80000000000001,81.60000000000001,86.4,91.19999999999999,102.4,
108.80000000000001,115.2,121.60000000000001,
153.60000000000002,163.20000000000002,172.8,182.39999999999998,204.8,217.60000000000002,230.4,243.20000000000002,34.56,36.72,38.879999999999995,41.03999999999999,46.08,48.96,
51.839999999999996,54.72,69.12,73.44,77.75999999999999,82.07999999999998,92.16,97.92,103.67999999999999,109.44], \
    'prix_assurance':[1.1814744801512287,1.48720999405116,1.9290123456790123,2.601456815816858,3.698224852071006,5.668934240362812,9.765625,20.66115702479339,69.44444444444444,2500.0], \
    'capacité_carburant':[48.00000000000001,51.0,54.0,56.99999999999999,64.0,68.0,72.0,76.0,96.00000000000001,102.0,108.0,113.99999999999999,128.0,136.0,144.0,152.0], \
    'output':['peu cher','cher','très cher','très très cher']}
#parent node for each endogenous variable
P = {'prix_carburant':(['type_carburant'],compute_prix_Carburant), \
    'prix_plein':(['prix_carburant','capacite_carburant'],compute_prix_plein), \
    'prix_assurance':(['annee_prod'],compute_prix_assurance), \
    'capacité_carburant':(['longueur','hauteur'],compute_capacite_carburant), \
    'output':(['nb_places','nb_chevaux','prix_plein','annee_prod','prix_assurance'],compute_output)}

C=  {'type_carburant':['prix_carburant'], \
    'prix_carburant':['prix_plein'], \
    'annee_prod':['prix_assurance','output'], \
    'longueur':['capacité_carburant'], \
	'hauteur':['capacité_carburant'], \
    'nb_places':['output'],\
	'nb_chevaux':['output'],\
	'prix_plein':['output'],\
	'prix_assurance':['output']}

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(Graph)
Sit = Situation(Mod,U,V)

