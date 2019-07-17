from os import path as ospath
from abc import abstractmethod
from typing import Dict, Union, List, Tuple
from yaml import ScalarNode, MappingNode, YAMLObject, Loader, load as yaml_load

from Map import Map
from Object import MapObjects


class MapFactory(YAMLObject):

    MANIFEST = None

    @staticmethod
    def load_manifest():
        try:
            path = ospath.dirname(ospath.abspath(__file__))
            file = open(f"{path}/manifest.yml", "r")
            MapFactory.MANIFEST = yaml_load(file.read(), Loader=Loader)
            print(MapFactory.MANIFEST)
            file.close()
        except IOError as e:
            print(e)

    @staticmethod
    def node_to_value(node: ScalarNode) -> Union[str, float]:
        """
        Получить значение правильного типа из yaml.ScalarNode
        """
        _type = node.tag.split(':')[-1]
        if _type == 'int':
            return int(node.value)
        elif _type == 'float':
            return float(node.value)

        return node.value

    @classmethod
    def from_yaml(cls, loader, node: MappingNode) -> Dict[str, Union[Map.Map, MapObjects.MapObjects]]:

        print(f'..create {cls}')
        factory = cls()
        factory.init_map()

        scalar_nodes = node.value  # type: List[Tuple[ScalarNode]]
        if len(scalar_nodes) > 0:
            contents = {}
            for node0, node1 in scalar_nodes:
                contents[node0.value] = MapFactory.node_to_value(node1)

            print(f'....with values {contents}')
            factory.declare_objects(contents)

        factory.init_map_objects()

        return {'map': factory.get_map(), 'obj': factory.get_map_objects()}

    def __init__(self):
        self.map = None
        self.map_objects = None
        self.contents = None

    def declare_objects(self, values: Dict[str, float]) -> 'MapFactory':
        self.contents = values
        return self

    def get_map(self):
        return self.map

    def get_map_objects(self):
        return self.map_objects

    @abstractmethod
    def init_map(self):
        pass

    @abstractmethod
    def init_map_objects(self):
        pass


class EmptyMapFactory(MapFactory):
    yaml_tag = '!empty_map'

    def init_map(self):
        self.map = Map.Empty()
        self.map.init()

    def init_map_objects(self):
        self.map_objects = MapObjects.Empty(self.map)
        self.map_objects.init()


class SpecialMapFactory(MapFactory):
    yaml_tag = '!special_map'

    def init_map(self):
        self.map = Map.Random()
        self.map.init()

    def init_map_objects(self):
        self.map_objects = MapObjects.Empty(self.map)
        self.map_objects.init()


class RandomMapFactory(MapFactory):
    yaml_tag = "!random_map"

    def init_map(self):
        self.map = Map.Random()
        self.map.init()

    def init_map_objects(self):
        self.map_objects = MapObjects.Random(self.map)
        self.map_objects.init(manifest=MapFactory.MANIFEST, contents=self.contents)


class EndMapFactory(MapFactory):
    yaml_tag = "!end_map"

    def init_map(self):
        self.map = Map.End()
        self.map.init()

    def init_map_objects(self):
        self.map_objects = MapObjects.Empty(self.map)
        self.map_objects.init()
