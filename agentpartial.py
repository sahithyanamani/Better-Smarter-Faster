import pandas as pd
import random
from queue import Queue
#Function to generalize and count success rate for each ghost level
ds = pd.read_excel("utilitiesold.xlsx")

x = ds.iloc[:,2].values
key_state = list(x)#[:10]

x = ds.iloc[:,3].values
utility = list(x)#[:10]

x = ds.iloc[:,4].values
next_move=list(x)

res = dict(zip(key_state, next_move))
key_utility = dict(zip(key_state, utility))

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



nodes={0: [1, 49, 45], 1: [2, 0, 6], 2: [3, 1, 49], 3: [4, 2, 7], 4: [5, 3, 9], 5: [6, 4, 8], 6: [7, 5, 1], 7: [8, 6, 3], 8: [9, 7, 5], 9: [10, 8, 4], 10: [11, 9, 12], 11: [12, 10], 12: [13, 11, 10], 13: [14, 12, 18], 14: [15, 13, 16], 15: [16, 14, 20], 16: [17, 15, 14], 17: [18, 16, 22], 18: [19, 17, 13], 19: [20, 18, 21], 20: [21, 19, 15], 21: [22, 20, 19], 22: [23, 21, 17], 23: [24, 22, 25], 24: [25, 23, 27], 25: [26, 24, 23], 26: [27, 25, 31], 27: [28, 26, 24], 28: [29, 27, 30], 29: [30, 28, 32], 30: [31, 29, 28], 31: [32, 30, 26], 32: [33, 31, 29], 33: [34, 32, 36], 34: [35, 33], 35: [36, 34, 38], 36: [37, 35, 33], 37: [38, 36, 42], 38: [39, 37, 35], 39: [40, 38, 41], 40: [41, 39], 41: [42, 40, 39], 42: [43, 41, 37], 43: [44, 42, 46], 44: [45, 43, 48], 45: [46, 44, 0], 46: [47, 45, 43], 47: [48, 46], 48: [49, 47, 44], 49: [0, 48, 2]}
predator,prey,agent=create_entity()
data_export=[]
key_partial_U={}

def find_U_parital(prey_belief,agent,pred):
    key_partialU_Local={}
    for i in nodes[agent]+[agent]:#range(50):
        for j in nodes[pred]:#range(50):
            ui=0
            for k in range(50):
                ui=ui+(prey_belief[k]*key_utility[str((i,k,j))])
            key_partialU_Local[str((i,j))]=ui
    return key_partialU_Local
#print(key_partial_U)

def agent_partial_U():
    m=0
    global data_export
    predator,prey,agent=create_entity()
    prey_belief=[1/49]*50
    prey_belief[agent]=0
    while True:
        m=m+1
        if m>5000:
            return 0
            print("out of moves")
        max_prey_beliefs=[]
        for i in range(len(prey_belief)):
            if prey_belief[i]==max(prey_belief):
                max_prey_beliefs.append(i)
        prey_prediction=random.choice(max_prey_beliefs)

        if prey_prediction==prey:
            prey_belief=[0]*50
            # prey_caught+=1
            prey_belief[prey_prediction]=1
        else:
            prey_belief=survey_update(prey_belief,prey_prediction)
        
        u=[]

        key_partial_U=find_U_parital(prey_belief,agent,predator)
        for i in key_partial_U.keys(): #change for V Model Inputs
            data_export.append([i, key_partial_U[i],prey_belief]) #change for V Model Inputs
        
        for i in nodes[agent]+[agent]:
            if i==predator:
                ui=10000000
                u.append(ui)
                continue
            ui=0
            for j in nodes[predator]:
                ui+=key_partial_U[str((i,j))]
            u.append(ui)
        action=nodes[agent]+[agent]
        minu=[]
        for i in range(len(u)):
            if u[i]==min(u):
                minu.append(i)
        select=random.choice(minu)
        agent=action[select]

        if(prey==agent):
            return 1,m
        if(predator==agent):
            return 0,m

        prey_belief=survey_update(prey_belief,agent)
        prey=move_prey(prey)
        if(prey==agent):
            return 1,m
        predator=move_predator(predator,agent)
        if(predator==agent):
            return 0,m

        prey_belief=prey_move_update(prey_belief)
        prey_belief=survey_update(prey_belief,agent)

t=0
move=0
for i in range(3000):
    print(i)
    r,m=agent_partial_U()
    t+=r
    move+=m
print(t/30)
print(move/3000)


logdf = pd.DataFrame(data_export)
# logdf.to_excel('partial_utilities.xlsx')