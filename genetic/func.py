from __future__ import division
import matplotlib.pyplot as plt
from numpy import *
from random import randrange, shuffle


RESOLUTION = 100.0


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

        m, ddd = self.find_min()
        extract_min = lambda d: ([p0['x'] for p0 in d], [p1['y'] for p1 in d])

        mx, my = extract_min(m)
        dx, dy = extract_min(ddd)
        plt.plot(dx, dy, 'go')
        plt.plot(mx, my, 'ro')


        plt.plot(x, self.f(x))
        plt.savefig('static/img/plot.jpg')

    def gen_pop(self):
        k = randrange(self.range)/self.range
        return self.minx + k * (self.maxx - self.minx)

    def group(self, lst, n):
        return zip(*[lst[i::n] for i in range(n)])

    def find_min(self):
        key = lambda x: x['y']
        population = [{'x': self.gen_pop()} for i in range(self.pop_count)]
        ddd = population
        res = []

        for i in range(self.gen_count):
            for p in population:
                p['y'] = self.f(p['x'])
            shuffle(population)
            g = self.group(population, self.tour_size)
            champs = [min(p, key=key) for p in g]
            res.append(min(champs, key=key))
            print res
            population = []
            nc = len(champs)
            for i in range(nc):
                for j in range(self.tour_size):
                    population.append({'x': (champs[i]['x']+champs[(i+j+1)%nc]['x'])/2})

        return res, ddd

