import pygame
import random
from GameEngine import GameEngine
from Object.Object import Hero
from Object.Effect import Blessing, Berserk, Weakness
from typing import NoReturn, List, Dict, TypeVar


def reload_game(self, engine: GameEngine, hero: Hero) -> NoReturn:
    level_list_max = len(self.levels) - 1
    engine.level += 1
    hero.position = [1, 1]
    engine.objects = []
    generator = self.levels[min(engine.level, level_list_max)]
    _map = generator['map'].create_map()
    engine.load_map(_map)
    engine.add_objects(generator['obj'].get_objects(_map))
    engine.set_hero(hero)


@staticmethod
def create_sprite(img: str, sprite_size: int) -> pygame.Surface:
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


@staticmethod
def restore_hp(engine: GameEngine, hero: Hero):
    engine.score += 0.1
    hero.hp = hero.max_hp
    engine.notify("HP restored")


@staticmethod
def apply_blessing(engine: GameEngine, hero: Hero):
    if hero.gold >= int(20 * 1.5 ** engine.level) - 2 * hero.stats["intelligence"]:
        engine.score += 0.2
        hero.gold -= int(20 * 1.5 ** engine.level) - \
                     2 * hero.stats["intelligence"]
        if random.randint(0, 1) == 0:
            engine.hero = Blessing(hero)
            engine.notify("Blessing applied")
        else:
            engine.hero = Berserk(hero)
            engine.notify("Berserk applied")
    else:
        engine.score -= 0.1


@staticmethod
def remove_effect(engine: GameEngine, hero: Hero):
    if hero.gold >= int(10 * 1.5 ** engine.level) - 2 * hero.stats["intelligence"] and "base" in dir(hero):
        hero.gold -= int(10 * 1.5 ** engine.level) - \
                     2 * hero.stats["intelligence"]
        engine.hero = hero.base
        engine.hero.calc_max_HP()
        engine.notify("Effect removed")


@staticmethod
def add_gold(engine: GameEngine, hero: Hero):
    if random.randint(1, 10) == 1:
        engine.score -= 0.05
        engine.hero = Weakness(hero)
        engine.notify("You were cursed")
    else:
        engine.score += 0.1
        gold = int(random.randint(10, 1000) * (1.1 ** (engine.hero.level - 1)))
        hero.gold += gold
        engine.notify(f"{gold} gold added")
