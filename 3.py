def combine(list1, list2):
    list = set()
    for i in list1:
        if i not in list:
            list.add(i)
    for i in list2:
        if i not in list:
            list.add(i)
    return list

