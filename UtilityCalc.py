import time
import json
import random
import pandas as pd
from queue import Queue
nodes={}
#################################################
################ GRAPH CREATION #################
#################################################
#Get node neighbor at distance 5 and remove immediate neighbors and those with degree 3
def get_5_around(n,nodes):
    neighbor=list(range(n-5,n+6))
    neighbor.remove(n-1)
    neighbor.remove(n)
    neighbor.remove(n+1)
    for i in range(len(neighbor)):
        if neighbor[i]>49:
            neighbor[i]=neighbor[i]-50
        elif neighbor[i]<0:
            neighbor[i]=neighbor[i]+50
    temp_neighbor=neighbor.copy()
    for i in range(len(neighbor)):
        if len(nodes[neighbor[i]])>2:
            temp_neighbor.remove(neighbor[i])
    if len(temp_neighbor)>0:
        return random.choice(temp_neighbor)
    else:
        return n
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
#create the environment using dictionary with key as a node and value as list of nodes that node is connected to
def create_graph():
    nodes ={}
    for i in range(50):
        nodes[i]=[i+1,i-1]
    nodes[0]=[1,49]
    nodes[49]=[0,48]

    node_degree=list(range(50))
    while len(node_degree)>0:
        current=random.choice(node_degree)
        next=get_5_around(current,nodes)
        if next!=current:
            nodes[current]=nodes[current]+[next]
            nodes[next]=nodes[next]+[current]
        node_degree.remove(current)
        if next in node_degree:
            node_degree.remove(next)

    predator,prey,agent=create_entity()

    return nodes,predator,prey,agent

#################################################
###########MOVEMENTS and BELIEF UPDATES##########
#################################################
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
#updates the probablity data for prey
def prey_move_update(prey_belief):
    prey_belief_new=[0]*50
    for i in range(len(prey_belief)):
        nodes_affecting=nodes[i]+[i]
        for j in nodes_affecting:
            degree_of_j=len(nodes[j])+1
            prey_belief_new[i]=prey_belief_new[i]+ (prey_belief[j]/degree_of_j)
    return prey_belief_new
#updates probablity after a negative survey
def survey_update(belief,prediction): 
    survey_not_prob=1-belief[prediction]
    belief[prediction]=0
    for i in range(len(belief)):
            belief[i]=belief[i]/survey_not_prob
    return belief

state_dict={}
converge_flag=0
t1=time.time()

# nodes,predator,prey,agent=create_graph()
nodes={0: [1, 49, 45], 1: [2, 0, 6], 2: [3, 1, 49], 3: [4, 2, 7], 4: [5, 3, 9], 5: [6, 4, 8], 6: [7, 5, 1], 7: [8, 6, 3], 8: [9, 7, 5], 9: [10, 8, 4], 10: [11, 9, 12], 11: [12, 10], 12: [13, 11, 10], 13: [14, 12, 18], 14: [15, 13, 16], 15: [16, 14, 20], 16: [17, 15, 14], 17: [18, 16, 22], 18: [19, 17, 13], 19: [20, 18, 21], 20: [21, 19, 15], 21: [22, 20, 19], 22: [23, 21, 17], 23: [24, 22, 25], 24: [25, 23, 27], 25: [26, 24, 23], 26: [27, 25, 31], 27: [28, 26, 24], 28: [29, 27, 30], 29: [30, 28, 32], 30: [31, 29, 28], 31: [32, 30, 26], 32: [33, 31, 29], 33: [34, 32, 36], 34: [35, 33], 35: [36, 34, 38], 36: [37, 35, 33], 37: [38, 36, 42], 38: [39, 37, 35], 39: [40, 38, 41], 40: [41, 39], 41: [42, 40, 39], 42: [43, 41, 37], 43: [44, 42, 46], 44: [45, 43, 48], 45: [46, 44, 0], 46: [47, 45, 43], 47: [48, 46], 48: [49, 47, 44], 49: [0, 48, 2]}
predator,prey,agent=create_entity()

for a1 in range(50):
    for prey in range(50):
        for pred in range(50):
            if a1==pred:
                state_dict[(a1,prey,pred)]=10000000
            else:
                state_dict[(a1,prey,pred)]=len(shortest_path(a1,prey))-1

temp_state_dict=state_dict.copy()
temp_state=state_dict.copy()
data_export=[list(state_dict.values())]

def comp_utility(state):
    u=[]
    global temp_state_dict
    agent=state[0]
    prey=state[1]
    predator=state[2]
    prey_prob=(1/(1+len(nodes[prey])))
    for i in nodes[agent]+[agent]:
        ui=1#temp_state[(i,prey,predator)]/2
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
                ui=ui+(temp_state_dict[(i,j,k)]*prey_prob*pred_prob)
        u.append(ui)
    action=nodes[agent]+[agent]
    minu=[]
    for i in range(len(u)):
        if u[i]==min(u):
            minu.append(i)
    select=random.choice(minu)
    return u[select], action[select]

best_pos=state_dict.copy()
while converge_flag<125000:
    converge_flag=0
    temp_state_dict=state_dict.copy()
    for i in state_dict.keys():
        temp=state_dict[i]
        if state_dict[i] not in [0,10000000]:
            state_dict[i],best_pos[i]=comp_utility(i)
        if abs(temp-state_dict[i])<0.001:
            converge_flag+=1
            best_pos[i]="done"
    print(converge_flag)

data_export=data_export+[list(state_dict.keys()), list(state_dict.values()), list(best_pos.values())]
logdf = pd.DataFrame(data_export)
logdf = logdf.transpose()
logdf.to_excel('utilities.xlsx')
# print(data_export)

print(time.time()-t1)
