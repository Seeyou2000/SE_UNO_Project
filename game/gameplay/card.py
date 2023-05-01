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

    def __str__(self) -> str:
        return f"[카드 색: {self.color}, 숫자: {self.number}, 능력: {self.ability}]"

    def info(self) -> str:  # gamestate_test.py 파일에서 모든 카드가 정상적으로 생성되는지 확인하기 위해 사용
        return f"[카드 색: {self.color}, 숫자: {self.number}, 능력: {self.ability}]"
