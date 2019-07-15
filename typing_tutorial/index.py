from typing import TypeVar, Sequence, List, Optional, Tuple
import random


Chooseable = TypeVar('Chooseable', str, float)


def choose(items: Sequence[Chooseable]) -> Chooseable:
    return random.choice(items)


reveal_type(choose(["Guido", "Jukka", "Ivan"]))  # mypy
reveal_type(choose([1, 2, 3]))  # mypy
reveal_type(choose([True, 42, 3.14]))  # mypy
reveal_type(choose(["Python", 3, 7]))  # mypy

xs: List[Optional[str]] = []
xs.append(1)


def test() -> List[str]:
    return [0]


Card = Tuple[str, str]
Deck = List[Card]


def test1(default=[]):
    default.append(1)
    return default

