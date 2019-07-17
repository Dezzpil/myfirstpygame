import yaml
from map import Factory

if __name__ == '__main__':

    Factory.MapFactory.load_manifest()

    file = open("map/levels.yml", "r")
    level_list = yaml.load(file.read(), Loader=yaml.Loader)['levels']
    file.close()

    exit()