from numpy import *
import random
import crossing
from genetic import mutation
import selecting
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.cbook import todate
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import logging as log
import os

class Genetic:
    def __init__(self):
        log.basicConfig(filename='runtime.log',level=log.DEBUG)

    def start(self, data):
        log.info("----------- starting ---------")
        plt.clf()
        if 'y' in data['function']:
            self.f = lambda x, y: eval(data['function'])
            self.plot = self.plot3d
            self.fitness = self.fitness3d
        else:
            self.f = lambda x: eval(data['function'])
            self.plot = self.plot2d
            self.fitness = self.fitness2d

        self.range = 2**int(data['pop_size'])
        self.pop_size = int(data['pop_size'])
        self.pop_count = int(data['pop_count'])
        self.gen_count = int(data['gen_count'])
        self.sel_method_param = int(data['sel_method_param'])
        self.mut_param = float(data['mut_method_param'])

        self.minx = float(data['min'])
        self.maxx = float(data['max'])
        self.width = self.maxx - self.minx


        cross_table = [crossing.average, crossing.one_point, crossing.two_point]
        try:
            self.cross_func = cross_table[int(data['cross_method'])]
        except:
            self.cross_func = crossing.average

        select_table = [selecting.rulette, selecting.turnee, selecting.ranking, selecting.elite]
        try:
            self.select_func = select_table[int(data['sel_method'])]
        except:
            self.select_func = selecting.rulette

        mut_table = [mutation.negation, mutation.defect, mutation.swap]
        try:
            self.mut_func = mut_table[int(data['mut_method'])]
        except:
            self.mut_func = mutation.negation
        
        self.plot()
        
        
        for _ in range(3):
            try:
                log.info("saving...")               
                plt.savefig('static/img/plot.jpg')
                log.info("saved")
                break
            except IOError:
                log.error("not saved")
        

    def getxy(self, xy):
        xpop_size = self.pop_size/2
        ypop_size = (self.pop_size+1)/2

        f = lambda x, y: self.minx + self.width/2**y*x

        return f(xy >> xpop_size, xpop_size), f((2**ypop_size-1) & xy, ypop_size)

    def fitness3d(self, xy):
        return self.f(*self.getxy(xy))

    def plot3d(self):
        log.info("plotting 3D...")
                        
        m = list(self.find_min())
        log.info("min found")

        mx = [self.getxy(i['x'])[0] for i in m]
        my = [self.getxy(i['x'])[1] for i in m]
        mz = [i['y'] for i in m]

        xpop_size = self.pop_size/2
        ypop_size = (self.pop_size+1)/2
        deltax = self.width/2**xpop_size
        deltay = self.width/2**ypop_size

        x = np.linspace(self.minx, self.maxx-deltax, 2**6 if self.pop_size >= 6 else 2**xpop_size)
        y = np.linspace(self.minx, self.maxx-deltay, 2**6 if self.pop_size >= 6 else 2**ypop_size)
        x, y = np.meshgrid(x, y)
        z = self.f(x, y)

        log.info("new figure")
        fig = plt.figure()
        log.info("adding subplot 3d")
        ax = fig.add_subplot(211, projection='3d')
        plotter = fig.gca(projection="3d")

        args = {
            'rstride': 1,
            'cstride': 1,
            'linewidth': 0,
            'cmap': cm.coolwarm
        }
        log.info("upper plotting")
        surface = plotter.plot_surface(x, y, z, **args)
        ax.scatter(mx, my, mz, s=10, marker='^', c='r')
        fig.colorbar(surface)

        log.info("lower plotting")
        plt.subplot(212)
        lims = [0, self.gen_count-1]
        plt.xlim(lims)
        plt.plot(range(len(mz)), mz)
        plt.plot(lims, 2*[np.min(z)], 'r')
        plt.plot(lims, 2*[min(mz)], 'g')


    def plot2d(self):
        m = list(self.find_min())
        extract_min = lambda d: ([self.getx(p0['x']) for p0 in d], [p1['y'] for p1 in d])

        mx, my = extract_min(m)
        delta = self.width/self.range
        x = range(0, self.range, 1 if self.pop_size <= 8 else self.range/256)
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

    def getx(self, x):
        return self.minx + self.width/self.range*x

    def fitness2d(self, x):
        return self.f(self.getx(x))


    def find_min(self):
        population = self.init()

        for i in range(self.gen_count):
            best, rated = self.rate(population)
            selected = self.select_func(population, self.sel_method_param)
            population = self.cross(selected)
            self.mutate(population)

            yield best


    def init(self):
        return [{'x': random.randrange(self.range)} for _ in range(self.pop_count)]


    def rate(self, population):
        for p in population:
            p['y'] = self.fitness(p['x'])

        return selecting.minp(population), population

    def cross(self, population):
        return [self.cross_func(p, self.pop_size) for p in population]

    def mutate(self, population):
        for _ in population:
            if random.uniform(0, 1) < self.mut_param:
                beast = random.choice(population)
                beast['x'] = self.mut_func(beast['x'], self.pop_size)
