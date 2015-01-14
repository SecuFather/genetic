import random

def minp(population):
    return min(population, key=lambda x: x['y'])

def maxp(population):
    return max(population, key=lambda x: x['y'])

def _rulette(best, worst, population):
    r = random.uniform(best['y'], worst['y'])
    ruletted = filter(lambda x: x['y'] < r, population)

    return best if not ruletted else random.choice(ruletted)

def rulette(population):
    best = minp(population)
    worst = maxp(population)

    return [(_rulette(best, worst, population), _rulette(best, worst, population)) for p in population]

def group(x, n):
    for i in range(0, len(x), n):
        yield x[i:i+n]

def turnee(population, tour_size):
    groups = list(group(population, tour_size))
    leaders = [minp(g) for g in groups]

    return [(random.choice(leaders), random.choice(leaders)) for p in population]


