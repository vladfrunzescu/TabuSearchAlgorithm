"""
We use Tabu Search algorithm for the Travelling Salesman Problem. The overall algorithm is properly parameterized
for both A and B problems.
Problem A requires as solution the shortest Hamiltonian path that visits all the cities exactly once, except for the
starting city/location, with minimum cost. Here, we use the same value for starting/ending location to show that
the problem is about a circuit more than a simple path from city A to city B.
Problem B requires as solution the shortest path from city A to city B, where A and B can be chosen by the user.
In both problems, it is not guaranteed the best solution will be found as we use a Greedy Local Search Algorithm.
Note: We suppose that the distances between the cities are symmetric and that there is a direct path between any two
distinct cities.
"""
import copy

"""
nearestNeighbourFirstSolution - function that implements the Nearest Neighbour local Greedy search Algorithm and returns
                        a locally optimal path from city A to city B.
                        
input:
start_node - integer representing starting location, < number of cities
end_node - integer representing ending location, < number of cities
dMatrix - matrix of distances representing the distance from every "i" city (as a row in the matrix)
          to every "j" city (as each column of the current line).
          
output:
first_solution - subset/permutation of the cities, representing the path found
distance_of_first_solution - integer, the overall cost of the path
"""


def nearestNeighbourFirstSolution(start_node, end_node, dMatrix):

    first_solution = []

    visiting = start_node

    distance_of_first_solution = 0

    while (visiting != end_node and len(first_solution) > 0 and visiting not in first_solution) or first_solution == []:
        minim = 10000
        i = 0
        for k in dMatrix[visiting]:     #for each city we look for the nearest neighbour
            if k < minim and i not in first_solution and i != visiting:
                minim = k
                best_node = i
            i += 1

        first_solution.append(visiting)
        distance_of_first_solution = distance_of_first_solution + int(minim)        #we compute the current distance
        visiting = best_node        #we assign the city found to the current visiting city


    first_solution.append(end_node)
    if(start_node == end_node):
        distance_of_first_solution += dMatrix[first_solution[-2]][end_node] #we add the distance
        distance_of_first_solution -= 10000
    return first_solution, distance_of_first_solution


"""
find_neighborhood - function that generates all the permutations using the elements from the solution, except 
                    first and last element
input:
solution - subset of the cities, potential solution for the problem
dMatrix - matrix of distances representing the distance from every "i" city (as a row in the matrix)
          to every "j" city (as each column of the current line).
          
output:
neighborhood_of_solution - list of permutations sorted by the overall cost of the path (permutation)
"""


def find_neighborhood(solution, dMatrix):

    neighborhood_of_solution = []

    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[1:-1]:
            idx2 = solution.index(kn)
            if n == kn:
                continue

            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0

            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                distance += dMatrix[k][next_node]

            _tmp.append(distance)

            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    if(len(neighborhood_of_solution) > 0):
        indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1
        neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    else:
        neighborhood_of_solution.append(solution)
    return neighborhood_of_solution


"""
tabu_search - functions that implements tabu search
intput:
first_solution - subset/permutation of the cities, representing the path found
distance_of_first_solution - integer, the overall cost of the path
dMatrix - matrix of distances representing the distance from every "i" city (as a row in the matrix)
          to every "j" city (as each column of the current line).
iters - number of iterations we want tabu search to execute
size - maximum size of tabu list
output:
best_solution_ever - the optimal solution found
best_cost - the overall cost of best_solution_ever
"""
def tabu_search(first_solution, distance_of_first_solution, dMatrix, iters, size):
    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution

    while count <= iters:
        neighborhood = find_neighborhood(solution, dMatrix)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1

        found = False
        while not found and index_of_best_solution < len(neighborhood)-1:
            i = 0
            while i < len(best_solution):

                if best_solution[i] != solution[i]:
                    first_exchange_node = best_solution[i]
                    second_exchange_node = solution[i]
                    break
                i = i + 1

            if [first_exchange_node, second_exchange_node] not in tabu_list and [
                second_exchange_node,
                first_exchange_node,
            ] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            else:
                try:
                    index_of_best_solution = index_of_best_solution + 1
                    best_solution = neighborhood[index_of_best_solution]
                except Exception as ex:
                    print(ex)

        if len(tabu_list) >= size:
            tabu_list.pop(0)

        count = count + 1

    return best_solution_ever, best_cost


"""
readFromFile - function that reads from a file the input data
input:
file - string, the file we want to read from
output:
numberOfCities - integer
dMatrix - matrix of distances
source_city - starting location for problem B
destination_city - ending location for problem B
"""


def readFromFile(file):
    file_in = open(file, 'r')
    numberOfCities = int(file_in.readline())
    dMatrix = []

    for i in range(numberOfCities):
        dMatrix_line = file_in.readline().split(',')
        dLine = [int(dist) for dist in dMatrix_line]
        dMatrix.append(dLine)

    #source_city = int(file_in.readline())
    #destination_city = int(file_in.readline())

    return numberOfCities, dMatrix#, source_city, destination_city


def writeToFile(file, best_solution, best_cost):
    file_out = open(file, 'a')
    file_out.write(str(len(best_solution)) + '\n')

    string = ""
    for city in best_solution:
        string = string + str(city+1) + ', '

    new_string = string[:-2]
    file_out.write(new_string + '\n')
    file_out.write(str(best_cost) + '\n')



def main():
    input_file = 'easy_01_tsp.txt'
    #input_file = 'easy_tsp.txt'
    #input_file = 'medium_tsp.txt'
    #input_file = 'hard_tsp.txt'
    output_file = 'easy_01_tsp_solution.txt'
    open('easy_01_tsp_solution.txt', 'w').close()

    #numberOfCities, dMatrix, start_node, end_node = readFromFile(input_file)

    numberOfCities, dMatrix = readFromFile(input_file)

    #Problem A
    first_solution, distance_of_first_solution = nearestNeighbourFirstSolution(0, 0, dMatrix)

    best_sol, best_cost = tabu_search(
        first_solution,
        distance_of_first_solution,
        dMatrix,
        20,
        20,
    )
    best_sol.pop()
    writeToFile(output_file, best_sol, best_cost)

    """
    #Problem B
    first_solution, distance_of_first_solution = nearestNeighbourFirstSolution(start_node-1, end_node-1, dMatrix)
    best_sol, best_cost = tabu_search(
        first_solution,
        distance_of_first_solution,
        dMatrix,
        20,
        20,
    )
    writeToFile(output_file, best_sol, best_cost)
    """

main()