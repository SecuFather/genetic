import random

def minp(population):
    return min(population, key=lambda x: x['y'])

def maxp(population):
    return max(population, key=lambda x: x['y'])

def rulette(population):
    best = minp(population)
    r = random.uniform(best['y'], maxp(population)['y'])
    ruletted = filter(lambda x: x['y'] < r, population)

    return best if not ruletted else random.choice(ruletted)

table=[]