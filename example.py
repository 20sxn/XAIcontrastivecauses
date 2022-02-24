### Implementation of an example

from main import *

# Exogenous variables
U = {'nb_places':[1,2,3,4,5,6,7], \
    'nb_chevaux':[20,30,40,50,60,70,80,90,100,120], \
    'longueur':[1.5,2,3,4], \
    'hauteur':[1.6,1.7,1.8,1.9], \
    'type_carburant':['Diesel','Essence','Gazeux'], \
    'annee_prod':[1930,1940,1950,1960,1970,1980,1990,2000,2010,2020]}

# Endogenous variables
V = {'prix_carburant':[1.50,1.6,0.72], \
    'prix_plein':[], \
    'prix_assurance':[], \
    'capacité_carburant':[30,40,50,60,70,80,90,100], \
    'output':['peu cher','cher','très cher','très très cher']}

# Functions to compute endogenous variables
def compute_prix_plein(prix_carburant,capacite_carburant):
    return prix_carburant*capacite_carburant

def compute_prix_assurance(annee_prod):
    pass

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(Graph)
Sit = Situation(Mod,U,V)

