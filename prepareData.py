def prepareData(grouped_cars,number_of_cars):
  prepared_data = []

  for car_num in range(number_of_cars):
    filter_group =[]
    for grouped_c in grouped_cars:
      if grouped_c['carNumber'] == car_num:
          filter_group.append(grouped_c)
    prepared_data.append(filter_group)

  return prepared_data
