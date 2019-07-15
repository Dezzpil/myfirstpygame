import yaml
from typing import Dict, Union, List, Tuple
from map import Map, MapObjects
import os
from pprint import pprint


def node_to_value(node: yaml.ScalarNode) -> Union[str, float]:
    """
    Получить значение правильного типа из yaml.ScalarNode
    """
    _type = node.tag.split(':')[-1]
    if _type == 'int':
        return int(node.value)
    elif _type == 'float':
        return float(node.value)

    return node.value


class MapFactory(yaml.YAMLObject):

    OBJECTS_CONFIG = {'objects': []}

    @staticmethod
    def load_objects_config():
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            file = open(f"{path}/objects.yml", "r")
            MapFactory.OBJECTS_CONFIG = yaml.load(file.read(), Loader=yaml.Loader)
            print(MapFactory.OBJECTS_CONFIG)
            file.close()
        except IOError as e:
            print(e)

    @classmethod
    def from_yaml(cls, loader, node: yaml.MappingNode) -> Dict[str, Union[Map.Map, MapObjects.MapObjects]]:

        print(f'..create {cls}')
        factory = cls()

        scalar_nodes = node.value  # type: List[Tuple[yaml.ScalarNode]]
        if len(scalar_nodes) > 0:
            values = {}
            for node0, node1 in scalar_nodes:
                values[node0.value] = node_to_value(node1)

            print(f'....with values {values}')
            factory.set_values(values)

        return {'map': factory.get_map(), 'obj': factory.get_map_objects()}

    def __init__(self):
        self.map = None
        self.map_objects = None
        self.values = None

    def set_values(self, values: Dict[str, float]):
        #TODO create creatures?
        self.values = values

    def get_map(self):
        return self.map

    def get_map_objects(self):
        return self.map_objects


class EmptyMapFactory(MapFactory):
    yaml_tag = '!empty_map'

    def __init__(self):
        self.map = Map.Empty()
        self.map_objects = MapObjects.Empty(self.map)


class SpecialMapFactory(MapFactory):
    yaml_tag = '!special_map'

    def __init__(self):
        self.map = Map.Random()
        self.map_objects = MapObjects.Empty(self.map)


class EndMapFactory(MapFactory):
    yaml_tag = "!end_map"

    def __init__(self):
        self.map = Map.End()
        self.map_objects = MapObjects.Empty(self.map)


class RandomMapFactory(MapFactory):
    yaml_tag = "!random_map"

    def __init__(self):
        self.map = Map.Random()
        self.map_objects = MapObjects.Random(self.map, MapFactory.OBJECTS_CONFIG)
