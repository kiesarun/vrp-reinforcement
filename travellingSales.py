import mlrose
from math import cos, asin, sqrt


def travellingSales(prepared_data):
    for number_of_cars in range(len(prepared_data)):
        # Create list of city coordinates
        coords_list = []
        number_of_orders = 0
        delivery = 0

        for order in prepared_data[number_of_cars]:
            coords_list.append((order['coor'][0], order['coor'][1]))
            number_of_orders = number_of_orders + 1

        # Initialize fitness function object using coords_list
        fitness_coords = mlrose.TravellingSales(coords=coords_list)

        # Create list of distances between pairs of cities
        dist_list = [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426),
                     (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000),
                     (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426),
                     (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721),
                     (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056),
                     (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623),
                     (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)]

        # Initialize fitness function object using dist_list
        fitness_dists = mlrose.TravellingSales(distances=dist_list)

        problem_fit = mlrose.TSPOpt(length=number_of_orders, fitness_fn=fitness_coords, maximize=False)

        problem_no_fit = mlrose.TSPOpt(length=number_of_orders, coords=coords_list, maximize=False)

        # Solve problem using the genetic algorithm
        best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)

        print('The best state found is: ', best_state)
        for i in range(number_of_orders):
            for order in prepared_data[number_of_cars]:
                if best_state[i] == prepared_data[number_of_cars].index(order):
                    order['delivery'] = delivery
                    delivery = delivery + 1

        print('The fitness at the best state is: ', best_fitness)

    return prepared_data


def travelSalesMan(orders):
    # Create list of city coordinates
    # coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]
    coordinates = []
    for order in orders:
        coordinates.append((order.coordinate['lat'], order.coordinate['lon']))
    number_of_orders = len(coordinates)

    dist_list = []
    for i, order1 in enumerate(orders):
        for j, order2 in enumerate(orders):
            if i < j:
                dist_list.append((i, j, computeDistance(order1.coordinate['lat'], order1.coordinate['lon'],
                                                        order2.coordinate['lat'], order2.coordinate['lon'])))

    # Initialize fitness function object using coords_list
    # fitness_coords = mlrose.TravellingSales(distances=dist_list)

    # Create list of distances between pairs of cities
    # dist_list = [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426),
    #              (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000),
    #              (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426),
    #              (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721),
    #              (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056),
    #              (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623),
    #              (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)]

    print(dist_list)
    # Initialize fitness function object using dist_list
    fitness_dists = mlrose.TravellingSales(distances=dist_list)

    problem_fit = mlrose.TSPOpt(length=number_of_orders, fitness_fn=fitness_dists, maximize=False)

    # coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6),
    #            (1, 5), (2, 3)]
    # problem_no_fit = mlrose.TSPOpt(length = number_of_orders, maximize=False)
    # problem_no_fit = mlrose.TSPOpt(length = number_of_orders, coords = coordinates, maximize=False)

    # Solve problem using the genetic algorithm
    best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)

    print('The best state found is: ', best_state)
    print('The fitness at the best state is: ', best_fitness)
    print('*******************************************************')
    return best_fitness


def computeDistance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
        cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin... as km.
