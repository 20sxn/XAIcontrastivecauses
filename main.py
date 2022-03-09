### Main things to deal with causes

import numpy as np

def produit(liste):
	"""
	list -> float
	return the product of all elements in liste
	"""
	produit = 1
	for i in liste:
		produit = produit * i
	return produit

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
	def __init__(self,U,V,G):
		Signature.__init__(self,U,V)
		self.G = G # class CausalGraph object

class Situation:
	def __init__(self,M,u,v):
		self.M = M # class Model object
		self.u = u # dict exgenous variable -> value
		self.v = v # dict endogenous variable -> value
	
	#update functions
	
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


        
	def value(self,X):
		"""
		variable -> value
		Calculer la valeur de la variable X en fonction des autres variables
	    """
		parents = self.val_Parents(X)   #dictionnaire des noeuds parent de X dans M.G
		if len(parents) == 0:
	        #cas de base = racine : retourner sa valeur
			return self.u[X]
		for k,v in parents.items():
			if v == None: # on ne connait pas la valeur
				parents[k] = self.value(k)
		return self.M.G.P[X][1](parents)
	
	def check(self,phi):
		"""
		dict -> bool
		return True iff (M,u) |= phi
		"""
		for k,v in phi.items():
			if v != self.value(k):
				return False
		return True


	def check_not(self,psi):
		"""
		dict * class Situation -> bool
		return True iff (M,u) |= not psi
		"""
		for k,v in psi.items():
			if v != self.value(k):
				return True
		return False
	
	## PREDICATES TO PROVE X=x ACTUAL CAUSE OF phi IN (M,u) [see p.9-10]
	
	def test_AC1(self,x,fact):
		"""
		dict * dict * class Situation
		return True iff AC1 is respected, False otherwise
		"""
		return self.check(x) and self.check(fact)
	
	
	def test_AC2(self,X,fact):
		"""
		dict * dict * class Situation
		return True iff AC2 is respected, False otherwise
		"""
		i = 0
		#b = False
		
		#partition de V en X et W
		W = dict()
		for var,val in self.v.items():
			if var not in X.keys():
				W[var] = val
		
		x_prim = [] #la liste de toutes les combinaisons possibles des valeurs de X
		nb_possibilities=produit([len(r) for r in Mu.U.values()]+[len(r) for r in Mu.V.values()]) #nb de combinaisons possibles
		while(i<nb_possibilities):
			tmp = []
			for k,v in X.items():
				new_val = v
				while(new_val == v):
					new_val= np.random.choice(Mu.M.V[k])
				tmp.append((k,new_val))
			if tmp not in x_prim:
				x_prim.append(tmp)
				i+=1
		for x in x_prim:
			newMu = "Mu avec les valeurs X=x' et W=w" # TODO
			if(newMu.check_not(fact)):# si M,u |= [X <- x_prim et W <- w] Phi alors on renvoie false car il y a un autre ensemble de valeur != x qui satisfait Phi
				return True
		return False
	
	
	def test_AC3(self,X,fact):
		"""
		dict * dict * class Situation
		return True iff AC1 is respected, False otherwise
		"""
		subsets_x = subsets_size(X,len(X)) #Tous les sous-ensembles possibles de X 
		for sub in subsets_x:
			if(test_AC1(sub,fact,Mu) and (test_AC2(sub,Mu))):
				return False	
		return True
	
	def test_actual_cause(self,x,fact):
		return self.test_AC1(x,fact) and self.test_AC2(x,fact) and self.test_AC3(x,fact)
	
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
	
	def test_partial_cause(self,x,phi):
		"""
		return True iff x is a partial cause of phi in Mu=(M,u)
		"""
		return self.test_actual_cause(phi) and is_subset(x,phi)
	
	def test_CC1(self,X,fact):
	    """
	    dict * dict * situation -> bool
	    Return True if CC1 is respected, False otherwise
	    """
	    return self.test_partial_cause(X,fact)
	
	
	def test_CC2(self,foil):
		"""
		dict * situation -> bool
		Return True if CC2 is respected, False otherwise
		"""
		return self.check_not(foil)	
	
	
	def test_CC3(self,y,foil):
		W = subsets((Mu.S.V-y)) #parties des valeurs possibles pour W
		for w in W:
			newMu = "Mu avec les valeurs W=w" #TODO
			if self.test_partial_cause(y,foil):
				return True
		return False
	
	
	def test_CC4(self,x,y):
		"""
		dict * dict -> bool
		return True iff CC4 is respected, False otherwise
		"""
		return (len(diff_cond(x,y))==0)
	
	
	def test_CC5(self,X,fact,foil):
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
	
	def test_counterfactual_cause(self,x, y, fact, foil):
	    """
	    dict**4 * causal model * dict -> bool
	    Return True if <x,y> is a contrastive counterfactual actual cause
	    (= counterfactual cause) of <fact,foil>, False otherwise
	    """
	    a = self.test_CC1(x,fact)
	    a = a and self.test_CC2(foil)
	    a = a and self.test_CC3(y,foil)
	    a = a and self.test_CC4(x,y)
	    a = a and self.test_CC5(x,fact,foil)
	    return a