def prepareData(coors,i):
    # print('ccccccccccccccccccccccccccccccccc',coors)
    coors_separated = []
    coor = []
    for c in coors:
        if c['carNumber'] == i:
            coor.append((c['coor'][0],c['coor'][1],c['id'],c['carNumber']))

    return coor
