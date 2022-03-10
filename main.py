### Main things to deal with causes

import numpy as np
import copy

class CausalGraph:
	def __init__(self,P,C):
		self.P = P #dictionnaire parents {'variable' : ([list of parent variables (string)],function)}
		self.C = C #dictionnaire enfants {'variable' : [list of children variables (string)]}

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
	def __init__(self,U,V,G):
		Signature.__init__(self,U,V)
		self.G = G # class CausalGraph object

class Situation:
	def __init__(self,M,u,v):
		self.M = M # class Model object
		self.u = u # dict exgenous variable -> value
		self.v = v # dict endogenous variable -> value
		for k in self.M.V.keys():
			if k not in v:
				v[k] = None

	def val_Parents(self,X):
		"""
		variable -> dict(parent var : value)
		"""
		res = dict()
		parents = self.M.G.get_Parents(X)
		for k in parents:
			if k in list(self.u.keys()):
				res[k] = self.u[k]
			elif k in list(self.v.keys()):
				res[k] = self.v[k]
		return res


	#update functions


def value(X,Mu):
	"""
	variable * Situation -> value
	Calculer la valeur de la variable X en fonction des autres variables
    """
	parents = Mu.val_Parents(X)   #dictionnaire noeuds parent de X dans M.G -> valeur
	if len(parents) == 0:
        #cas de base = racine : retourner sa valeur
		return Mu.u[X]

	for k,v in parents.items():
		if v == None: # on ne connait pas la valeur
			parents[k] = value(k,Mu)

	#lparents = Mu.M.G.get_Parents(X)
	#lvalue = [parents[k] for k in lparents]
	return Mu.M.G.P[X][1](parents)

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

## PREDICATES TO PROVE X=x ACTUAL CAUSE OF phi IN (M,u) [see p.9-10]

def test_AC1(x,fact,Mu):
	"""
	dict * dict * class Situation
	return True iff AC1 is respected, False otherwise
	"""
	return check(x,Mu) and check(fact,Mu)


def produit(liste):
	"""
	list -> float
	return the product of all elements in liste
	"""
	produit = 1
	for i in liste:
		produit = produit * i
	return produit

def diff(d1,d2):
    """
	retourne le dictionnaire d1\(k,v) (k) in d2
	"""
    res = dict()
    for k in d1:
        if k not in d2:
            res[k] = d1[k]
    return res

def dico2list(d):
	"""
	transforme un dictionnaire en liste (opération inverse : dict(l))
	"""
	l = []
	for k,v in d.items():
		l.append((k,v))
	return l

def test_AC2(X,fact,Mu):
	"""
	dict * dict * class Situation
	return True iff AC2 is respected, False otherwise
	"""
	i = 0
	#b = False
	W = diff(Mu.M.V,X) #(Mu.S.V-X) #partition de V en X et W
	for sublW in subsets(dico2list(W)):
		if len(sublW)>0:
			subW = dict(sublW)
			x_prim = [] #la liste de toutes les combinaisons possibles des valeurs de X
			nb_possibilities=produit([len(r) for r in Mu.M.U.values()]+[len(r) for r in Mu.M.V.values()]) #nb de combinaisons possibles
			while(i<nb_possibilities):
				tmp = []
				for k,v in X.items():
					new_val = v
					while(new_val == v):
						if k in Mu.M.V:
							new_val= np.random.choice(Mu.M.V[k])
						elif k in Mu.M.U:
							new_val= np.random.choice(Mu.M.U[k])
						else:
							raise Exception("Variable inconnue")
					tmp.append((k,new_val))
				if tmp not in x_prim: #x_prim = already tested
					x_prim.append(tmp)
					i+=1
					v = dict(tmp)
					for w,val in subW.items():
						v[w]=val
					newMu = Situation(Mu.M,Mu.u,v)
					if(check_not(fact,newMu)):# si M,u |= [X <- x_prim et W <- w] Phi alors on renvoie false car il y a un autre ensemble de valeur != x qui satisfait Phi
						return True
	return False

def subsets(liste):
	"""
	list -> list
	return the list of all subsets of liste
	"""
	if len(liste)==0:
		return [[]]
	x = subsets(liste[1:])
	return x + [[liste[0]] + y for y in x]

def subsets_size(liste,n):
	"""
	list * int -> list(int)
	return the list of elements of liste that have length < n
	"""
	return [l for l in subsets(liste) if len(l)<n]


def test_AC3(X,fact,Mu):
	"""
	dict * dict * class Situation
	return True iff AC1 is respected, False otherwise
	"""
	subsets_x = subsets_size(X,len(X)) #Tous les sous-ensembles possibles de X
	for sub in subsets_x:
		if(test_AC1(sub,fact,Mu) and (test_AC2(sub,Mu))):
			return False
	return True

def test_actual_cause(x,fact,Mu):
	return test_AC1(x,fact,Mu) and test_AC2(x,fact,Mu) and test_AC3(x,fact,Mu)

## PREDICATES TO PROVE <X=x,X=y> COUNTERFACTUAL CAUSE OF <fact,foil> IN (M,u) [see p.10]

def is_subset(X,phi):
	"""
	dict * dict -> bool
	return True iff x is a subset of phi
	"""
	f = phi.items()
	for x in X.items():
		if x not in f:
			return False
	return True

def test_partial_cause(x,phi,Mu):
	"""
	return True iff x is a partial cause of phi in Mu=(M,u)
	"""
	return test_actual_cause(phi,Mu) and is_subset(x,phi)

def test_CC1(X,fact,Mu):
    """
    dict * dict * situation -> bool
    Return True if CC1 is respected, False otherwise
    """
    return test_partial_cause(X,fact,Mu)


def test_CC2(foil,Mu):
	"""
	dict * situation -> bool
	Return True if CC2 is respected, False otherwise
	"""
	return check_not(foil,Mu)


def test_CC3(y,foil,Mu):
	W = diff(Mu.S.V,y) #parties des valeurs possibles pour W
	#W = subsets((Mu.S.V-y))
	for sublW in subsets(dico2list(W)):
		if len(sublW)>0:
			subW = dict(sublW)
			newMu = copy.deepcopy(Mu) #Mu avec valeurs de subW
			for w in subW:
				if w in newMu.U:
					newMu.U[w] = subW[w]
				elif w in newMu.v:
					newMu.v[w] = subW[w]
				else:
					raise Exception("Custom : Mu not properly defined")
			if test_partial_cause(y,foil,newMu):
				return True
	return False


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
	"""
	dict * dict -> bool
	return True iff CC4 is respected, False otherwise
	"""
	return (len(diff_cond(x,y))==0)


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


def actual_cause_generator(fact,Mu):
	"""
	dict * situation -> dict
	retourne une cause actuelle de fact dans la situation (M,u)
	"""
	xu = Mu.u
	xv = Mu.v
	to_test = list(sorted(subsets(dico2list(xu)+dico2list(xv)),key = len))[1:] 	#enumere toutes les combinaisons de variables a tester
																				#on les tris par taille pour vérifier AC3 par construction
	for lx in to_test:
		if  test_AC1(dict(lx),fact,Mu) and test_AC2(dict(lx),fact,Mu): #AC3 vraie par construction
			return dict(lx)
	return dict() #s'il n'y a pas de cause actuelle

def counterfactual_cause_generator(fact,foil,Mu):
	acx = actual_cause_generator(fact,Mu)
	allX = subsets(dico2list(acx))
	pass
