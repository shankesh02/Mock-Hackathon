import json
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

readObject=open("C:\Mock Hackathon\Input\level1a.json","r")
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


demand=[]
for i in input["neighbourhoods"]:
    demand.append(input["neighbourhoods"][i]["order_quantity"])

cost, path = main(matrix,0)

start_points=[]
capacity=[]
for i in input["vehicles"]:
    start_points.append(input["vehicles"][i]["start_point"])
    capacity.append(input["vehicles"][i]["capacity"])

json_path=[]
t=[]
demand_met=0
for i in path:
    if i==0:
       t.append(start_points[0])
    else:
        if demand_met+demand[i-1] > capacity[0]:
            t.append(start_points[0])
            json_path.append(t)
            t=[start_points[0],"n"+str(i-1)]
            demand_met=demand[i-1]
        else:
            demand_met=demand_met+demand[i-1]
            t.append("n"+str(i-1))
json_path.append(t)
print("-> Best Tour with Capacity: ",json_path)

sub_dict=[]
for i in range(len(json_path)):
    d={"path"+str(i+1):json_path[i]
       }
    sub_dict.append(d)


for i in input["vehicles"]:
    dictionary={
        i: {
            "path1":json_path[0],
            "path2":json_path[1],
            "path3":json_path[2],
            "path4":json_path[3]
            }
    }
    with open("C:\Mock Hackathon\Output\level1a_output.json","w") as writeObject:
        json.dump(dictionary,writeObject)
