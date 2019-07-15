import random
from abc import ABC


WALL = [0]
FLOOR1 = [0]
FLOOR2 = [0]
FLOOR3 = [0]


class Map(ABC):
    def __init__(self):
        self.grid = []

    def get(self):
        return self.grid


class Empty(Map):
    """
    Пустая карта
    """
    def __init__(self):
        self.grid = []


class Random(Map):
    """
    Случайно генерируемая карта
    """
    def __init__(self):
        self.grid = [[0 for _ in range(41)] for _ in range(41)]
        for i in range(41):
            for j in range(41):
                if i == 0 or j == 0 or i == 40 or j == 40:
                    self.grid[j][i] = WALL
                else:
                    self.grid[j][i] = [WALL, FLOOR1, FLOOR2, FLOOR3, FLOOR1,
                                       FLOOR2, FLOOR3, FLOOR1, FLOOR2][random.randint(0, 8)]


class End(Map):
    """
    Последняя карта в игре
    """
    def __init__(self):
        self.grid = ['000000000000000000000000000000000000000',
                    '0                                     0',
                    '0                                     0',
                    '0  0   0   000   0   0  00000  0   0  0',
                    '0  0  0   0   0  0   0  0      0   0  0',
                    '0  000    0   0  00000  0000   0   0  0',
                    '0  0  0   0   0  0   0  0      0   0  0',
                    '0  0   0   000   0   0  00000  00000  0',
                    '0                                   0 0',
                    '0                                     0',
                    '000000000000000000000000000000000000000'
                    ]
        self.grid = list(map(list, self.grid))
        for i in self.grid:
            for j in range(len(i)):
                i[j] = WALL if i[j] == '0' else FLOOR1

