import time
import random
import pandas as pd
from queue import Queue
nodes={0: [1, 49, 45], 1: [2, 0, 6], 2: [3, 1, 49], 3: [4, 2, 7], 4: [5, 3, 9], 5: [6, 4, 8], 6: [7, 5, 1], 7: [8, 6, 3], 8: [9, 7, 5], 9: [10, 8, 4], 10: [11, 9, 12], 11: [12, 10], 12: [13, 11, 10], 13: [14, 12, 18], 14: [15, 13, 16], 15: [16, 14, 20], 16: [17, 15, 14], 17: [18, 16, 22], 18: [19, 17, 13], 19: [20, 18, 21], 20: [21, 19, 15], 21: [22, 20, 19], 22: [23, 21, 17], 23: [24, 22, 25], 24: [25, 23, 27], 25: [26, 24, 23], 26: [27, 25, 31], 27: [28, 26, 24], 28: [29, 27, 30], 29: [30, 28, 32], 30: [31, 29, 28], 31: [32, 30, 26], 32: [33, 31, 29], 33: [34, 32, 36], 34: [35, 33], 35: [36, 34, 38], 36: [37, 35, 33], 37: [38, 36, 42], 38: [39, 37, 35], 39: [40, 38, 41], 40: [41, 39], 41: [42, 40, 39], 42: [43, 41, 37], 43: [44, 42, 46], 44: [45, 43, 48], 45: [46, 44, 0], 46: [47, 45, 43], 47: [48, 46], 48: [49, 47, 44], 49: [0, 48, 2]}

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
#updates the probablity data for predator
def predator_move_update(predator_belief):
    predator_belief_new=[0]*50
    for i in range(len(predator_belief)):
        nodes_affecting=nodes[i]
        for j in nodes_affecting:
            degree_of_j=len(nodes[j])
            predator_belief_new[i]=predator_belief_new[i]+ ((predator_belief[j]/degree_of_j)*0.4)
            
        nodes_affecting=nodes[i]
        for j in nodes_affecting:
            distance=[]
            j_neighbors=nodes[j]
            for node in j_neighbors:
                distance.append(len(shortest_path(node,agent)))
            best_neighbor=[]
            for k in range(len(distance)):
                if distance[k]==min(distance):
                    best_neighbor.append(j_neighbors[k])
            if i in best_neighbor:
                predator_belief_new[i]=predator_belief_new[i]+ ((predator_belief[j]/len(best_neighbor))*0.6)
    return predator_belief_new

#updates probablity after a negative survey
def survey_update(belief,prediction): 
    survey_not_prob=1-belief[prediction]
    belief[prediction]=0
    for i in range(len(belief)):
            belief[i]=belief[i]/survey_not_prob
    return belief


#################################################
#################### AGENTS #####################
#################################################

def agent1(nodes,prey,predator,agent):
    run=True
    m=0
    while run==True:
        m=m+1
        if m>5000:
            return "out of moves"
        c_prey_dist=len(shortest_path(agent,prey))
        c_predator_dist=len(shortest_path(agent,predator))
        neighbor_nodes=nodes[agent]
        node_viability=[]
        for nn in neighbor_nodes:
            prey_dist=len(shortest_path(nn,prey))
            predator_dist=len(shortest_path(nn,predator))
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
            agent=random.choice(good_nn)
        if(predator==agent):
            return "Death",m
        if(prey==agent):
            return "success",m
        prey=move_prey(prey)
        if(prey==agent):
            return "success",m
        predator=move_predator(predator,agent)
        if(predator==agent):
            return "Death",m

def agent2(nodes,prey,predator,agent):
    run=True
    m=0
    while run==True:
        m=m+1
        if m>5000:
            return "out of moves"

        c_prey_dist=len(shortest_path(agent,prey))
        c_predator_dist=len(shortest_path(agent,predator))
        #predict based on future location of prey
        prey_prediction=prey
        prey_after_x_moves=[0]*50
        prey_after_x_moves[prey]=1
        for i in range(int(c_prey_dist/2)):
            prey_after_x_moves=prey_move_update(prey_after_x_moves)
        max_prey_beliefs=[]
        for i in range(len(prey_after_x_moves)):
            if prey_after_x_moves[i]==max(prey_after_x_moves):
                max_prey_beliefs.append(i)
        prey_prediction=random.choice(max_prey_beliefs)

        neighbor_nodes=nodes[agent]
        node_viability=[]
        for nn in neighbor_nodes:
            prey_dist=len(shortest_path(nn,prey_prediction))
            predator_dist=len(shortest_path(nn,predator))
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
            agent=random.choice(good_nn)

        if(predator==agent):
            return "Death",m

        if(prey==agent):
            return "success",m

        prey=move_prey(prey)
        if(prey==agent):
            return "success",m

        predator=move_predator(predator,agent)
        if(predator==agent):
            return "Death",m

def agent3(nodes,prey,predator,agent):
    run=True
    m=1
    prey_belief=[1/49]*50
    prey_belief[agent]=0
    prey_caught=0
    while run==True:
        m=m+1
        if m>5000:
            return "out of moves"
        
        max_prey_beliefs=[]
        for i in range(len(prey_belief)):
            if prey_belief[i]==max(prey_belief):
                max_prey_beliefs.append(i)
        prey_prediction=random.choice(max_prey_beliefs)

        if prey_prediction==prey:
            prey_belief=[0]*50
            prey_caught+=1
            prey_belief[prey_prediction]=1
        else:
            prey_belief=survey_update(prey_belief,prey_prediction)

        max_prey_beliefs=[]
        for i in range(len(prey_belief)):
            if prey_belief[i]==max(prey_belief):
                max_prey_beliefs.append(i)
        prey_prediction=random.choice(max_prey_beliefs)

        c_prey_dist=len(shortest_path(agent,prey_prediction))
        c_predator_dist=len(shortest_path(agent,predator))
        neighbor_nodes=nodes[agent]
        node_viability=[]
        for nn in neighbor_nodes:
            prey_dist=len(shortest_path(nn,prey_prediction))
            predator_dist=len(shortest_path(nn,predator))
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
            agent=random.choice(good_nn)
        
        if(predator==agent):
            return "Death",prey_caught
        if(prey==agent):
            return "success",prey_caught

        prey_belief=survey_update(prey_belief,agent)

        predator=move_predator(predator,agent)
        if(predator==agent):
            return "Death",prey_caught

        prey=move_prey(prey)
        if(prey==agent):
            return "success",prey_caught

        prey_belief=prey_move_update(prey_belief)
        prey_belief=survey_update(prey_belief,agent)

def agent4(nodes,prey,predator,agent):
    run=True
    m=1
    prey_belief=[1/49]*50
    prey_belief[agent]=0
    prey_caught=0
    # print(prey_belief)
    # print(sum(prey_belief))
    while run==True:
        m=m+1
        if m>5000:
            return "out of moves"

        # print("1 ",predator,prey,agent)
        prey_belief=prey_move_update(prey_belief)
        # print(prey_belief)
        # print(sum(prey_belief))

        #####Find max of the beliefs
        max_prey_beliefs=[]
        for i in range(len(prey_belief)):
            if prey_belief[i]==max(prey_belief):
                max_prey_beliefs.append(i)
        prey_prediction=random.choice(max_prey_beliefs)
        # print(prey_prediction)
        #####SURVEY THE MAX
        if prey_prediction==prey:
            prey_belief=[0]*50
            prey_caught+=1
            prey_belief[prey_prediction]=1
        else:
            prey_belief=survey_update(prey_belief,prey_prediction)

        # print(prey_belief)
        # print(sum(prey_belief))

        #####Find max of the beliefs
        max_prey_beliefs=[]
        for i in range(len(prey_belief)):
            if prey_belief[i]==max(prey_belief):
                max_prey_beliefs.append(i)
        prey_prediction=random.choice(max_prey_beliefs)

        c_prey_dist=len(shortest_path(agent,prey_prediction))
        c_predator_dist=len(shortest_path(agent,predator))
        # print(c_predator_dist,c_prey_dist)
        neighbor_nodes=nodes[agent]
        node_viability=[]
        # print(neighbor_nodes)
        for nn in neighbor_nodes:
            prey_dist=len(shortest_path(nn,prey_prediction))
            predator_dist=len(shortest_path(nn,predator))
            # print(predator_dist,prey_dist)
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
        # print("node",node_viability)
        if min(node_viability)!=7:
            good_nn=[]
            for n in range(len(node_viability)):
                if node_viability[n]==min(node_viability):
                    good_nn.append(neighbor_nodes[n])
            agent=random.choice(good_nn)
        # print("2 ",predator,prey,agent)

        if(predator==agent):
            return "Death",m
            run=False
        if(prey==agent):
            return "success",m
            run=False
        
        prey_belief=survey_update(prey_belief,agent)

        predator=move_predator(predator,agent)
        # print("3 ",predator,prey,agent)
        if(predator==agent):
            return "Death",m
            run=False

        prey=move_prey(prey)
        if(prey==agent):
            return "success",m
            run=False



#####################################################
#### CALLING AGENT FUNCTIONS FOR MULTIPLE GRAPHS ####
#####################################################

t1=time.time()
data_export=[]
win=0
mean_move=0
predator,prey,agent=create_entity()
data_export=[]
for a in range(50):
    for p in range(50):
        print(a,p)
        predator,prey,agent=create_entity()
        predator=p
        agent=a
        move_count=[]
        for i in range(200):
            win_loss,moves=agent4(nodes,prey,predator,agent)  ####call specific agent, Make vary of the parameters the functions returns and store them accordingly
            if win_loss=="success":
                move_count.append(moves)
            if len(move_count)==100:
                break
        move_count=sorted(move_count)
        if len(move_count)==100:
            u=sum(move_count[0:20])/20
            data_export.append([(a,p),u])
logdf = pd.DataFrame(data_export)
logdf.to_excel('bonus_partial_utilities.xlsx')
print(time.time()-t1)
