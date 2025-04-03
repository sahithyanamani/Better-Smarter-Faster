import pandas as pd
import random
from queue import Queue
#Function to generalize and count success rate for each ghost level
ds = pd.read_excel("utilitiesold.xlsx")

x = ds.iloc[:,2].values
key_state = list(x)#[:10]

x = ds.iloc[:,4].values
next_move=list(x)

res = dict(zip(key_state, next_move))


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




def agentU_star():
    m=0
    predator,prey,agent=create_entity()
    agentU=agent1=agent2=agent
    PU=P1=P2=predator
    pathU=[agent]
    path1=[agent]
    path2=[agent]
    pathprey=[prey]
    pathpredU=[PU]
    pathpred1=[P1]
    pathpred2=[P2]
    cu=c1=c2=0
    while cu==0 or c1==0 or c2==0:
        m=m+1
        if m>5000:
            return 0,m
            #print("out of moves")
        
        agentU=res[str((agentU,prey,PU))]
        pathU.append(agentU)
        ###Agent 1
        c_prey_dist=len(shortest_path(agent1,prey))
        c_predator_dist=len(shortest_path(agent1,P1))
        neighbor_nodes=nodes[agent1]
        node_viability=[]
        for nn in neighbor_nodes:
            prey_dist=len(shortest_path(nn,prey))
            predator_dist=len(shortest_path(nn,P1))
            if prey_dist<c_prey_dist and predator_dist>c_predator_dist:
                node_viability.append(1)
            elif prey_dist<c_prey_dist and predator_dist==c_predator_dist:
                node_viability.append(2)
            elif prey_dist==c_prey_dist and predator_dist>c_predator_dist:
                node_viability.append(3)
            elif prey_dist==c_prey_dist and predator_dist==c_predator_dist:
                node_viability.append(4)
            elif predator_dist>c_predator_dist:
                node_viability.append(5)
            elif predator_dist==c_predator_dist:
                node_viability.append(6)
            else:
                node_viability.append(7)
        if min(node_viability)!=7:
            good_nn=[]
            for n in range(len(node_viability)):
                if node_viability[n]==min(node_viability):
                    good_nn.append(neighbor_nodes[n])
            agent1=random.choice(good_nn)
        path1.append(agent1)


        #Agent2
        c_prey_dist=len(shortest_path(agent2,prey))
        c_predator_dist=len(shortest_path(agent2,P2))
        #predict based on future location of prey
        
        neighbor_nodes=nodes[agent2]
        node_viability=[]
        for nn in neighbor_nodes:
            prey_dist=len(shortest_path(nn,prey))
            predator_dist=len(shortest_path(nn,P2))
            if c_prey_dist<c_predator_dist:
                if prey_dist<c_prey_dist and predator_dist>c_predator_dist:
                    node_viability.append(1)
                elif prey_dist<c_prey_dist and predator_dist==c_predator_dist:
                    node_viability.append(2)
                elif prey_dist==c_prey_dist and predator_dist>c_predator_dist:
                    node_viability.append(3)
                elif prey_dist==c_prey_dist and predator_dist==c_predator_dist:
                    node_viability.append(4)
                elif predator_dist>c_predator_dist:
                    node_viability.append(5)
                elif predator_dist==c_predator_dist:
                    node_viability.append(6)
                else:
                    node_viability.append(7)
            else:
                if prey_dist<c_prey_dist and predator_dist>c_predator_dist:
                    node_viability.append(1)
                elif prey_dist==c_prey_dist and predator_dist>c_predator_dist:
                    node_viability.append(2)
                elif prey_dist>c_prey_dist and predator_dist>c_predator_dist:
                    node_viability.append(3)
                elif prey_dist<c_prey_dist and predator_dist==c_predator_dist:
                    node_viability.append(4)
                elif prey_dist==c_prey_dist and predator_dist==c_predator_dist:
                    node_viability.append(5)
                elif prey_dist>c_prey_dist and predator_dist==c_predator_dist:
                    node_viability.append(6)
                else:
                    node_viability.append(7)

        if min(node_viability)!=7:
            good_nn=[]
            for n in range(len(node_viability)):
                if node_viability[n]==min(node_viability):
                    good_nn.append(neighbor_nodes[n])
            agent2=random.choice(good_nn)
        path2.append(agent2)




        if cu==0:
            if(PU==agentU):
                print("deathu")
                cu=1
                # return 0,m
            if(prey==agentU):
                print("agentU")
                print(pathU)
                print(pathprey)
                print(pathpredU)
                cu=1
                # return 1,m
        if c1==0:
            if(P1==agent1):
                print("death1")
                c1=1
                # return 0,m
            if(prey==agent1):
                print("agent1")
                print(path1)
                print(pathprey)
                print(pathpred1)
                c1=1
                # return 1,m
        if c2==0:
            if(P2==agent2):
                print("death2")
                c2=1
                # return 0,m
            if(prey==agent2):
                print("agent2")
                print(path2)
                print(pathprey)
                print(pathpred2)
                c2=1
                # return 1,m




        prey=move_prey(prey)
        pathprey.append(prey)

        if cu==0:
            if(PU==agentU):
                print("deathu")
                cu=1
                # return 0,m
            if(prey==agentU):
                print("agentU")
                print(pathU)
                print(pathprey)
                print(pathpredU)
                cu=1
                # return 1,m
        if c1==0:
            if(P1==agent1):
                print("death1")
                c1=1
                # return 0,m
            if(prey==agent1):
                print("agent1")
                print(path1)
                print(pathprey)
                print(pathpred1)
                c1=1
                # return 1,m
        if c2==0:
            if(P2==agent2):
                print("death2")
                c2=1
                # return 0,m
            if(prey==agent2):
                print("agent2")
                print(path2)
                print(pathprey)
                print(pathpred2)
                c2=1
                # return 1,m




        PU=move_predator(PU,agentU)
        pathpredU.append(PU)
        P1=move_predator(P1,agent1)
        pathpred1.append(P1)
        P2=move_predator(P2,agent2)
        pathpred2.append(P2)
        if cu==0:
            if(PU==agentU):
                print("deathu")
                cu=1
                # return 0,m
            if(prey==agentU):
                print("agentU")
                print(pathU)
                print(pathprey)
                print(pathpredU)
                cu=1
                # return 1,m
        if c1==0:
            if(P1==agent1):
                print("death1")
                c1=1
                # return 0,m
            if(prey==agent1):
                print("agent1")
                print(path1)
                print(pathprey)
                print(pathpred1)
                c1=1
                # return 1,m
        if c2==0:
            if(P2==agent2):
                print("death2")
                c2=1
                # return 0,m
            if(prey==agent2):
                print("agent2")
                print(path2)
                print(pathprey)
                print(pathpred2)
                c2=1
                # return 1,m
t=0
move=0
for i in range(1):
    print(i)
    agentU_star()

print(t)
# print(move/3000)
