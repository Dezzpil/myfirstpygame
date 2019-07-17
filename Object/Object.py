from abc import ABC, abstractmethod
import pygame
import random
from typing import Any, Tuple, Callable


class AbstractObject(ABC):
    def __init__(self, stats: dict):
        self.stats = stats


class Drawable(AbstractObject):
    @abstractmethod
    def draw(self, display: pygame.display, icon: pygame.Surface, position: Tuple[int]):
        pass

    @staticmethod
    def create_sprite(img_path: str, sprite_size: int) -> pygame.Surface:
        icon = pygame.image.load(img_path).convert_alpha()
        icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
        sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
        sprite.blit(icon, (0, 0))
        return sprite


class Interactive(Drawable):

    def set_action(self, action: Callable) -> 'Interactive':
        self.action = action
        return self

    @abstractmethod
    def interact(self, engine: GameEngine, hero: Hero):
        self.action(engine, hero)


class Stairs(Interactive):
    pass


class Ally(Interactive):
    def interact(self, engine, hero):
        pass

    def draw(self, display: pygame.display, icon: pygame.Surface, position: Tuple[int]):
        pass


class Creature(Interactive):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    def draw(self, display):
        # FIXME
        pass


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Enemy(Creature):
    pass