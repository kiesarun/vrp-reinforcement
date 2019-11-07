import mlrose
import numpy as np

def travellingSales(coors):
    # Create list of city coordinates
    print('coors: ', coors)
    # coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]
    coords_list =[]
    for c in coors:
        # print('eieieieieieieieieie : ',c[0],c[1])
        coords_list.append((c[0],c[1]))

    print('coords_list: ',coords_list)

    # Initialize fitness function object using coords_list
    fitness_coords = mlrose.TravellingSales(coords = coords_list)

    # Create list of distances between pairs of cities
    # dist_list = [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426),
    #              (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000),
    #              (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426),
    #              (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721),
    #              (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056),
    #              (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623),
    #              (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)]
    dist_list = []

    # Initialize fitness function object using dist_list
    fitness_dists = mlrose.TravellingSales(distances = dist_list)

    problem_fit = mlrose.TSPOpt(length = 8, fitness_fn = fitness_coords,maximize=False)

    coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]
    problem_no_fit = mlrose.TSPOpt(length = 8, coords = coords_list,maximize=False)

    # Solve problem using the genetic algorithm
    best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state = 2)

    print('The best state found is: ', best_state)

    print('The fitness at the best state is: ', best_fitness)

    return best_state



