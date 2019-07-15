from abc import ABC
import random
from map.Map import Map, WALL, FLOOR1, FLOOR2, FLOOR3
import Objects


class MapObjects(ABC):
    def __init__(self, _map: Map, config: dict = None):
        self.grid = []
        self.map = _map
        self.config = config

    def get(self):
        return self.grid


class Empty(MapObjects):
    pass


class Special(MapObjects):
    pass


class Random(MapObjects):
    def __init__(self, _map: Map, config: dict = None):
        self.grid = []
        self.map = _map.get()
        self.config = config
        self.objects = []

        map_grid = self.map

        if 'objects' in self.config:
            for obj_name in self.config['objects']:
                prop = self.config['objects'][obj_name]

                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if map_grid[coord[1]][coord[0]] == WALL:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

        if 'ally' in self.config:
            for obj_name in self.config['ally']:
                prop = self.config['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = (random.randint(1, 39), random.randint(1, 39))
                    intersect = True
                    while intersect:
                        intersect = False
                        if map_grid[coord[1]][coord[0]] == WALL:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))
                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

        if 'enemies' in self.config:
            for obj_name in self.config['enemies']:
                prop = self.config['enemies'][obj_name]
                for i in range(random.randint(0, 5)):
                    coord = (random.randint(1, 30), random.randint(1, 22))
                    intersect = True
                    while intersect:
                        intersect = False
                        if map_grid[coord[1]][coord[0]] == WALL:
                            intersect = True
                            coord = (random.randint(1, 39),
                                     random.randint(1, 39))
                            continue
                        for obj in self.objects:
                            if coord == obj.position or coord == (1, 1):
                                intersect = True
                                coord = (random.randint(1, 39),
                                         random.randint(1, 39))

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

