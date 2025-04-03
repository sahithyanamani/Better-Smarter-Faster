import numpy as np
import pandas as pd
import random
from queue import Queue

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

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

ds = pd.read_excel("utilities.xlsx")

x = ds.iloc[:,2].values
key_state = list(x)#:10]

x = ds.iloc[:,3].values
utility = list(x)#[:10]

output_scale=17#16.8512088094962
lookup_table={}

nodes={0: [1, 49, 45], 1: [2, 0, 6], 2: [3, 1, 49], 3: [4, 2, 7], 4: [5, 3, 9], 5: [6, 4, 8], 6: [7, 5, 1], 7: [8, 6, 3], 8: [9, 7, 5], 9: [10, 8, 4], 10: [11, 9, 12], 11: [12, 10], 12: [13, 11, 10], 13: [14, 12, 18], 14: [15, 13, 16], 15: [16, 14, 20], 16: [17, 15, 14], 17: [18, 16, 22], 18: [19, 17, 13], 19: [20, 18, 21], 20: [21, 19, 15], 21: [22, 20, 19], 22: [23, 21, 17], 23: [24, 22, 25], 24: [25, 23, 27], 25: [26, 24, 23], 26: [27, 25, 31], 27: [28, 26, 24], 28: [29, 27, 30], 29: [30, 28, 32], 30: [31, 29, 28], 31: [32, 30, 26], 32: [33, 31, 29], 33: [34, 32, 36], 34: [35, 33], 35: [36, 34, 38], 36: [37, 35, 33], 37: [38, 36, 42], 38: [39, 37, 35], 39: [40, 38, 41], 40: [41, 39], 41: [42, 40, 39], 42: [43, 41, 37], 43: [44, 42, 46], 44: [45, 43, 48], 45: [46, 44, 0], 46: [47, 45, 43], 47: [48, 46], 48: [49, 47, 44], 49: [0, 48, 2]}

train_outputs = np.array([utility]).T

train_input=[]
train_outputs=[]
for i in range(len(key_state)):
    l=key_state[i].replace(" ","").replace("(","").replace(")","").split(",")
    agent=int(l[0])
    prey=int(l[1])
    predator=int(l[2])
    inp=[len(shortest_path(agent,prey))-1,len(shortest_path(agent,predator))-1,len(shortest_path(prey,predator))-1,1]
    if inp not in train_input:
        if utility[i]<50:
            train_input.append([len(shortest_path(agent,prey))-1,len(shortest_path(agent,predator))-1,len(shortest_path(prey,predator))-1,1])
            train_outputs.append([utility[i]/output_scale])
        else:
            lookup_table[key_state[i]]=utility[i]

train_outputs = np.array(train_outputs)
train_inputs = np.array(train_input, dtype=float)

# np.random.seed(1)
weight1 = 1 * np.random.randn(4, 5) #(input size*hiddenlayer1 size)
weight12 = 1 * np.random.randn(5, 5) #(hiddenlayer1 size*hiddenlayer2 size)
weight2 = 1 * np.random.randn(5, 1) #(hiddenlayer2 size*output size)

err_mean=10
while err_mean>0.025:
    ####FORWARD PROPAGATION
    l = np.dot(train_inputs, weight1) #dot product of X (input) and first set of weights (3x2)
    l2 = sigmoid(l) #activation function
    l3 = np.dot(l2, weight12) #dot product of hidden layer (z2) and second set of weights (3x1)
    l4 = sigmoid(l3)
    l5 = np.dot(l4, weight2)
    output = sigmoid(l5)

    ####BACKWARD PROPAGATION
    output_error = train_outputs - output # error in output
    output_delta = output_error * sigmoid_derivative(output)
    
    l2_error = output_delta.dot(weight2.T) #z2 error: how much our hidden2 layer weights contribute to output error
    l2_delta = l2_error * sigmoid_derivative(l2) #applying derivative of sigmoid to z2 error
    
    l4_error = l2_delta.dot(weight12.T) #z2 error: how much our hidden1 layer weights contribute to output error
    l4_delta = l4_error * sigmoid_derivative(l4) #applying derivative of sigmoid to z2 error
    
    weight1 += 0.01*train_inputs.T.dot(l4_delta) # adjusting first set (input -> hidden) weights
    weight12 += 0.01*l2.T.dot(l2_delta) # adjusting second set (hidden1 -> hidden2) weights
    weight2 += 0.01*l4.T.dot(output_delta) # adjusting second set (hidden2 -> output) weights

    err_mean =np.mean(np.square(train_outputs - output))
    print("Loss: " + str(err_mean))


print(weight1)
print(weight12)
print(weight2)
print(output)
