import sys

import pygame

from engine.event import Event
from engine.scene import SceneDirector
from game.settings.settings import Settings


class World:
    screen: pygame.Surface
    director: SceneDirector
    clock: pygame.time.Clock
    target_fps: float
    settings: Settings

    def __init__(self, size: tuple[float, float], target_fps: float = 60) -> None:
        pygame.init()
        self.director = SceneDirector()
        self.set_size(size)
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps
<<<<<<< HEAD
        self.is_colorblind = None
        self.settings = {
            "size": (800, 600),
            "colorblind": False,
            # add any other settings later to save here
        }
        self.load_settings()
=======
        self.settings = Settings()
        self.settings.on("change", self.handle_settings_change)
>>>>>>> 6245d18a75cbe7f80686b914df9574cbf60fc067

    def set_size(self, size: tuple[float, float]) -> None:
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        current_scene = self.director.get_current()
        if current_scene is not None:
            current_scene.emit("resize", Event(None))

    def get_rect(self) -> pygame.Rect:
        return self.screen.get_rect()

    def loop(self) -> None:
        while True:
            self.update()
            self.render()

    def update(self) -> None:
        self.handle_event()
        self.director.get_current().update()
        self.clock.tick(self.target_fps)

    def render(self) -> None:
        self.screen.fill(pygame.Color("white"))
        self.director.get_current().render(self.screen)
        pygame.display.flip()

    def handle_event(self) -> None:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    self.director.get_current().emit("mouse_down", Event(event.dict))
                case pygame.MOUSEMOTION:
                    self.director.get_current().emit("mouse_move", Event(event.dict))
<<<<<<< HEAD

        # Minghui Xu

    def toggle_set_colorblind(self, is_colorblind) -> None:
        self.is_colorblind = is_colorblind

        if is_colorblind:
            # colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
            # pygame.display.set_palette(colors)
            pass
        else:
            # colors = [(255, 255, 255), (0, 0, 0), (128, 128, 128)]
            # pygame.display.set_palette(None)
            pass

    def reset(self):
        self.set_size((1280, 720))

    def save_settings(self):
        with open("settings.txt", "w") as f:
            f.write(repr(self.settings))

    def load_settings(self):
        try:
            with open("settings.txt", "r") as f:
                self.settings = eval(f.read())
        except FileNotFoundError:
            pass
=======
                case pygame.WINDOWRESIZED:
                    event_width = event.dict["x"]
                    event_height = event.dict["y"]
                    clipped_width = max(800, event_width)
                    clipped_height = max(600, event_height)
                    self.set_size((clipped_width, clipped_height))

    def handle_settings_change(self, _: Event) -> None:
        self.set_size(self.settings.window_size)
>>>>>>> 6245d18a75cbe7f80686b914df9574cbf60fc067
