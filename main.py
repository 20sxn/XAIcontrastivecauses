# classe M avec signature S (autre classe), F dictionnaire des fonctions, G graphe causal (utiliser une librairie ?)

class CausalGraph:
	def __init__(self,P,C):
		self.P = P #dictionnaire parents {'variable' : {[liste of variables (string)]}
		self.C = C #dictionnaire enfants
	def get_Parents(self,n):
		if n in self.P.keys():
			return self.P[n][0]
		return []
	def get_Children(self,n):
		if n in self.C.keys():
			return self.C[n][0]
		return []
	def get_function(self,n):
		if n in self.C.keys():
			return self.C[n][1]
		return False
	def set_Parents(self,n,p):
		for k,v in self.P.items():
			if k==n:
				self.P[n][0]=p
	def set_Children(self,n,c):
		for k,v in self.C.items():
			if k==n:
				self.C[n]=c
	def set_function(self,n,f):
		for k,v in self.C.items():
			if k==n:
				self.C[n][1]==f
	

class Signature():
	def __init__(U,V,R):
		self.U = U # set of exogenous variables
		self.V = V  # set of endogenous variables
		self.R = R #dict containing possible values for each variable V+U
        
class Model():
	def __init__(S,F,G):
		self.F = F # dict : variable -> function
		self.S = S # causal graph, node = (X,v)
		self.G = G # causal graph, node = (X,v)
        # ajouter u ?
        
def value(X,M,u):
    """
    Calculer la valeur de la variable X en fonction des autres variables
    """
	parents = M.G.get_Parents(X)   #dictionnaire des nœuds parent de X dans M.G
	if len(parents) == 0:
        #cas de base = racine : retourner sa valeur
		return u[X]
	for k,v in parents.items():
		if v == None: # on ne connait pas la valeur
			parents[k] = value(k,M u)
	return M.F[X](u) 
    # ou return M.F[X]() si on met u dans M
#question : faire rentrer u dans la classe  M ?

def check(phi,M,u):
    """
    dict * class M * dict -> bool
    return True iff (M,u) |= phi
    """
	for k,v in phi.items():
		if v != value(k,M,u):
			return False
	return True


def check_not(psi,M,u):
    """
    dict * class M * dict -> bool
    return True iff (M,u) |= not psi
    """
	for k,v in psi.items():
		if v != value(k,M,u):
			return True
	return False

# X=x actual cause of phi in (M,u)

def test_AC1(x,fact,M,u):
	return check(x,M,u) and check(fact,M,u) 


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
		for k,v in X:
			new_val = v
			while(new_val == v):
				new_val= random.choice(M.S.R[k])
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


def test_AC3(X,fact,M,u):
	b = False
	subsets_x = subsets_size(X,len(X)) #Tous les sous-ensembles possibles de X 
	for sub in subsets_x:
		if((test_AC1(sub,fact,M,u) and (test_AC2(sub,M,u)):
			return False	
	return True



def test_CC2(x,foil,M,u):
	return check_not(foil,M,u)	
	
