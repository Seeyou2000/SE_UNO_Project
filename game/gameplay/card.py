from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin

from game.constant import AbilityType


@dataclass
class Card(DataClassJsonMixin):
    color: str
    number: int | None = None
    ability: AbilityType | None = None

    def __str__(self) -> str:
        return f"[카드 색: {self.color}, 숫자: {self.number}, 능력: {self.ability}]"
