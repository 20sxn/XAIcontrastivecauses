### Main things to deal with causes

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
	
	def set_val_v(self):
		"""
		Calcule les valeurs de v non définies
		"""
		for k,v in self.v.items():
			if v == None:
				self.v[k] = value(k,self,set_val=True)
	
	def reset_val_v(self):
		"""
		Mets toutes les valeurs de v à None
		"""
		for k in self.M.V.keys():
			self.v[k]=None

	#update functions


## GRAPH MANIPULATION
def value(X,Mu,set_val = False):
	"""
	variable * Situation -> value
	Calculer la valeur de la variable X en fonction des autres variables
    """
	if X in Mu.u:
		return Mu.u[X]
	if X in Mu.v:
		if Mu.v[X] != None:
			return Mu.v[X]
	parents = Mu.val_Parents(X)   #dictionnaire noeuds parent de X dans M.G -> valeur
	if len(parents) == 0:
        #cas de base = racine : retourner sa valeur
		return Mu.u[X]

	for k,v in parents.items():
		if v == None: # on ne connait pas la valeur
			parents[k] = value(k,Mu)
	if set_val:
		Mu.v[X] = Mu.M.G.P[X][1](parents)
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

def search(args):
	"""
	list[list] -> list[list]
	retourne le produit cartesien des ensembles dans la liste args
	"""
	pools = [tuple(pool) for pool in args]
	result = [[]]
	for pool in pools:
		result = [x+[y] for x in result for y in pool]
	#for prod in result:
	#	yield list(prod)
	return result

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

def sub(dic1,dic2):
    """
    return True if forall k in dic1.keys(), k in dic2.keys()
	i.e. dic1.keys() \in dic2.keys()
    """
    for k in dic1.keys():
        if k not in dic2.keys():
            return False
    return True

def fullsub(dic1,dic2):
	"""
	return True if forall k,v in dic1.items, k,v in dic2.items()
	i.e. dic1 \in dic2
	"""
	for k,v in dic1.items():
		if k not in dic2:
			return False
		elif v!= dic2[k]:
			return False
	return True

#TESTING ACTUAL CAUSE

def test_AC1(x,fact,Mu):
	"""
	dict * dict * class Situation
	return True iff AC1 is respected, False otherwise
	"""
	return check(x,Mu) and check(fact,Mu)


def test_AC2(X,fact,Mu,verbose=False):
	"""
	dict * dict * class Situation
	return True iff AC2 is respected, False otherwise
	"""
	Mutmp = copy.deepcopy(Mu)
	Mutmp.set_val_v()
	W = diff(Mutmp.v,X) # partition de V en X

	var_test_xprime = list(X.keys())
	combi_test_xprime = search([Mutmp.M.V[k] for k in X.keys()]) # ensemble des valeurs possibles pour x'
	for combi in combi_test_xprime:
		if set(X.values()) == set(combi): # on s'assure que x' est différent de x
			combi_test_xprime.remove(combi)

	if verbose:
		print(combi_test_xprime)
		cpt = 0

	for sublW in subsets(dico2list(W)):
		if len(sublW)>0:
			w = dict(sublW) #peut etre verifier si w non vide à demander

			if verbose:
				print("Boucle " + str(cpt) + " w")
				print(w)
				cpt += 1


			for combi_xprime in combi_test_xprime:
				#xprime = dict() # dictionnaire representant X = x'
				#for i in range(len(var_test_xprime)):
				#	xprime[var_test_xprime[i]] = combi_xprime[i]

				#newv = w.copy() # contient les variables de w et de x'
				#for var,val in xprime.items():
				#	newv[var] = val
				newv = w.copy()
				for i in range(len(var_test_xprime)):
					newv[var_test_xprime[i]] = combi_xprime[i]

				if verbose:
					print("\tBoucle x'")
					#print("\t",xprime)
					print("\t",newv)

				newMu = Situation(Mutmp.M,Mutmp.u,newv)
				if check_not(fact,newMu):
					return True
	return False

def test_AC3(X,fact,Mu):
	"""
	dict * dict * class Situation
	return True iff AC3 is respected, False otherwise
	"""
	subsets_x = subsets_size(list(X.keys()),len(X)) #Tous les sous-ensembles possibles de X
	for sub in subsets_x:
		newx = dict()
		for var in sub:
			newx[var] = X[var]
		if(test_AC1(newx,fact,Mu) and (test_AC2(newx,fact,Mu))):
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

def test_partial_cause(x,phi,Mu):
	"""
	return True iff x is a partial cause of phi in Mu=(M,u)
	"""
	return test_actual_cause(x,phi,Mu) #and is_subset(x,phi)

# TESTING COUNTERFACTUAL CAUSE

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


def test_CC4(x,y):
	"""
	dict * dict -> bool
	return True iff CC4 is respected, False otherwise
	"""
	return (len(diff_cond(x,y))>0)


def test_CC5(x,y,fact,foil,Mu):
    """
    dict**5 -> bool
    Return True if CC5 is respected, False otherwise
    """
    v_x = diff(Mu.u,x)
    u_x = diff(Mu.v,x)
    l_all = v_x.copy()
    l_all.update(u_x)
    for subl in subsets(dico2list(l_all)):
        new_x = x.copy()
        new_x.update(subl)
        if(test_CC1(new_x,fact,Mu) and test_CC2(foil,Mu) and test_CC3(y,foil,Mu) and test_CC4(x,y)):
            return False
    return True
        

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


# CAUSE GENERATION

def actual_cause_generator(fact,Mu,verbose = False): #same fuction, only difference : test_AC2 -> test_AC2v2
	"""
	dict * situation -> dict
	retourne la liste des causes effective de fact dans la situation (M,u)
	"""
	if not check(fact,Mu): #si fact n'est pas vérififié dans la situation (M,u)
		return []
	Mutmp = copy.deepcopy(Mu)
	Mutmp.set_val_v()

	lres = []

	#xu = Mutmp.u
	xu = dict() #temporaire : a voir si on test sur les variables exo, voir combi_test_xprime(test_AC2)
	xv = Mutmp.v
	to_test = list(sorted(subsets(dico2list(xu)+dico2list(xv)),key = len))[1:] 	#enumere toutes les combinaisons de variables a tester
																				#on les tris par taille pour vérifier AC3 par construction
	for lx in to_test:
		x = dict(lx)
		if verbose:
			print(lx)
		if not sub(fact,x): #on ne veut pas que le fact se retrouve comme cause de lui meme.
			condAC3 = True
			for d in lres:
				if sub(d,x): #Test AC3
					condAC3 = False
					break
			if condAC3:
				if  test_AC1(x,fact,Mutmp) and test_AC2(x,fact,Mutmp): #AC3 vraie par construction
					lres.append(x)
	return lres


def counterfactual_cause_generator(fact,foil,Mu,verbose = False):
	"""
	dict * dict * situation -> dict
	retourne la liste des causes contrefactuelle de (fact,foil) dans la situation Mu
	"""
	#CC1
	ac = actual_cause_generator(fact,Mu)
	lx = [] #liste des causes partielles
	for c in ac:
		[lx.append(dict(i)) for i in subsets(dico2list(c))[1:] if i not in lx]
	lx = sorted(lx,key = len,reverse = True) #on ordonne par nombre de variable dans la cause (ordre decroissant)

    
    #CC2
	if not check_not(foil,Mu):
		raise Exception('foil is True under Mu')
    
	if not check(fact,Mu): #not in CC2 but better to test it early on.
		raise Exception('fact is False under Mu')
        
    #CC4
	#l_X = [] #liste des valeurs possible pour X
	#[l_X.append(dict()) for i in range(len(lx))]
	#for i in range(len(lx)):
	#	l_X.append(dict())
	#	for key in lx[i]:
	#		l_X[i][key] = Mu.M.V[key]


	#combi_test_y = [] #combinaison de valeurs a tester pour X = y
	#[combi_test_y.append(search([l for l in l_X[i].values()])) for i in range(len(l_X))]

	ly = [] #liste des listes des X = y en sachant X = x   
			#liste pour les variables X des listes des valeurs y possibles i.e. ly[i] correspond a var_X[i] et contient la liste des assignations de valeurs possibles
	for i in range(len(lx)):
		ly.append([])
		#var_X = list(l_X[i].keys())
		var_X = list(lx[i].keys())
		#combi_test_y = search([l for l in l_X[i].values()])
		combi_test_y = search([l for l in [Mu.M.V[key] for key in lx[i]]])
		for combi_y in combi_test_y:
			ly[i].append(dict())
			for j in range(len(var_X)):
				ly[i][-1][var_X[j]] = combi_y[j]
		if lx[i] in ly[i] : ly[i].remove(lx[i]) #CC4

	#for i in range(len(ly)):
	#	if lx[i] in ly[i] : ly[i].remove(lx[i]) #CC4

	if verbose:
		for i in range(len(ly)):
			print(ly[i])
			print(lx[i])
    #CC3
	lres = []
	for iteration in range(len(ly)): #une itération = une cause partielle X = x
		for y in ly[iteration]:
			condCC5 = True #on obtient CC5 par construction
			for d in lres:
				if fullsub(y,d[1]): #if y \in d[1] for some d in lres then CC5 is false     d[1] because it's where X=y is stored
					condCC5 = False #may want to choose better the subsomption fucntion depending on what we want
					break
			if condCC5:
				allW = diff(Mu.M.V,y)
				allW = diff(allW,foil) #we remove any variable from the foil in our Ws
				for subW in subsets(dico2list(allW)):
					stop = False
					if len(subW)>0: #non Empty

						W = dict(subW) #list of all value for a each variable of W

						var_test_w = list(W.keys())
						combi_test_w = search([l for l in W.values()]) #list of all possible value for W

						for combi_w in combi_test_w:
							w = dict() # dictionnaire representant W = w
							for i in range(len(var_test_w)):
								w[var_test_w[i]] = combi_w[i]

							newv = w.copy()
							for k,v in y.items():
								newv[k] = v
								
							newMu = Situation(Mu.M,Mu.u,newv)
							#test partial cause (y is a partial cause of foil under this Situation)
							lac = actual_cause_generator(foil,newMu)
							for c in lac: #we must test for each of these cause if X=y \in c
								if verbose:
									print("-"*70)
									print(newv)
									print(c)
									print(y)
									print("-"*70)
								if sub(y,c): #X=y is a partial cause of foil									
									lres.append((lx[iteration],y)) #if all CC1-5 holds for (X = x,X = y) then its a CC.
									stop = True #we already found that (X=x,X=y) is a cc for (fact,foil) so we can stop testing for that value y
									break
							if stop:
								break
					if stop:
						break
	return lres

