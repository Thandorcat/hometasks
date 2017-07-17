def top10logs(file):
    adresses = {}
    with open(file,'r') as f:
        for line in f:
            address = line[:line.index(' ')]
            if address in adresses:
                adresses[address] += 1
            else:
                adresses[address] = 1

    return (sorted(adresses, key=adresses.get, reverse=True))[:10]