import matplotlib.pyplot as plt
from numpy import *
import random
import crossing
import selecting

class Genetic:
    def __init__(self):
        pass

    def start(self, data):
        plt.clf()
        self.f = lambda x: eval(data['function'])
        self.range = 2**int(data['pop_size'])
        self.pop_size = int(data['pop_size'])
        self.pop_count = int(data['pop_count'])
        self.gen_count = int(data['gen_count'])
        self.sel_method_param = int(data['sel_method_param'])

        self.minx = float(data['min'])
        self.maxx = float(data['max'])
        self.width = self.maxx - self.minx


        cross_table = [crossing.average, crossing.one_point, crossing.two_point]
        try:
            self.cross_func = crossing.table[int(data['cross_method'])]
        except:
            self.cross_func = crossing.average

        select_table = [selecting.rulette, selecting.turnee, selecting.ranking, selecting.elite]
        try:
            self.select_func = select_table[int(data['sel_method'])]
        except:
            self.select_func = selecting.rulette


        m = list(self.find_min())
        extract_min = lambda d: ([self.getx(p0['x']) for p0 in d], [p1['y'] for p1 in d])

        mx, my = extract_min(m)

        delta = self.width/self.range
        x = range(self.range)
        y = [self.fitness(i) for i in x]

        plt.subplot(211)
        plt.xlim([self.minx, self.maxx-delta])
        plt.plot(mx, my, 'ro')
        plt.plot([self.getx(i) for i in x], y)

        plt.subplot(212)
        lims = [0, self.gen_count-1]
        plt.xlim(lims)
        plt.plot(range(len(my)), my)
        plt.plot(lims, 2*[min(y)], 'r')
        plt.plot(lims, 2*[min(my)], 'g')

        while True:
            try:
                plt.savefig('static/img/plot.jpg')
                break
            except:
                pass

    def getx(self, x):
        return self.minx + self.width/self.range*x

    def fitness(self, x):
        return self.f(self.getx(x))


    def find_min(self):
        population = self.init()

        for i in range(self.gen_count):
            best, rated = self.rate(population)
            selected = self.select_func(population, self.sel_method_param)
            population = self.cross(selected)

            yield best


    def init(self):
        return [{'x': random.randrange(self.range)} for _ in range(self.pop_count)]


    def rate(self, population):
        for p in population:
            p['y'] = self.fitness(p['x'])

        return selecting.minp(population), population

    def cross(self, population):
        return [self.cross_func(p, self.pop_size) for p in population]

