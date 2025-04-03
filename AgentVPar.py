import pandas as pd
import numpy as np
import random
from queue import Queue

ds = pd.read_excel("ModelVPartiallookup.xlsx")

x = ds.iloc[:, 1].values
key_state = list(x)  # [:10]

x = ds.iloc[:, 2].values
next_move = list(x)

res = dict(zip(key_state, next_move))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


weight1 = [[6.6789186, 7.21293345,  1.93184462, -2.78780733, -0.78283898],
           [-1.04394074,  0.85513568, -1.65430233, -0.27925756, -1.01752639],
           [1.14607142,  0.63285182, -0.69013486, -1.09591571, -0.47659213],
           [-0.1063429,  -1.68816343,  0.18076658,  0.02020222, -0.00828629],
           [-0.05099541, -0.62905126, -0.3899357,  -0.57013595,  0.51279321],
           [-1.46938611, -0.07733717,  1.18929085, -2.06862871,  1.30937672],
           [0.73579088,  0.20908729,  0.74740208, -0.04875522,  0.35971615],
           [0.62723303, -0.21845958, -1.6603869,  -1.31019794, -0.81645013],
           [1.44738252,  1.23387455,  0.24711952,  1.16451735,  0.01911806],
           [-2.14644507,  1.02646013,  1.36647664, -0.6485991,  -0.33894655],
           [-1.51386889,  0.43841481, -0.60569223, -0.29055928,  0.86453144],
           [0.01450907,  0.75153334, -1.64331151, -0.75601344,  0.85554191],
           [1.81584247,  0.01698685,  1.36674005,  1.29434621, -0.92930874],
           [-0.59282701,  0.59644539,  0.06932796, -2.96112473,  1.17942831],
           [0.82529842,  1.28273908, -0.02551626, -0.31505882,  1.02438124],
           [-0.01189821, -1.1428057,  -1.11389715, -0.37377446,  0.02808248],
           [-0.39089516, -0.91241617, -0.23031222,  1.02886658,  0.92737024],
           [0.58442393,  1.36364207,  0.11054275, -1.68122881,  0.54969425],
           [-0.7996939,   0.35374698, -1.74782285,  2.20883222, -0.18488508],
           [1.6761695,  -1.33403207, -0.27636001, -0.77555042,  0.31440005],
           [0.57893798, -1.36310022,  0.26395475,  1.90452109, -0.1108613],
           [-1.65388789, -0.23609723,  1.34629354,  1.46810567, -0.65278119],
           [-0.01817399, -0.76220944, -0.64954119, -0.41854943, -1.14153725],
           [-2.20370189,  0.06304628, -2.22355729, -0.48080832,  1.32647654],
           [0.10507727,  1.56264278, -0.90131532, -0.34110163, -0.11902488],
           [-0.20229314, -0.33937193,  0.77530771,  0.04390389, -1.61090624],
           [0.5313672,  -0.11102391,  0.61500684,  0.63009641, -0.44515271],
           [0.79912747,  0.54731751,  1.38572266,  0.25215349,  0.53881863],
           [1.67286732, -1.01761685, -1.50260358,  0.76664447,  0.12039094],
           [0.0794518,  -0.98933336, -1.47362544, -1.53739744, -0.72456275],
           [1.98762203,  0.32306071, -0.59824456,  0.11507048,  0.29800336],
           [-0.66406624,  0.28460058, -0.53597297, -0.87629931,  0.03738724],
           [1.2615778,  -1.2348926,   0.44024661, -0.68375754, -0.67039439],
           [0.2827203,   1.93129696,  1.93898045,  2.20129847,  0.52664778],
           [-0.98202734, -0.74826827,  0.62351579,  2.45611577,  0.07103695],
           [0.35018037,  0.7255914,  -1.19150352, -1.02409667, -0.95350107],
           [-0.09075129, -0.9228936,   0.2089229,  -1.1536842,   1.04792201],
           [-0.1400869,   0.22066072, -0.77344339,  0.3767629,  -0.17816183],
           [0.33842703, -0.19692364, -0.13609212,  0.11463521,  0.93589763],
           [-0.63184112, -0.79554138,  1.20817129, -0.16847198, -1.91915406],
           [3.58239294,  0.41332852,  0.84892119,  0.27462383,  0.31857523],
           [-0.60501598, -1.45720371, -0.20865775,  0.93282524,  0.5740151],
           [0.58133089,  0.28988017,  0.3118847,   0.92011735,  0.59145631],
           [0.89078815,  0.7623031,  0.39182755, -0.51600013, -0.75517478],
           [0.03771397, -2.45377377, -0.16932438, -0.28061899, -1.50432573],
           [0.54639548, -1.43334016,  0.19559251,  0.18211387,  1.15394131],
           [-1.06044922, -0.49069609, -0.58014407,  1.78838093, -0.22417057],
           [0.46340154, -0.40991382,  1.12722562, -0.85688648,  0.0813176],
           [0.30889757, -0.65339891,  0.58704872, -0.39376786, -0.44877587],
           [0.92729317, -1.14755184,  1.73186927,  0.25332661, -0.11282823],
           [-0.07558293,  0.20346545,  0.7319477,   0.19646336, -0.52679095],
           [0.03185715,  1.15809126,  0.19982445,  0.29174309, -0.09682723]]
weight12 = [[0.29405409, -2.83728115, -0.6125338,  -5.94480753,  1.38509496],
            [-0.71156164, -0.02798036,  0.23182841, -6.29022516,  1.42147102],
            [0.81859047, -0.74364486, -0.98722646, -5.78467833,  1.9987396],
            [1.27527553, -1.4477724,   0.55874741, -3.99765283,  0.0627271],
            [-0.09206944,  0.56140735, -0.29798044, -0.81313642, -0.84631512]]
weight2 = [[-42.86528341],
           [-36.35708623],
           [-57.14342617],
           [-8.16257509],
           [-58.44102358]]


# BFS to return the shortest path between 2 nodes
def shortest_path(start, end):
    if start == end:
        return [start]
    run = True
    PQ = Queue()
    PQ.put(start)
    came_from = {}
    v = ["nv"]*50
    v[start] = "v"
    while run:
        current = PQ.get()
        for neighbor in nodes[current]:
            if v[neighbor] == "nv":
                v[neighbor] = "v"
                came_from[neighbor] = current
                if neighbor != end:
                    PQ.put(neighbor)
                else:
                    run = False
                    break
    path = [end]
    while end in came_from:
        end = came_from[end]
        path.append(end)
    path = path[::-1]

    return path
# randomly generate the 3 entities


def create_entity():
    l = list(range(50))
    prey = random.choice(l)
    predator = random.choice(l)
    l.remove(prey)
    if prey != predator:
        l.remove(predator)
    agent = random.choice(l)
    return predator, prey, agent
# returns a new position of the prey after it moves following it's movement pattern


def move_prey(prey):
    return random.choice(nodes[prey]+[prey])
# returns a new position of the predator after it moves following it's movement pattern


def move_predator(predator, agent):
    if random.choice(range(10)) < 4:
        return random.choice(nodes[predator])
    else:
        predator_neighbors = nodes[predator]
        distance = []
        for node in predator_neighbors:
            distance.append(len(shortest_path(node, agent)))
        best_neighbor = []
        for i in range(len(distance)):
            if distance[i] == min(distance):
                best_neighbor.append(predator_neighbors[i])
        return random.choice(best_neighbor)

# updates the probablity data for prey


def prey_move_update(prey_belief):
    prey_belief_new = [0]*50
    for i in range(len(prey_belief)):
        nodes_affecting = nodes[i]+[i]
        for j in nodes_affecting:
            degree_of_j = len(nodes[j])+1
            prey_belief_new[i] = prey_belief_new[i] + \
                (prey_belief[j]/degree_of_j)
    return prey_belief_new

# updates probablity after a negative survey


def survey_update(belief, prediction):
    survey_not_prob = 1-belief[prediction]
    belief[prediction] = 0
    for i in range(len(belief)):
        belief[i] = belief[i]/survey_not_prob
    return belief


nodes = {0: [1, 49, 45], 1: [2, 0, 6], 2: [3, 1, 49], 3: [4, 2, 7], 4: [5, 3, 9], 5: [6, 4, 8], 6: [7, 5, 1], 7: [8, 6, 3], 8: [9, 7, 5], 9: [10, 8, 4], 10: [11, 9, 12], 11: [12, 10], 12: [13, 11, 10], 13: [14, 12, 18], 14: [15, 13, 16], 15: [16, 14, 20], 16: [17, 15, 14], 17: [18, 16, 22], 18: [19, 17, 13], 19: [20, 18, 21], 20: [21, 19, 15], 21: [22, 20, 19], 22: [23, 21, 17], 23: [24, 22, 25], 24: [25, 23, 27], 25: [
    26, 24, 23], 26: [27, 25, 31], 27: [28, 26, 24], 28: [29, 27, 30], 29: [30, 28, 32], 30: [31, 29, 28], 31: [32, 30, 26], 32: [33, 31, 29], 33: [34, 32, 36], 34: [35, 33], 35: [36, 34, 38], 36: [37, 35, 33], 37: [38, 36, 42], 38: [39, 37, 35], 39: [40, 38, 41], 40: [41, 39], 41: [42, 40, 39], 42: [43, 41, 37], 43: [44, 42, 46], 44: [45, 43, 48], 45: [46, 44, 0], 46: [47, 45, 43], 47: [48, 46], 48: [49, 47, 44], 49: [0, 48, 2]}
predator, prey, agent = create_entity()


def generate_U(agent, predator, prey_belief):
    if agent == predator:
        return 10000000
    else:
        inp = [len(shortest_path(agent, predator))-1]+prey_belief+[1]
        l = np.dot(inp, weight1)
        l2 = sigmoid(l)
        l3 = np.dot(l2, weight12)
        l4 = sigmoid(l3)
        l5 = np.dot(l4, weight2)
        output = sigmoid(l5)
        return output*14

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


def find_VPartialmodel_action(agent, predator, prey_belief):
    u = []
    for i in nodes[agent]+[agent]:
        ui = 0
        if i == prey:
            ui = 1
            u.append(ui)
            continue
        if i == predator:
            ui = 10000000
            u.append(ui)
            continue
        pred_dist = []
        for p in nodes[predator]:
            pred_dist.append(len(shortest_path(p, i)))
        min_pred_dist = min(pred_dist)
        close_nodes = pred_dist.count(min_pred_dist)
        for k in nodes[predator]:
            if len(shortest_path(i, k)) == min_pred_dist:
                pred_prob = (0.6*(1/close_nodes)) + \
                    (0.4*(1/len(nodes[predator])))
            else:
                pred_prob = 0.4*(1/len(nodes[predator]))
            ui = ui+(generate_U(i, k, prey_belief)*pred_prob)
        u.append(ui)
    action = nodes[agent]+[agent]
    minu = []
    for i in range(len(u)):
        if u[i] == min(u):
            minu.append(i)
    select = random.choice(minu)
    return action[select]
    # return action[u.index(min(u))]


def agentVPartial_star():
    m = 0
    predator, prey, agent = create_entity()
    prey_belief = [1/49]*50
    prey_belief[agent] = 0
    while True:
        m = m+1
        if m > 5000:
            return 0, m
            #print("out of moves")
        max_prey_beliefs = []
        for i in range(len(prey_belief)):
            if prey_belief[i] == max(prey_belief):
                max_prey_beliefs.append(i)
        prey_prediction = random.choice(max_prey_beliefs)

        if prey_prediction == prey:
            prey_belief = [0]*50
            # prey_caught+=1
            prey_belief[prey_prediction] = 1
        else:
            prey_belief = survey_update(prey_belief, prey_prediction)

        agent = find_VPartialmodel_action(agent, predator, prey_belief)

        if (prey == agent):
            return 1, m
        if (predator == agent):
            return 0, m

        prey_belief = survey_update(prey_belief, agent)
        prey = move_prey(prey)
        if (prey == agent):
            return 1, m
        predator = move_predator(predator, agent)
        if (predator == agent):
            return 0, m

        prey_belief = prey_move_update(prey_belief)
        prey_belief = survey_update(prey_belief, agent)


t = 0
move = 0
for i in range(3000):
    print(i)
    r, m = agentVPartial_star()
    move += m
    t += r
print(t/30)
print(move/3000)
