import json
from dataclasses import dataclass
from typing import Any

import pygame

from engine.events.emitter import EventEmitter
from engine.events.event import Event

ACHIEVEMENTS_FILE_PATH = "achievements.json"
DEFAULT_ACHIEVEMENTS = {
    "win_less_10turn": [False, None],
    "win_single_play": [False, None],
    "win_never_use_ability": [False, None],
    "win_other_player_press_uno": [False, None],
    "???1": [False, None],
    "???2": [False, None],
    "???3": [False, None],
    "win_area1": [False, None],
    "win_area2": [False, None],
    "win_area3": [False, None],
    "win_area4": [False, None],
}


@dataclass
class Achievement:
    icon: pygame.Surface
    title: str
    description: str


ACHIEVEMENT_DATA = {
    "win_less_10turn": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "10턴 안에 승리",
        "10턴 내로 승리시 획득",
    ),
    "win_single_play": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "싱글플레이에서 승리",
        "싱글플레이에서 1회 승리시 획득",
    ),
    "win_never_use_ability": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "능력 카드 사용하지 않고 승리",
        "게임 진행 중 능력 카드를 사용하지 않고 승리시 획득",
    ),
    "win_other_player_press_uno": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "다른 플레이어가 UNO를 선언한 뒤 승리",
        "다른 플레이어가 UNO를 선언한 상태에서 승리시 획득",
    ),
    "???1": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "???",
        "~~~",
    ),
    "???2": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "???",
        "~~~",
    ),
    "???3": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "???",
        "~~~",
    ),
    "win_area1": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "스테이지1 클리어",
        "AREA1에서 승리시 획득",
    ),
    "win_area2": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "스테이지2 클리어",
        "AREA2에서 승리시 획득",
    ),
    "win_area3": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "스테이지3 클리어",
        "AREA3에서 승리시 획득",
    ),
    "win_area4": Achievement(
        pygame.image.load("resources/images/unoarchieve_temp.jpg"),
        "스테이지4 클리어",
        "AREA4에서 승리시 획득",
    ),
}


class Achievements(EventEmitter):
    _win_less_10turn: list

    def __init__(self) -> None:
        super().__init__()
        self.achieve_clear = False

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
            print("기존 업적 파일을 찾지 못했습니다. 새 업적 파일을 만듭니다.")
            self.reset()

    def load_dict(self, value: dict[str, Any]) -> None:
        try:
            self.set_values(
                win_less_10turn=value["win_less_10turn"],
            )
        except (AttributeError, KeyError) as e:
            raise e
            if value is DEFAULT_ACHIEVEMENTS:
                print("기본 업적값을 불러오는 데 문제가 있습니다. 키값을 점검하세요.")
            else:
                print("저장된 업적을 불러오는 데 문제가 있어 기본 업적값으로 대체합니다.")
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
        if self.achieve_clear is True:
            self.emit("clear", Event(target=self))

    def reset(self) -> None:
        self.load_dict(DEFAULT_ACHIEVEMENTS)
