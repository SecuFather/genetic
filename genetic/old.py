def cross(self, x, y):
        return self.cross_func(x, y, self.crossing_params)

    def gen_pop(self):
        k = randrange(self.range)/self.rangew
        dx = (self.maxx-self.minx)/self.resolution
        return self.minx + int(k*self.resolution) * dx

    def group(self, x, n):
        for i in range(0, len(x), n):
            yield x[i:i+n]

    def create_population(self, n):
        return [{'x': self.gen_pop()} for i in range(n)]

    def crossed_champs(self, champs):
        nc = len(champs)
        for i in range(nc-1):
            for j in range(i+1, nc):
                yield {'x': self.cross(champs[i]['x'], champs[j]['x'])}

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