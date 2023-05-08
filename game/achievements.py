import json
from typing import Any

from engine.events.emitter import EventEmitter
from engine.events.event import Event

ACHIEVEMENTS_FILE_PATH = "achievements.json"
DEFAULT_ACHIEVEMENTS = {
    "win_less_10turn": [False, None],
}


class Achievements(EventEmitter):
    _win_less_10turn: list

    def __init__(self) -> None:
        super().__init__()
        pass

    def save(self) -> None:
        with open(ACHIEVEMENTS_FILE_PATH, "w") as f:
            json.dump(
                {
                    "win_less_10turn": self.win_less_10turn,
                },
                f,
            )

    def load(self) -> None:
        try:
            with open(ACHIEVEMENTS_FILE_PATH) as f:
                self.load_dict(json.load(f))
        except FileNotFoundError:
            print("기존 설정 파일을 찾지 못했습니다. 새 설정 파일을 만듭니다.")
            self.reset()

    def load_dict(self, value: dict[str, Any]) -> None:
        try:
            self.set_values(
                win_less_10turn=value["win_less_10turn"],
            )
        except (AttributeError, KeyError) as e:
            raise e
            if value is DEFAULT_ACHIEVEMENTS:
                print("기본 설정값을 불러오는 데 문제가 있습니다. 키값을 점검하세요.")
            else:
                print("저장된 설정을 불러오는 데 문제가 있어 기본 설정값으로 대체합니다.")
                self.reset()

    @property
    def win_less_10turn(self) -> list:
        return self._win_less_10turn

    def set_values(
        self,
        win_less_10turn: list | None = None,
    ) -> None:
        self._win_less_10turn = (
            win_less_10turn if win_less_10turn is not None else self._win_less_10turn
        )
        self.save()
        self.emit("change", Event(target=self))
