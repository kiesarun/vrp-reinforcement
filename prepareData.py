def prepareData(grouped_cars,car_number,):
    prepared_data = []

    for grouped_c in grouped_cars:
        if grouped_c['carNumber'] == car_number:
            prepared_data.append(grouped_c)
                
    return prepared_data
