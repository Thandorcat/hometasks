def formDict(keys, values ):
    values += [None]*(keys.__len__() - values.__len__())
    dict = {}
    for key, value in zip(keys, values):
        dict[key] = value
    else: return dict
