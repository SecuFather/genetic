import random

min_key = lambda x: x['y']

def minp(population):
    return min(population, key=min_key)

def maxp(population):
    return max(population, key=min_key)

def _rulette(best, worst, population):
    r = random.uniform(best['y'], worst['y'])
    ruletted = filter(lambda x: x['y'] <= r, population)

    return random.choice(ruletted)

def rulette(population, param):
    best = minp(population)
    worst = maxp(population)

    return [(_rulette(best, worst, population), _rulette(best, worst, population)) for _ in population]

def group(x, n):
    for i in range(0, len(x), n):
        yield x[i:i+n]

def turnee(population, tour_size):
    groups = list(group(population, tour_size))
    leaders = [minp(g) for g in groups]

    return [(random.choice(leaders), random.choice(leaders)) for _ in population]

def _ranking(rank, head_size):
    thres = random.randrange(head_size)
    lucky = filter(lambda x: x[0] <= thres, rank)

    return random.choice(lucky)[1]

def ranking(population, head_size):
    ordered = sorted(population, key=min_key)
    rank = filter(lambda x: x[0] < head_size, enumerate(ordered))
    
    return [(_ranking(rank, head_size), _ranking(rank, head_size)) for _ in population]


def elite(population, elite_count):
    ordered = sorted(population, key=min_key)
    ell = ordered[:elite_count]

    return [(random.choice(ell), random.choice(ell)) for _ in population]