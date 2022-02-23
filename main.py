# classe M avec signature S (autre classe), F dictionnaire des fonctions, G graphe causal (utiliser une librairie ?)

class Signature():
    def __init__(U,V):
        self.U = U # set of exogenous variables
        self.V = V  # set of endogenous variables
        
class Model(Signature):
    def __init__(F,G):
        self.F = F # dict : variable -> function
        self.G = G # causal graph, node = (X,v)
        # ajouter u ?
        
def value(X,M,u):
    """
    Calculer la valeur de la variable X en fonction des autres variables
    """
    parents = dictionnaire des nœuds parent de X dans M.G
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

def test_CC2(x,foil,M,u):
    return check_not(foil,M,u)
