import json

'''
The below code does not run for large datasets as it computes permutation which requires a lot of time.

from sys import maxsize 
from itertools import permutations
V = 20
 
# implementation of traveling Salesman Problem 
def travellingSalesmanProblem(graph, s): 
    
 
    # store all vertex apart from source vertex 
    vertex = [] 
    for i in range(V): 
        if i != s: 
            vertex.append(i) 
 
    # store minimum weight Hamiltonian Cycle 
    min_path = maxsize 
    next_permutation=permutations(vertex)
    
    for i in next_permutation:
        print(i)
        
        # store current Path weight(cost) 
        current_pathweight = 0
 
        # compute current path weight 
        k = s 
        for j in i: 
            current_pathweight += graph[k][j] 
            k = j 
        current_pathweight += graph[k][s] 
 
        # update minimum 
        min_path = min(min_path, current_pathweight) 
         
    return min_path 
'''

import numpy as np
from scipy.spatial.distance import euclidean

def score_solution(cities, solution):
    
    if len(solution) != len(cities):
        raise Exception(('Invalid solution: len(solution) is {}, ' + \
                'but it should be {}.').format(len(solution), len(cities)))

    if set(solution) != set(range(len(cities))):
        raise Exception('Invalid solution: The solution does not ' + \
                'visit each city exactly once!')

    dist = 0.0
    for i in range(len(solution)):
        p_prev = cities[solution[i-1]]
        p_here = cities[solution[i]]
        dist += euclidean(p_prev, p_here)
    return dist

def tsp_solver_silly(cities, new_best_solution_func = None):

    best_dist = float("inf")
    best_solution = None
    for i in range(1000):
        solution = np.arange(len(cities))
        np.random.shuffle(solution)
        dist = score_solution(cities, solution)
        if dist < best_dist:
            best_dist = dist
            best_solution = solution
            if new_best_solution_func:
                new_best_solution_func(solution)
    return best_solution,best_dist



readObject=open("C:\Mock Hackathon\Input\level0.json","r")
input=json.load(readObject)
matrix=[]
res_dist=[]
for i in input["restaurants"]:
    for j in input["restaurants"][i]:
        for k in input["restaurants"][i]["neighbourhood_distance"]:
            res_dist.append(k)

ind=res_dist.index(min(res_dist))

for i in input["neighbourhoods"]:
    for j in input["neighbourhoods"][i]:
        temp=[]
        for k in input["neighbourhoods"][i]["distances"]:
            temp.append(k)
    matrix.append(temp)

ghostPath,dist=tsp_solver_silly(matrix)
path=[]
for i in ghostPath:
    if i<(len(matrix)):
        path.append(i)

print("\nPath: ",path)
print("Distance: ",dist)

json_path=[]
start_points=[]
for i in input["vehicles"]:
    start_points.append(input["vehicles"][i]["start_point"])
json_path.append(start_points[0])
for i in path:
    json_path.append("n"+str(i))
json_path.append(start_points[0])
print(json_path)

for i in input["vehicles"]:
    dictionary={
        i:{
            "path": json_path
        }
    }
    with open("C:\Mock Hackathon\Output\level0_output.json","w") as writeObject:
        json.dump(dictionary,writeObject)
