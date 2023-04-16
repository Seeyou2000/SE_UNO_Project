from engine.gameobjectcontainer import GameObjectContainer
from game.constant import AbilityType


class Card(GameObjectContainer):
    def __init__(
        self,
        color: str,
        number: int | None = None,
        ability: AbilityType | None = None,
    ) -> None:  # 일반 숫자 카드
        super().__init__()
        self.color = color
        self.number = number
        self.ability = ability
