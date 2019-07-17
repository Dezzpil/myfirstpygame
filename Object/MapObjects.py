from abc import ABC
import random
from Map.Map import Map, WALL, FLOOR1, FLOOR2, FLOOR3
import Objects


class MapObjects(ABC):
    """
    Класс знает структуру манифеста объектов
    Класс знает какие типы объектов как соотносятся с манифестом
    """
    def __init__(self, _map: Map):
        """
        :param _map: Объект карты
        """
        self.map = _map.get_grid()
        self.grid = []
        self.objects = []
        self.manifest = None
        self.contents = None

    def init(self, manifest: dict = None, contents: dict = None) -> None:
        """
        Инициализация объектов на карте
        :param manifest: Манифест с описанием объектов
        :param contents: Явно заданный список объектов, присутсвующих на карте
        :return:
        """
        self.manifest = manifest
        self.contents = contents
        print(f'contents: {contents}')
        print(f'manifest: {manifest}')
        if contents is None and manifest is not None:
            self.contents = dict()
            for obj_group_key, obj_group in manifest.items():
                for obj_key, obj_params in obj_group.items():
                    self.contents[obj_key] = 0
                    if 'min-count' in obj_params and 'max-count' in obj_params:
                        self.contents[obj_key] = range(random.randint(obj_params['min-count'], obj_params['max-count']))

        for group_name, obj_type in [
            ('objects', Objects.Interactive),
            ('ally', Objects.Ally),
            ('enemies', Objects.Enemy)
        ]:
            if group_name in manifest:
                for obj_name in manifest[group_name]:
                    obj_props = manifest[group_name][obj_name]
                    self._create_object(obj_name, obj_props, self.contents[obj_name])

    def _create_object(self, obj_type: type, obj_props: dict, count: int) -> None:
        """
        Создать требуемое кол-во объектов карты заданного типа, следуя манифесту
        :param obj_type:
        :param obj_props:
        :param count:
        :return:
        """
        for i in range(0, count):
            coord = (random.randint(1, 39), random.randint(1, 39))
            # coord = (random.randint(1, 30), random.randint(1, 22))
            intersect = True
            while intersect:
                intersect = False
                if self.map[coord[1]][coord[0]] == WALL:
                    intersect = True
                    coord = (random.randint(1, 39),
                             random.randint(1, 39))
                    continue
                for obj in self.objects:
                    if coord == obj.position or coord == (1, 1):
                        intersect = True
                        coord = (random.randint(1, 39),
                                 random.randint(1, 39))
            self.objects.append(obj_type(obj_props, coord))
                # prop['sprite'], prop['action'], coord)) # for objects and ally
                # prop['sprite'], prop, prop['experience'], coord)) # for enemies

    def get(self) -> list:
        """
        Получить список объекты карты
        :return:
        """
        return self.objects


class Empty(MapObjects):
    pass


class Special(MapObjects):
    pass


class Random(MapObjects):
    pass
