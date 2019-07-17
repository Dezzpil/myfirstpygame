import pygame
import random
import yaml
import os
# import Objects
from GameEngine import GameEngine
from Objects import Hero, Blessing, Berserk, Weakness
from typing import NoReturn, List, Dict, TypeVar

TService = TypeVar('TService', bound='Service')

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


class Service:

    def __init__(self):
        self.levels = []

    def set_levels(self, levels: List[dict]) -> TService:
        self.levels = levels
        return self

    # def reload_game(self, engine: GameEngine, hero: Hero) -> NoReturn:
    #     level_list_max = len(self.levels) - 1
    #     engine.level += 1
    #     hero.position = [1, 1]
    #     engine.objects = []
    #     generator = self.levels[min(engine.level, level_list_max)]
    #     _map = generator['map'].create_map()
    #     engine.load_map(_map)
    #     engine.add_objects(generator['obj'].get_objects(_map))
    #     engine.set_hero(hero)
    #
    # @staticmethod
    # def create_sprite(img: str, sprite_size: int) -> pygame.Surface:
    #     icon = pygame.image.load(img).convert_alpha()
    #     icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    #     sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    #     sprite.blit(icon, (0, 0))
    #     return sprite
    #
    # @staticmethod
    # def restore_hp(engine: GameEngine, hero: Hero):
    #     engine.score += 0.1
    #     hero.hp = hero.max_hp
    #     engine.notify("HP restored")
    #
    # @staticmethod
    # def apply_blessing(engine: GameEngine, hero: Hero):
    #     if hero.gold >= int(20 * 1.5**engine.level) - 2 * hero.stats["intelligence"]:
    #         engine.score += 0.2
    #         hero.gold -= int(20 * 1.5**engine.level) - \
    #             2 * hero.stats["intelligence"]
    #         if random.randint(0, 1) == 0:
    #             engine.hero = Blessing(hero)
    #             engine.notify("Blessing applied")
    #         else:
    #             engine.hero = Berserk(hero)
    #             engine.notify("Berserk applied")
    #     else:
    #         engine.score -= 0.1
    #
    # @staticmethod
    # def remove_effect(engine: GameEngine, hero: Hero):
    #     if hero.gold >= int(10 * 1.5**engine.level) - 2 * hero.stats["intelligence"] and "base" in dir(hero):
    #         hero.gold -= int(10 * 1.5**engine.level) - \
    #             2 * hero.stats["intelligence"]
    #         engine.hero = hero.base
    #         engine.hero.calc_max_HP()
    #         engine.notify("Effect removed")
    #
    # @staticmethod
    # def add_gold(engine: GameEngine, hero: Hero):
    #     if random.randint(1, 10) == 1:
    #         engine.score -= 0.05
    #         engine.hero = Weakness(hero)
    #         engine.notify("You were cursed")
    #     else:
    #         engine.score += 0.1
    #         gold = int(random.randint(10, 1000) * (1.1**(engine.hero.level - 1)))
    #         hero.gold += gold
    #         engine.notify(f"{gold} gold added")


# FIXME
# add classes for YAML !empty_map and !special_map{}

wall = [0]
floor1 = [0]
floor2 = [0]
floor3 = [0]


def service_init(sprite_size, full=True):
    global object_list_prob, level_list

    global wall
    global floor1
    global floor2
    global floor3

    wall[0] = create_sprite(os.path.join("texture", "wall.png"), sprite_size)
    floor1[0] = create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
    floor2[0] = create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
    floor3[0] = create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)

    file = open("objects.yml", "r")

    object_list_tmp = yaml.load(file.read())
    if full:
        object_list_prob = object_list_tmp

    object_list_actions = {'reload_game': reload_game,
                           'add_gold': add_gold,
                           'apply_blessing': apply_blessing,
                           'remove_effect': remove_effect,
                           'restore_hp': restore_hp}

    for obj in object_list_prob['objects']:
        prop = object_list_prob['objects'][obj]
        prop_tmp = object_list_tmp['objects'][obj]
        prop['sprite'][0] = create_sprite(
            os.path.join(OBJECT_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for ally in object_list_prob['ally']:
        prop = object_list_prob['ally'][ally]
        prop_tmp = object_list_tmp['ally'][ally]
        prop['sprite'][0] = create_sprite(
            os.path.join(ALLY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for enemy in object_list_prob['enemies']:
        prop = object_list_prob['enemies'][enemy]
        prop_tmp = object_list_tmp['enemies'][enemy]
        prop['sprite'][0] = create_sprite(
            os.path.join(ENEMY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)

    file.close()

    if full:
        file = open("levels.yml", "r")
        level_list = yaml.load(file.read())['levels']
        level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
        file.close()
