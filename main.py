### Main things to deal with causes

import numpy as np

class CausalGraph:
	def __init__(self,P,C):
		self.P = P #dictionnaire parents {'variable' : ([list of parent variables (string)],function)}
		self.C = C #dictionnaire enfants {'variable' : [liste of children variables (string)]}

	def get_Parents(self,n):
		if n in self.P.keys():
			return self.P[n][0]
		return []

	def get_Children(self,n):
		if n in self.C.keys():
			return self.C[n]
		return []

	def get_function(self,n):
		if n in self.P.keys():
			return self.P[n][1]
		return False

	def set_Parents(self,n,p):
		for k in self.P.keys():
			if k==n:
				self.P[n][0]=p

	def set_Children(self,n,c):
		for k,v in self.C.items():
			if k==n:
				self.C[n]=c

	def set_function(self,n,f):
		for k in self.P.keys():
			if k==n:
				self.P[n][1] = f
	

class Signature:
	def __init__(self,U,V):
		self.U = U # dict exogenous variable -> list of possible values
		self.V = V  # dict exogenous variable -> list of possible values
        
class Model(Signature):
	def __init__(self,G):
		Signature.__init__(self)
		self.G = G # class CausalGraph object

class Situation:
	def __init__(self,M,u,v):
		self.M = M # class Model object
		self.u = u # dict exgenous variable -> value
		self.v = v # dict endogenous variable -> value
	
	#update functions

        
def value(X,Mu):
	"""
	variable * Situation -> value
	Calculer la valeur de la variable X en fonction des autres variables
    """
	parents = Mu.M.G.get_Parents(X)   #dictionnaire des noeuds parent de X dans M.G
	if len(parents) == 0:
        #cas de base = racine : retourner sa valeur
		return Mu.u[X]
	for k,v in parents.items():
		if v == None: # on ne connait pas la valeur
			parents[k] = value(k,Mu)
	return Mu.M.G.P[X][1](Mu)

def check(phi,Mu):
	"""
	dict * class Situation -> bool
	return True iff (M,u) |= phi
	"""
	for k,v in phi.items():
		if v != value(k,Mu):
			return False
	return True


def check_not(psi,Mu):
	"""
	dict * class Situation -> bool
	return True iff (M,u) |= not psi
	"""
	for k,v in psi.items():
		if v != value(k,Mu):
			return True
	return False

## PREDICATES TO PROVE X=x ACTUAL CAUSE OF phi IN (M,u)

def test_AC1(x,fact,Mu):
	return check(x,Mu) and check(fact,Mu)


def produit(liste):
	produit = 1
	for i in liste:
		produit = produit * i
	return produit

def test_AC2(X,M,u):
	i = 0
	b = False
	W = (M.S.V-X) #partition de V en X et W
	x_prim = [] #la liste de toutes les combinaisons possibles des valeurs de X
	nb_possibilities=produit([len(r) for r in M.R.values()]) #nb de combinaisons possibles
	while(i<nb_possibilities):
		tmp = []
		for k,v in X:
			new_val = v
			while(new_val == v):
				new_val= np.random.choice(M.S.R[k])
			tmp.append((k,new_val))
		if tmp not in x_prim:
			x_prim.append(tmp)
			i+=1
	for x in x_prim:
		if(check(x+W,M,u)):# si M,u |= [X <- x_prim et W <- w] Phi alors on renvoie false car il y a un autre ensemble de valeur != x qui satisfait Phi
			b=True
	return not(b)

def subsets(liste):
	if len(liste)==0:
		return [[]]
	x = subsets(liste[1:])
	return x + [[liste[0]] + y for y in x]

def subsets_size(liste,n):
	return [l for l in subsets(liste) if len(l)<n]


def test_AC3(X,fact,Mu):
	subsets_x = subsets_size(X,len(X)) #Tous les sous-ensembles possibles de X 
	for sub in subsets_x:
		if(test_AC1(sub,fact,Mu) and (test_AC2(sub,Mu))):
			return False	
	return True



## PREDICATES TO PROVE <X=x,X=y> COUNTERFACTUAL CAUSE OF <fact,foil> IN (M,u) [see p.10]

def test_CC1(X,fact):
    """
    dict * dict * situation -> bool
    Return True if CC1 is respected, False otherwise
    """
    f = fact.items()
    for x in X.items():
        if x not in f:
            return False
    return True


def test_CC2(foil,Mu):
	"""
    dict * situation -> bool
    Return True if CC2 is respected, False otherwise
    """
	return check_not(foil,Mu)	


def test_CC3():
    pass


def diff_cond(D1,D2):
    """
    dict * dict -> dict
    Input : dictionnaries of variables and their values
    Hypothesis : same variables in D1 and D2
    Output : dictionnary containing the difference condition between D1 and D2 (key = variable, value = tuple of values in D1 and D2)
    """
    res = dict()
    for k,v in D1.items():
        v2 = D2[k]
        if v2 != v:
            res[k] = (v,v2)
    return res

def test_CC4(x,y):
    return(len(diff_cond(x,y))==0)


def test_CC5(X,fact,foil):
    """
    dict**3 -> bool
    Return True if CC5 is respected, False otherwise
    """
    diff1 = set(fact.items()).difference(set(foil.items()))
    diff2 = set(foil.items()).difference(set(fact.items()))
    diff = list(diff1.union(diff2))

    if (len(set(X) & set(diff))==len(X)):
        return True
    return False

def test_counterfactual_cause(x, y, fact, foil, Mu):
    """
    dict**4 * causal model * dict -> bool
    Return True if <x,y> is a contrastive counterfactual actual cause
    (= counterfactual cause) of <fact,foil>, False otherwise
    """
    a = test_CC1(x,fact,Mu)
    a = a and test_CC2(foil,Mu)
    a = a and test_CC3(y,foil,Mu)
    a = a and test_CC4(x,y)
    a = a and test_CC5(x,fact,foil)
    return a