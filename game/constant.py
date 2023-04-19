from enum import Enum, auto


class AbilityType(Enum):
    GIVE_TWO_CARDS = 1
    GIVE_FOUR_CARDS = auto()
    SKIP_ORDER = auto()
    REVERSE_ORDER = auto()
    CHANGE_CARD_COLOR = 100
    ABSOULTE_ATTACK = auto()
    ABSOULTE_PROTECT = auto()


COLORABLEABILITY = [
    AbilityType.GIVE_TWO_CARDS,
    AbilityType.GIVE_FOUR_CARDS,
    AbilityType.SKIP_ORDER,
    AbilityType.REVERSE_ORDER,
]

NONCOLORABLEABILITY = [
    AbilityType.CHANGE_CARD_COLOR,
    AbilityType.ABSOULTE_ATTACK,
    AbilityType.ABSOULTE_PROTECT,
]

COLORS = ["red", "yellow", "green", "blue"]
NAME = ["PLAYER", "AI 1", "AI 2", "AI 3", "AI 4", "AI 5"]
