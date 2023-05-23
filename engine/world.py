import asyncio
import sys

import pygame
import tween

from engine.events.event import Event
from engine.scene import SceneDirector
from game.achievements import Achievements
from game.audio_player import AudioPlayer
from game.gameplay.timer import Timer
from game.settings.settings import Settings
from game.storyclearstatus import StoryClearStatus
from network.client.client import Client

AUDIO_PLAYER: AudioPlayer = AudioPlayer()


class World:
    screen: pygame.Surface
    director: SceneDirector
    clock: pygame.time.Clock
    target_fps: float
    settings: Settings
    achievements: Achievements
    story_clear_status: StoryClearStatus
    client: Client

    def __init__(self, size: tuple[float, float], target_fps: float = 60) -> None:
        pygame.init()
        self.director = SceneDirector()
        self.set_size(size)
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps
        self.settings = Settings()
        self.settings.on("change", self.handle_settings_change)
        self.achievements = Achievements()
        self.achievements.on("clear", self.handle_achievements_clear)
        self.audio_player = AudioPlayer(self.settings)
        self.audio_player.play_bg_music()
        self.achieve_clear = False
        self.cleared_achieve_name = ""
        self.show_timer = Timer(5)
        global AUDIO_PLAYER
        AUDIO_PLAYER.play_bg_music()
        self.settings.on("change", AUDIO_PLAYER.handle_settings_change)

        self.audio_player = AUDIO_PLAYER
        self.achievements = Achievements()
        self.story_clear_status = StoryClearStatus()

        self.client = Client()
        self.client.on("room_state_changed", self.handle_room_state_changed)

        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    def set_size(self, size: tuple[float, float]) -> None:
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        current_scene = self.director.get_current()
        if current_scene is not None:
            current_scene.emit("resize", Event(None))

    def get_rect(self) -> pygame.Rect:
        return self.screen.get_rect()

    async def loop(self, _: any) -> None:
        while True:
            self.update()
            self.render()
            await asyncio.sleep(0)

    def update(self) -> None:
        self.handle_event()
        dt = self.clock.tick(self.target_fps) / 1000.0
        self.director.get_current().update(dt)
        tween.update(dt)
        self.show_timer.update(dt)

    def render(self) -> None:
        self.screen.fill(pygame.Color("#FFF6EF"))
        self.director.get_current().render(self.screen)
        self.real_time_achieve_clear(self.cleared_achieve_name)
        pygame.display.flip()

    def handle_event(self) -> None:
        current_scene = self.director.get_current()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.exit()
                case pygame.MOUSEBUTTONDOWN:
                    current_scene.event_system.handle_mouse_down(event)
                case pygame.MOUSEBUTTONUP:
                    current_scene.event_system.handle_mouse_up(event)
                case pygame.MOUSEMOTION:
                    current_scene.event_system.handle_mouse_move(event)
                case pygame.KEYDOWN:
                    current_scene.emit("keydown", Event(event.dict))
                case pygame.TEXTEDITING:
                    current_scene.emit("textediting", Event(event.dict))
                case pygame.TEXTINPUT:
                    current_scene.emit("textinput", Event(event.dict))
                case pygame.WINDOWRESIZED:
                    event_width = event.dict["x"]
                    event_height = event.dict["y"]
                    clipped_width = max(1280, event_width)
                    clipped_height = max(720, event_height)
                    self.set_size((clipped_width, clipped_height))

    def handle_settings_change(self, _: Event) -> None:
        self.set_size(self.settings.window_size)

    def handle_achievements_clear(self, _: Event) -> None:
        self.show_timer.update(0)
        self.show_timer = Timer(5)
        self.show_timer.on("tick", self.reset_show_achieve)

    def real_time_achieve_clear(self, achieve: str = "") -> None:
        screen_size = self.get_rect()
        if achieve == "win_less_10turn":
            pygame.draw.rect(
                self.screen,
                [255, 232, 214],
                [screen_size.right - 400, screen_size.bottom - 100, 400, 100],
            )
            self.achieve_img = pygame.image.load(
                "resources/images/unoarchieve_temp.jpg"
            )
            self.screen.blit(
                self.achieve_img, (screen_size.right - 400, screen_size.bottom - 100)
            )
        self.font = pygame.font.SysFont("resources/fonts/GmarketSansTTFMedium.ttf", 30)
        self.clear_achieve_text = self.font.render(achieve, True, pygame.Color("black"))
        self.screen.blit(
            self.clear_achieve_text, (screen_size.right - 290, screen_size.bottom - 58)
        )

    def reset_show_achieve(self, event: Event) -> None:  # 실시간 업적표시 타이머&텍스트 초기화
        self.cleared_achieve_name = ""
        self.achieve_clear = False

    def handle_room_state_changed(self, event: Event) -> None:
        from game.room.roomscene import RoomScene

        if isinstance(self.director.get_current(), RoomScene):
            return

        self.director.change_scene(RoomScene(self, event.data["room"]))

    def exit(self) -> None:
        self.client.io.disconnect()
        pygame.quit()
        sys.exit()
