#!/usr/bin/env python
# coding: utf-8

# In[9]:


from main import *

def c_weight_lbs(param):
    return round(param['Current_Weight']*2.205)

def p_weight_lbs(param):
    return round(param['Pre_Weight']*2.205)

def height_inches(param):
    return round(param['Height']/2.54)

def calc_IMC(param):
    return round((param['Current_Weight']/param['Height']**2)*10000)

def healthy_weight(param):
    return round(25*((param['Height_inches']*param['Height_inches'])/703))

def lbs_lost(param):
    if (param['Pre_weight_lbs'] - param['Current_weight_lbs'])<0:
        return 0
    return (param['Pre_weight_lbs'] - param['Current_weight_lbs'])
        

def excess_body_weight(param):
    if (param['Pre_weight_lbs'] - param['Healthy_weight'])<0:
        return 0
    return (param['Pre_weight_lbs'] - param['Healthy_weight'])

def percent_weight_loss(param):
    if(param['Excess_weight']<=0):
        return 100
    if(param['Number_lbs_lost']==0):
        return 0
    elif(param['Number_lbs_lost']>param['Excess_weight']):
        return 100
    return round((param['Number_lbs_lost']/param['Excess_weight'])*100)

def output(param):
    if (param['IMC']<18):
        res = 'Underweight'
    elif (param['IMC']>=18 and param['IMC']<25):
        res = 'Healthy weight'
    elif (param['IMC']>=25 and param['IMC']<30):
        res = 'Overweight'
    else :
        res = 'Obesity'
    if res=='Underweight':
        return (0,res)
    return (100-param['Percent_weight_loss'],res)

# Exogenous variables
U = {'Height':[50,55,60,65,70,75,80,85,90,95,100,105,110,120,125,130,135,140,145,150,               155,160,165,170,175,180,185,190,195,200],     'Current_Weight':[5,10,15,20,25,30,35,40,45,60,65,70,75,80,85,90,95,100,105,110,                      115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200],    'Pre_Weight':[5,10,15,20,25,30,35,40,45,60,65,70,75,80,85,90,95,100,105,110,115,                  120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200]}

# Endogenous variables
V = {'Height_inches':[2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 30.0, 32.5, 35.0, 37.5,                       40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0, 67.5, 70.0,                      72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0, 92.5, 95.0, 97.5, 100.0],     'Current_weight_lbs':[10, 20, 30, 40, 50, 60, 70, 80, 90, 120, 130, 140, 150, 160, 170, 180,                           190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320,                           330, 340, 350, 360, 370, 380, 390, 400],     'Pre_weight_lbs':[10, 20, 30, 40, 50, 60, 70, 80, 90, 120, 130, 140, 150, 160, 170, 180,                       190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320,                       330, 340, 350, 360, 370, 380, 390, 400],     'IMC':[0, 2, 4, 8, 12, 18, 24, 32, 40, 72, 84, 98, 112, 128, 144, 162, 180, 200, 220, 242,           264, 288, 312, 338, 364, 392, 420, 450, 480, 512, 544, 578, 612, 648, 684, 722, 760,           800, 7, 11, 16, 22, 29, 37, 65, 77, 89, 102, 116, 131, 147, 164, 182, 240, 262, 284,           307, 331, 356, 382, 409, 437, 465, 495, 525, 557, 589, 622, 656, 691, 727, 10, 15, 20,           27, 34, 60, 70, 82, 94, 107, 120, 135, 150, 167, 184, 202, 260, 282, 304, 327, 350, 375,           400, 427, 454, 482, 510, 540, 570, 602, 634, 667, 3, 6, 14, 19, 25, 31, 55, 75, 87, 111, 125,           139, 154, 170, 186, 203, 222, 280, 302, 323, 346, 370, 394, 419, 445, 471, 498, 527, 555, 585,           615, 1, 9, 13, 23, 51, 80, 91, 103, 129, 143, 158, 173, 189, 206, 223, 241, 300, 321, 343, 366,           389, 413, 438, 463, 489, 516, 543, 571, 5, 21, 48, 56, 85, 96, 108, 133, 161, 176, 192, 208, 225,           243, 261, 320, 341, 363, 385, 408, 432, 456, 481, 507, 533, 45, 53, 61, 90, 101, 113, 138, 151,           165, 195, 211, 228, 245, 263, 281, 340, 361, 383, 405, 428, 451, 475, 500, 42, 50, 58, 66, 95,            106, 118, 130, 142, 156, 169, 199, 214, 231, 247, 265, 283, 301, 360, 381, 403, 425, 447, 47, 54,           62, 71, 100, 122, 134, 160, 174, 188, 218, 234, 250, 267, 380, 401, 422, 444, 17, 38, 44, 52, 59,           67, 76, 105, 127, 152, 178, 221, 237, 253, 269, 287, 322, 421, 36, 49, 64, 81, 110, 121, 132, 196,           210, 256, 272, 289, 306, 324, 342, 69, 86, 115, 126, 137, 149, 187, 229, 244, 259, 275, 292, 309,           326, 344, 362, 33, 74, 166, 191, 205, 233, 248, 278, 295, 311, 328, 30, 35, 41, 68, 83, 92, 141,           163, 175, 213, 227, 255, 270, 285, 317, 333, 39, 88, 97, 146, 157, 168, 274, 28, 43, 93, 140, 185,           197, 209, 236, 249, 308, 145, 190, 254, 296, 26, 46, 79, 172, 183, 194, 219, 258, 286, 99, 117,           155, 177, 276, 104, 171, 193, 204, 216, 78, 109, 136, 198, 114, 181, 226, 238, 73, 119, 207, 230,           124, 201, 212, 224, 235, 57, 63, 217, 123, 148, 153],    'Number_lbs_lost':[0, 10, 20, 30, 40, 50, 60, 70, 80, 110, 100, 90, 120, 130, 140, 150, 160, 170, 180,                       190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350,                       360, 370, 380, 390],     'Healthy_weight':[22, 27, 32, 38, 44, 50, 57, 64, 72, 80, 89, 98, 108, 128, 139, 150, 162, 174, 187,                       200, 214, 228, 242, 257, 272, 288, 304, 321, 338, 356],     'Excess_weight':[0, 8, 3, 18, 13, 2, 28, 23, 12, 6, 38, 33, 22, 16, 10, 48, 43, 32, 26, 20, 58, 53,                      42, 36, 30, 68, 63, 52, 46, 40, 1, 98, 93, 88, 82, 76, 70, 56, 31, 108, 103, 92, 86,                      80, 73, 66, 50, 41, 118, 113, 102, 96, 90, 83, 60, 51, 128, 123, 112, 106, 100, 78,                       61, 11, 138, 133, 122, 116, 110, 71, 62, 21, 148, 143, 132, 126, 120, 81, 72, 158,                      153, 142, 136, 130, 91, 168, 163, 152, 146, 140, 101, 178, 173, 162, 156, 150, 111,                      188, 183, 172, 166, 160, 121, 198, 193, 182, 176, 170, 131, 208, 203, 192, 186, 180,                      141, 218, 213, 202, 196, 190, 151, 228, 223, 212, 206, 200, 161, 238, 233, 222, 216,                      210, 171, 248, 243, 232, 226, 220, 181, 258, 253, 242, 236, 230, 191, 268, 263, 252,                      246, 240, 201, 278, 273, 262, 256, 250, 211, 288, 283, 272, 266, 260, 221, 298, 293,                      282, 276, 270, 231, 308, 303, 292, 286, 280, 241, 9, 318, 313, 302, 296, 290, 251, 19,                      328, 323, 312, 306, 300, 261, 29, 338, 333, 322, 316, 310, 271, 39, 4, 348, 343, 332,                       326, 320, 281, 49, 14, 358, 353, 342, 336, 330, 291, 59, 24, 368, 363, 352, 346, 340,                      301, 69, 34, 378, 373, 362, 356, 350, 311, 79, 44],     'Percent_weight_loss':[100, 0, 56, 77, 36, 71, 43, 87, 83, 26, 53, 79, 30, 61, 91, 45, 62, 21, 42, 23,                             47, 70, 93, 31, 94, 38, 50, 17, 34, 52, 69, 86, 19, 57, 75, 24, 48, 95, 28, 33, 67,                            15, 29, 44, 59, 74, 88, 16, 32, 63, 58, 96, 22, 65, 25, 10, 20, 41, 51, 82, 92, 11,                            54, 97, 68, 80, 12, 37, 49, 73, 85, 98, 13, 39, 66, 14, 18, 89, 9, 46, 78, 76, 35,                            81, 27, 55, 40, 60, 8, 72, 84, 90, 64, 7, 99, 6, 5, 4, 3],     'Output':[(0, 'Underweight'), (100, 'Healthy weight'), (100, 'Obesity'), (100, 'Overweight'), (0, 'Healthy weight'), (0, 'Obesity'), (0, 'Overweight'), (56, 'Healthy weight'), (56, 'Obesity'), (56, 'Overweight'), (77, 'Healthy weight'), (77, 'Obesity'), (77, 'Overweight'), (36, 'Healthy weight'), (36, 'Obesity'), (36, 'Overweight'), (71, 'Healthy weight'), (71, 'Obesity'), (71, 'Overweight'), (43, 'Healthy weight'), (43, 'Obesity'), (43, 'Overweight'), (87, 'Healthy weight'), (87, 'Obesity'), (87, 'Overweight'), (83, 'Healthy weight'), (83, 'Obesity'), (83, 'Overweight'), (26, 'Healthy weight'), (26, 'Obesity'), (26, 'Overweight'), (53, 'Healthy weight'), (53, 'Obesity'), (53, 'Overweight'), (79, 'Healthy weight'), (79, 'Obesity'), (79, 'Overweight'), (30, 'Healthy weight'), (30, 'Obesity'), (30, 'Overweight'), (61, 'Healthy weight'), (61, 'Obesity'), (61, 'Overweight'), (91, 'Healthy weight'), (91, 'Obesity'), (91, 'Overweight'), (45, 'Healthy weight'), (45, 'Obesity'), (45, 'Overweight'), (62, 'Healthy weight'), (62, 'Obesity'), (62, 'Overweight'), (21, 'Healthy weight'), (21, 'Obesity'), (21, 'Overweight'), (42, 'Healthy weight'), (42, 'Obesity'), (42, 'Overweight'), (23, 'Healthy weight'), (23, 'Obesity'), (23, 'Overweight'), (47, 'Healthy weight'), (47, 'Obesity'), (47, 'Overweight'), (70, 'Healthy weight'), (70, 'Obesity'), (70, 'Overweight'), (93, 'Healthy weight'), (93, 'Obesity'), (93, 'Overweight'), (31, 'Healthy weight'), (31, 'Obesity'), (31, 'Overweight'), (94, 'Healthy weight'), (94, 'Obesity'), (94, 'Overweight'), (38, 'Healthy weight'), (38, 'Obesity'), (38, 'Overweight'), (50, 'Healthy weight'), (50, 'Obesity'), (50, 'Overweight'), (17, 'Healthy weight'), (17, 'Obesity'), (17, 'Overweight'), (34, 'Healthy weight'), (34, 'Obesity'), (34, 'Overweight'), (52, 'Healthy weight'), (52, 'Obesity'), (52, 'Overweight'), (69, 'Healthy weight'), (69, 'Obesity'), (69, 'Overweight'), (86, 'Healthy weight'), (86, 'Obesity'), (86, 'Overweight'), (19, 'Healthy weight'), (19, 'Obesity'), (19, 'Overweight'), (57, 'Healthy weight'), (57, 'Obesity'), (57, 'Overweight'), (75, 'Healthy weight'), (75, 'Obesity'), (75, 'Overweight'), (24, 'Healthy weight'), (24, 'Obesity'), (24, 'Overweight'), (48, 'Healthy weight'), (48, 'Obesity'), (48, 'Overweight'), (95, 'Healthy weight'), (95, 'Obesity'), (95, 'Overweight'), (28, 'Healthy weight'), (28, 'Obesity'), (28, 'Overweight'), (33, 'Healthy weight'), (33, 'Obesity'), (33, 'Overweight'), (67, 'Healthy weight'), (67, 'Obesity'), (67, 'Overweight'), (15, 'Healthy weight'), (15, 'Obesity'), (15, 'Overweight'), (29, 'Healthy weight'), (29, 'Obesity'), (29, 'Overweight'), (44, 'Healthy weight'), (44, 'Obesity'), (44, 'Overweight'), (59, 'Healthy weight'), (59, 'Obesity'), (59, 'Overweight'), (74, 'Healthy weight'), (74, 'Obesity'), (74, 'Overweight'), (88, 'Healthy weight'), (88, 'Obesity'), (88, 'Overweight'), (16, 'Healthy weight'), (16, 'Obesity'), (16, 'Overweight'), (32, 'Healthy weight'), (32, 'Obesity'), (32, 'Overweight'), (63, 'Healthy weight'), (63, 'Obesity'), (63, 'Overweight'), (58, 'Healthy weight'), (58, 'Obesity'), (58, 'Overweight'), (96, 'Healthy weight'), (96, 'Obesity'), (96, 'Overweight'), (22, 'Healthy weight'), (22, 'Obesity'), (22, 'Overweight'), (65, 'Healthy weight'), (65, 'Obesity'), (65, 'Overweight'), (25, 'Healthy weight'), (25, 'Obesity'), (25, 'Overweight'), (10, 'Healthy weight'), (10, 'Obesity'), (10, 'Overweight'), (20, 'Healthy weight'), (20, 'Obesity'), (20, 'Overweight'), (41, 'Healthy weight'), (41, 'Obesity'), (41, 'Overweight'), (51, 'Healthy weight'), (51, 'Obesity'), (51, 'Overweight'), (82, 'Healthy weight'), (82, 'Obesity'), (82, 'Overweight'), (92, 'Healthy weight'), (92, 'Obesity'), (92, 'Overweight'), (11, 'Healthy weight'), (11, 'Obesity'), (11, 'Overweight'), (54, 'Healthy weight'), (54, 'Obesity'), (54, 'Overweight'), (97, 'Healthy weight'), (97, 'Obesity'), (97, 'Overweight'), (68, 'Healthy weight'), (68, 'Obesity'), (68, 'Overweight'), (80, 'Healthy weight'), (80, 'Obesity'), (80, 'Overweight'), (12, 'Healthy weight'), (12, 'Obesity'), (12, 'Overweight'), (37, 'Healthy weight'), (37, 'Obesity'), (37, 'Overweight'), (49, 'Healthy weight'), (49, 'Obesity'), (49, 'Overweight'), (73, 'Healthy weight'), (73, 'Obesity'), (73, 'Overweight'), (85, 'Healthy weight'), (85, 'Obesity'), (85, 'Overweight'), (98, 'Healthy weight'), (98, 'Obesity'), (98, 'Overweight'), (13, 'Healthy weight'), (13, 'Obesity'), (13, 'Overweight'), (39, 'Healthy weight'), (39, 'Obesity'), (39, 'Overweight'), (66, 'Healthy weight'), (66, 'Obesity'), (66, 'Overweight'), (14, 'Healthy weight'), (14, 'Obesity'), (14, 'Overweight'), (18, 'Healthy weight'), (18, 'Obesity'), (18, 'Overweight'), (89, 'Healthy weight'), (89, 'Obesity'), (89, 'Overweight'), (9, 'Healthy weight'), (9, 'Obesity'), (9, 'Overweight'), (46, 'Healthy weight'), (46, 'Obesity'), (46, 'Overweight'), (78, 'Healthy weight'), (78, 'Obesity'), (78, 'Overweight'), (76, 'Healthy weight'), (76, 'Obesity'), (76, 'Overweight'), (35, 'Healthy weight'), (35, 'Obesity'), (35, 'Overweight'), (81, 'Healthy weight'), (81, 'Obesity'), (81, 'Overweight'), (27, 'Healthy weight'), (27, 'Obesity'), (27, 'Overweight'), (55, 'Healthy weight'), (55, 'Obesity'), (55, 'Overweight'), (40, 'Healthy weight'), (40, 'Obesity'), (40, 'Overweight'), (60, 'Healthy weight'), (60, 'Obesity'), (60, 'Overweight'), (8, 'Healthy weight'), (8, 'Obesity'), (8, 'Overweight'), (72, 'Healthy weight'), (72, 'Obesity'), (72, 'Overweight'), (84, 'Healthy weight'), (84, 'Obesity'), (84, 'Overweight'), (90, 'Healthy weight'), (90, 'Obesity'), (90, 'Overweight'), (64, 'Healthy weight'), (64, 'Obesity'), (64, 'Overweight'), (7, 'Healthy weight'), (7, 'Obesity'), (7, 'Overweight'), (99, 'Healthy weight'), (99, 'Obesity'), (99, 'Overweight'), (6, 'Healthy weight'), (6, 'Obesity'), (6, 'Overweight'), (5, 'Healthy weight'), (5, 'Obesity'), (5, 'Overweight'), (4, 'Healthy weight'), (4, 'Obesity'), (4, 'Overweight'), (3, 'Healthy weight'), (3, 'Obesity'), (3, 'Overweight')]
    }

# Parent node for each endogenous variable
P = {'Height_inches':(['Height'],height_inches),     'Current_weight_lbs':(['Current_Weight'],c_weight_lbs),     'Pre_weight_lbs':(['Pre_Weight'],p_weight_lbs),     'IMC':(['Height','Current_Weight'],calc_IMC),    'Number_lbs_lost':(['Current_weight_lbs','Pre_weight_lbs'],lbs_lost),     'Healthy_weight':(['Height_inches'],healthy_weight),     'Excess_weight':(['Pre_weight_lbs','Healthy_weight'],excess_body_weight),     'Percent_weight_loss':(['Excess_weight','Number_lbs_lost'],percent_weight_loss),    'Output':(['Percent_weight_loss','IMC'],output)}

C =  {'Height':['Height_inches','IMC'],     'Current_Weight':['Current_weight_lbs','IMC'],     'Pre_Weight':['Pre_weight_lbs'],     'Pre_weight_lbs':['Excess_weight','Number_lbs_lost'],     'Current_weight_lbs':['Number_lbs_lost'],     'Height_inches':['Healthy_weight'],    'Healthy_weight':['Excess_weight'],    'Number_lbs_lost':['Percent_weight_loss'],    'Percent_weight_loss':['Output'],    'IMC':['Output'],    'Excess_weight':['Percent_weight_loss']}

# Construction of situation (M,u)
Graph = CausalGraph(P,C)
Mod = Model(U,V,Graph)


# In[10]:


u = {'Height': 160,'Current_Weight':68,'Pre_Weight':120} #A charge le pistolet, B ne tire pas, C tire.
v = dict()

Sit = Situation(Mod,u,v)
Sit.reset_val_v()
print(value('Output',Sit)) #a cet instant on ne connait aucune valeurs des variables de V
                            #on calcule les valeurs des variables a partir des variables exogênes.
Sit.set_val_v()
print(Sit.v)


# In[11]:


fact = {'Output': (7, 'Overweight')}
foil = {'Output': (7, 'Obesity')}
print(check(fact,Sit))
print(check(foil,Sit))
print(check_not(fact,Sit))
print(check_not(foil,Sit))


# In[12]:


print(actual_cause_generator_v2(fact,Sit))


# In[ ]:


print(counterfactual_cause_generator(fact,foil,Sit))


# In[ ]:




