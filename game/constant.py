from enum import Enum, auto


class ColorableAbilityType(Enum):
    GIVE_TWO_CARDS = 1
    GIVE_FOUR_CARDS = auto()
    SKIP_ORDER = auto()
    REVERSE_ORDER = auto()


class NonColorableAbilityType(Enum):
    # 우주방어
    # 스킵
    # 그냥 방어없이 무지성 카드 주기 <- 열받는용도
    CHANGE_CARD_COLOR = 100


AbilityType = ColorableAbilityType | NonColorableAbilityType


COLORS = ["red", "yellow", "green", "blue"]
NAME = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX"]
