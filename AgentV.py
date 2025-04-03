import pandas as pd
import numpy as np
import random
from queue import Queue

ds = pd.read_excel("ModelVloopup.xlsx")

x = ds.iloc[:,1].values
key_state = list(x)#[:10]

x = ds.iloc[:,2].values
next_move=list(x)

res = dict(zip(key_state, next_move))

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

weight1=[[0.19111269, -0.70236007, -1.17309019, -0.55263379, -1.66711356],
        [-1.65611119, -0.81389674, -1.18953741, 0.94948687, -0.06735042],
        [-1.21159974, -0.03225222, 0.608634, 0.61535635, 1.60220942],
        [-0.81441084, 1.27417325, -0.38540838, 0.09804544, -0.8551972 ]]
weight12=[[-1.03777132, 1.81628364, 1.89130175, 0.2956065, 0.83446512],
        [ 0.21754178, 1.57475417, -1.78049239, 1.62723804,-1.67751909],
        [ 1.59983479, 2.13676209, -1.25270013, -0.70966023, -0.01142294],
        [ 0.84134238, -2.19991635, -0.15352855, 0.67768466, 0.78659198],
        [ 0.65231115, -0.4720582, -0.40754716, -0.56176415, 2.53029285]]
weight2=[[-1.28889202],
        [ 0.40175152],
        [ 0.30124234],
        [ 0.50488661],
        [-0.47137889]]


#BFS to return the shortest path between 2 nodes
def shortest_path(start,end):
    if start==end:
        return [start]
    run=True
    PQ = Queue()
    PQ.put(start)
    came_from = {}
    v=["nv"]*50
    v[start]="v"
    while run:
        current = PQ.get()
        for neighbor in nodes[current]:
            if v[neighbor]=="nv":
                v[neighbor]="v"
                came_from[neighbor] = current
                if neighbor != end:
                    PQ.put(neighbor)
                else:
                    run=False
                    break
    path=[end]
    while end in came_from:
        end = came_from[end]
        path.append(end)
    path=path[::-1]

    return path
#randomly generate the 3 entities
def create_entity():
    l=list(range(50))
    prey=random.choice(l)
    predator=random.choice(l)
    l.remove(prey)
    if prey!= predator:
        l.remove(predator)
    agent=random.choice(l)
    return predator,prey,agent
#returns a new position of the prey after it moves following it's movement pattern
def move_prey(prey):
    return random.choice(nodes[prey]+[prey])
#returns a new position of the predator after it moves following it's movement pattern
def move_predator(predator,agent):
    if random.choice(range(10))<4:
        return random.choice(nodes[predator])
    else:
        predator_neighbors=nodes[predator]
        distance=[]
        for node in predator_neighbors:
            distance.append(len(shortest_path(node,agent)))
        best_neighbor=[]
        for i in range(len(distance)):
            if distance[i]==min(distance):
                best_neighbor.append(predator_neighbors[i])
        return random.choice(best_neighbor)

nodes={0: [1, 49, 45], 1: [2, 0, 6], 2: [3, 1, 49], 3: [4, 2, 7], 4: [5, 3, 9], 5: [6, 4, 8], 6: [7, 5, 1], 7: [8, 6, 3], 8: [9, 7, 5], 9: [10, 8, 4], 10: [11, 9, 12], 11: [12, 10], 12: [13, 11, 10], 13: [14, 12, 18], 14: [15, 13, 16], 15: [16, 14, 20], 16: [17, 15, 14], 17: [18, 16, 22], 18: [19, 17, 13], 19: [20, 18, 21], 20: [21, 19, 15], 21: [22, 20, 19], 22: [23, 21, 17], 23: [24, 22, 25], 24: [25, 23, 27], 25: [26, 24, 23], 26: [27, 25, 31], 27: [28, 26, 24], 28: [29, 27, 30], 29: [30, 28, 32], 30: [31, 29, 28], 31: [32, 30, 26], 32: [33, 31, 29], 33: [34, 32, 36], 34: [35, 33], 35: [36, 34, 38], 36: [37, 35, 33], 37: [38, 36, 42], 38: [39, 37, 35], 39: [40, 38, 41], 40: [41, 39], 41: [42, 40, 39], 42: [43, 41, 37], 43: [44, 42, 46], 44: [45, 43, 48], 45: [46, 44, 0], 46: [47, 45, 43], 47: [48, 46], 48: [49, 47, 44], 49: [0, 48, 2]}
predator,prey,agent=create_entity()

def generate_U(agent,prey,predator):
    if (agent,prey,predator) in res.keys():
        return res[(agent,prey,predator)]
    else:
        inp=[len(shortest_path(agent,prey))-1,len(shortest_path(agent,predator))-1,len(shortest_path(prey,predator))-1,1]
        l = np.dot(inp, weight1) 
        l2 = sigmoid(l) 
        l3 = np.dot(l2, weight12) 
        l4 = sigmoid(l3)
        l5 = np.dot(l4, weight2)
        output = sigmoid(l5)
        return output*17

# ds = pd.read_excel("utilitiesold.xlsx")

# x = ds.iloc[:,2].values
# key_stateV = list(x)#[:10]

# x = ds.iloc[:,3].values
# UtilityV=list(x)

# resV = dict(zip(key_stateV, UtilityV))

# err=[]
# for i in range(50):
#     for j in range(50):
#         for k in range(50):
#             err.append(abs(resV[str((i,j,k))]-generate_U(i,j,k)))

# print(sum(err)/len(err))

def find_Vmodel_action(agent,prey,predator):
    u=[]
    prey_prob=(1/(1+len(nodes[prey])))
    for i in nodes[agent]+[agent]:
        ui=0
        if i==prey:
            ui=1
            u.append(ui)
            continue
        if i==predator:
            ui=10000000
            u.append(ui)
            continue
        pred_dist=[]
        for p in nodes[predator]:
            pred_dist.append(len(shortest_path(p,i)))
        min_pred_dist=min(pred_dist)
        close_nodes=pred_dist.count(min_pred_dist)
        for j in nodes[prey]+[prey]:
            for k in nodes[predator]:
                if len(shortest_path(i,k))==min_pred_dist:
                    pred_prob=(0.6*(1/close_nodes))+(0.4*(1/len(nodes[predator])))
                else:
                    pred_prob=0.4*(1/len(nodes[predator]))
                ui=ui+(generate_U(i,j,k)[0]*prey_prob*pred_prob)
        u.append(ui)
    action=nodes[agent]+[agent]
    minu=[]
    for i in range(len(u)):
        if u[i]==min(u):
            minu.append(i)
    select=random.choice(minu)
    return action[select]
    # return action[u.index(min(u))]



def agentV_star():
    m=0
    predator,prey,agent=create_entity()
    while True:
        m=m+1
        if m>5000:
            return 0,m
            #print("out of moves")
        agent=find_Vmodel_action(agent,prey,predator)
        if(prey==agent):
            return 1,m
        if(predator==agent):
            return 0,m
        prey=move_prey(prey)
        if(prey==agent):
            return 1,m
        predator=move_predator(predator,agent)
        if(predator==agent):
            return 0,m

t=0
move=0
for i in range(3000):
    print(i)
    r,m=agentV_star()
    move+=m
    t+=r
print(t/30)
print(move/3000)
