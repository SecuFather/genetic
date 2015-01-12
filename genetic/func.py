from __future__ import division
import matplotlib.pyplot as plt
from numpy import *
from random import randrange, shuffle
import itertools as it


RESOLUTION = 1000.0

class Genetic:
    def __init__(self):
        pass

    def start(self, data):
        plt.clf()
        self.f = lambda x: eval(data['function'])
        self.range = 2**int(data['pop_size'])
        self.pop_count = int(data['pop_count'])
        self.gen_count = int(data['gen_count'])
        self.tour_size = int(data['sel_method_param'])

        self.minx = float(data['min'])
        self.maxx = float(data['max'])

        x = arange(self.minx, self.maxx, (self.maxx-self.minx)/RESOLUTION)

        m = self.find_min()
        extract_min = lambda d: ([p0['x'] for p0 in d], [p1['y'] for p1 in d])

        mx, my = extract_min(m)

        plt.subplot(211)
        plt.plot(mx, my, 'ro')
        plt.plot(x, self.f(x))

        plt.subplot(212)
        plt.plot(range(self.gen_count), my)
        plt.plot([0, self.gen_count-1], 2*[min(self.f(x))], 'r')
        plt.plot([0, self.gen_count-1], 2*[my[-1]], 'g')

        while True:
            try:
                plt.savefig('static/img/plot.jpg')
                break
            except:
                pass

    def gen_pop(self):
        k = randrange(self.range)/self.range
        return self.minx + k * (self.maxx - self.minx)

    def group(self, x, n):
        for i in range(0, len(x), n):
            yield x[i:i+n]

    def create_population(self, n):
        return [{'x': self.gen_pop()} for i in range(n)]

    def crossed_champs(self, champs):
        nc = len(champs)
        for i in range(nc-1):
            for j in range(i+1, nc):
                yield {'x': (champs[i]['x']+champs[j]['x'])/2.0}

    def crossed_champs_list(self, champs, n):
        return list(it.islice(self.crossed_champs(champs), n))

    def find_min(self):
        key = lambda x: x['y']
        population = self.create_population(self.pop_count)
        res = []

        for i in range(self.gen_count):
            for p in population:
                p['y'] = self.f(p['x'])

            g = list(self.group(population, self.tour_size))

            champs = [min(p, key=key) for p in g]
            res.append(min(champs, key=key))

            population = self.crossed_champs_list(champs, self.pop_count-len(champs))
            population += self.create_population(self.pop_count - len(population))
        return res

