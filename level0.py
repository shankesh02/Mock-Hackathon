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

'''
The below code does not give an optimal solution as it takes random paths and chooses the best among them
'''
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

'''

import numpy as np
import math as math

def objective_calculator(solution, coordinates):
    cost = 0
    for i in range(len(solution) - 1):
        city_1 = solution[i]
        city_2 = solution[i + 1]
        cost += euclid_calculator(city_1, city_2, coordinates)
    return cost

def euclid_calculator(city_1, city_2, coordinates):
    return math.sqrt((coordinates[city_1][0] - coordinates[city_2][0]) ** 2 +
                     (coordinates[city_1][1] - coordinates[city_2][1]) ** 2)

def city_swap(city_1, city_2, current_solution, coordinates):
    tour_choice = current_solution.copy()
    keeper = tour_choice[city_1]
    tour_choice[city_1] = tour_choice[city_2]
    tour_choice[city_2] = keeper
    
    if objective_calculator(tour_choice, coordinates) < objective_calculator(current_solution, coordinates):
        print("Current cost: ", objective_calculator(tour_choice, coordinates))
        current_solution = tour_choice
        print("Current tour:", current_solution)
        print("-------------------------------------------------------------")
    return current_solution

'''
def main(coordinates, start_vertex=0):
    np.random.seed(start_vertex)
    partly_initial_solution = np.random.permutation(range(-1, len(coordinates)-1))
    initial_solution = np.append(partly_initial_solution, [partly_initial_solution[0]])
    
    current_solution = initial_solution
    for k in range(10):
        for i in range(1, len(coordinates) - 1):
            for j in range(i + 1, len(coordinates)):
                current_solution = city_swap(i, j, current_solution, coordinates)
    
    cost = objective_calculator(current_solution, coordinates)
    print("Results:")
    print("-> Cost of best solution: ", cost)
    print("-> Best Tour Founded: ", current_solution)
    return cost, current_solution
'''
def main(coordinates, start_vertex=0):
    np.random.seed(start_vertex)
    partly_initial_solution = list(range(1, len(coordinates)))
    initial_solution = [0] + partly_initial_solution + [0]  # Include the source vertex at the beginning and end

    current_solution = initial_solution
    for k in range(10):
        for i in range(1, len(coordinates) - 1):
            for j in range(i + 1, len(coordinates)):
                current_solution = city_swap(i, j, current_solution, coordinates)

    cost = objective_calculator(current_solution, coordinates)
    print("Results:")
    print("-> Cost of the best solution: ", cost)
    print("-> Best Tour Found: ", current_solution)
    return cost, current_solution



readObject=open("C:\Mock Hackathon\Input\level0.json","r")
input=json.load(readObject)
matrix=[]
res_dist=[]
for i in input["restaurants"]:
    for j in input["restaurants"][i]:
        temp=[0]
        for k in input["restaurants"][i]["neighbourhood_distance"]:
            temp.append(k)
    res_dist.append(temp)
matrix.append(res_dist[0])

c=1
for i in input["neighbourhoods"]:
    for j in input["neighbourhoods"][i]:
        temp=[res_dist[0][c]]
        for k in input["neighbourhoods"][i]["distances"]:
            temp.append(k)
    c=c+1
    matrix.append(temp)

cost, path = main(matrix,0)

# ghostPath,dist=tsp_solver_silly(matrix)
# path=[]
# for i in ghostPath:
#     if i<(len(matrix)):
#         path.append(i)

# print("\nPath: ",path)
# print("Distance: ",dist)

json_path=[]
start_points=[]
for i in input["vehicles"]:
    start_points.append(input["vehicles"][i]["start_point"])

for i in path:
    if i==0:
        json_path.append(start_points[0])
    else:
        json_path.append("n"+str(i-1))

for i in input["vehicles"]:
    dictionary={
        i:{
            "path": json_path
        }
    }
    with open("C:\Mock Hackathon\Output\level0_output.json","w") as writeObject:
        json.dump(dictionary,writeObject)
