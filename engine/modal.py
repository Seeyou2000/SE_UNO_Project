import pygame

from engine.events.emitter import EventEmitter
from engine.events.event import Event
from engine.focus import FocusController, FocusMoveDirection
from engine.gameobjectcontainer import GameObjectContainer
from engine.scene import Scene
from engine.sprite import Sprite


class Modal(GameObjectContainer):
    def __init__(self, size: tuple[int, int], scene: Scene) -> None:
        super().__init__()

        self.scene = scene
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.surface,
            pygame.Color("#fff1e7"),
            self.surface.get_rect(),
            border_radius=5,
        )
        background = Sprite(self.surface)
        self.add_child(background)
        self.focus_controller = FocusController()
        self.rect = background.rect.copy()

        scene.on("keydown", self.handle_focus_keydown)
        scene.on("textinput", self.handle_textinput)

    def handle_focus_keydown(self, event: Event) -> None:
        pressed_key: int = event.data["key"]

        match pressed_key:
            case pygame.K_UP:
                self.focus_controller.move_focus(FocusMoveDirection.UP)
            case pygame.K_DOWN:
                self.focus_controller.move_focus(FocusMoveDirection.DOWN)
            case pygame.K_LEFT:
                self.focus_controller.move_focus(FocusMoveDirection.LEFT)
            case pygame.K_RIGHT:
                self.focus_controller.move_focus(FocusMoveDirection.RIGHT)

        if isinstance(self.focus_controller.current_focus, EventEmitter):
            self.focus_controller.current_focus.emit("keydown", event)
            
    def handle_textinput(self, event: Event) -> None:
        if isinstance(self.focus_controller.current_focus, EventEmitter):
            self.focus_controller.current_focus.emit("textinput", event)

    def close(self) -> None:
        self.scene.close_modal(self)
        self.scene.off("keydown", self.handle_focus_keydown)
