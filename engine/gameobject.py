import abc
from typing import Self

import pygame

from engine.events.emitter import EventEmitter


class GameObject(EventEmitter, abc.ABC):
    """
    발생할 수 있는 이벤트
    mouse_down: 이 오브젝트의 absolute_rect 범위에서 마우스 버튼 누름이 일어난 경우 한 번 발생
    mouse_up: 이 오브젝트의 absolute_rect 범위에서 마우스 버튼 뗌이 일어난 경우 한 번 발생
    mouse_move: 이 오브젝트의 absolute_rect 범위에서 마우스 움직임이 일어난 경우 항상 발생
    mouse_enter: 이 오브젝트의 absolute_rect 범위에 마우스가 들어오는 그 시점에 한 번 발생, 버블링 없음
    mouse_leave: 이 오브젝트의 absolute_rect 범위 안에 마우스 커서가 있다가 빠져나가는 그 시점에 한 번 발생, 버블링 없음
    mouse_over: mouse_enter와 같지만 버블링 있음
    mouse_out: mouse_leave와 같지만 버블링 있음
    click: mouse_down과 mouse_up이 같은 객체에서 일어났을 때에만 한 번 발생
    """

    rect: pygame.Rect
    parent: Self
    absolute_rect: pygame.Rect
    is_visible: bool

    def __init__(self) -> None:
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.absolute_rect = self.rect.copy()

        self.is_visible = True

    def update(self, dt: float) -> None:
        if not self.is_visible:
            return
        self.update_absolute_rect()

    def render(self, surface: pygame.Surface) -> None:
        pass

    def update_absolute_rect(self) -> None:
        if self.parent is None:
            self.absolute_rect = self.rect.copy()
        else:
            self.absolute_rect = self.rect.move(self.parent.absolute_rect.topleft)
