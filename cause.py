#### Draft

from this import d

from numpy import character

catalog = dict()    #weight length width height price wheels
catalog["Twingo"] = (1000, 3.6, 1.6, 1.5, 15000,4)

def classifier_vehicule(u): #decomposer en une  fonction extractrice de features + fonctions de calculs de variable endogene + vrai classifier.
    charac = catalog[u]
    weight = charac[0]
    length = charac[1]
    width = charac[2]
    height = charac[3]
    price = charac[4]
    wheels = charac[5]
    
    if wheels == 2:
        if weight > 150:
            return "Moto"
        else:
            return "Scooter"

    if wheels == 4:
        if weight > 3000:
            return "Tractor"
        else:
            return "Voiture"
    
    if wheels > 4:
        if length < 30:
            return "Truck"
        else:
            return "Train"

    if wheels == 0:
        if price < 1e+7:
            return "Cruise Ship"
        else:
            return "Boat"
    if (0.5<(length/width)) and ((length/width) <2):
        return "Plane"

    return "Unknown"

        





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

def test_CC1(X,fact,M,u):
    """
    dict * dict * causal model * dict -> bool
    Return True if CC1 is respected (see p.10), False otherwise
    """
    f = fact.items()
    for x in X.items():
        if x not in f:
            return False
    return True

def test_CC2(foil,M,u):
    pass

def test_CC3():
    pass

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

def test_counterfactual_cause(x, y, fact, foil, M,u):
    """
    dict**4 * causal model * dict -> bool
    Return True if <x,y> is a contrastive counterfactual actual cause
    (= counterfactual cause) of <fact,foil>, False otherwise
    """
    a = test_CC1(x,fact,M, u)
    a = a and test_CC2(foil,M, u)
    a = a and test_CC3(y,foil,M,u)
    a = a and test_CC4(x,y)
    a = a and test_CC5()
    return a
