import math

import pygame
import socketio
from loguru import logger

from engine.events.event import Event
from engine.layout import LayoutAnchor, LayoutConstraint, Vertical
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World
from game.achievementscene import AchievementScene
from game.lobby.lobbyscene import LobbyScene
from game.lobby.multilobbyscene import MultiLobbyScene
from game.menu.menubutton import MenuButton
from game.messagemodal import MessageModal
from game.networktest.networktestscene import NetworkTestScene
from game.storyselect.storymodeselectscene import StoryModeSelectScene
from network.client.client import clientio


class MenuScene(Scene):
    def __init__(self, world: World) -> None:
        super().__init__(world)
        from game.settings.settingscene import SettingScene

        button_size = pygame.Vector2(200, 60)

        self.background_tile_surface = pygame.image.load(
            "resources/images/background-tile.png"
        )
        self.background_tile_rect = self.background_tile_surface.get_rect()
        self.background_surface = pygame.Surface(
            (self.background_tile_rect.width, self.background_tile_rect.height * 2),
            pygame.SRCALPHA,
        )

        self.logo = Sprite(pygame.image.load("resources/images/logo.png"))
        self.add(
            self.logo,
            LayoutConstraint(LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-200, 0)),
        )

        self.logo_icon = Sprite(pygame.image.load("resources/images/logo-icon.png"))
        self.add(
            self.logo_icon,
            LayoutConstraint(LayoutAnchor.MIDDLE_RIGHT, pygame.Vector2(-500, -80)),
        )

        button_list = [
            MenuButton(
                "싱글플레이",
                button_size,
                lambda _: world.director.change_scene(LobbyScene(world)),
            ),
            MenuButton(
                "스토리",
                button_size,
                lambda _: world.director.change_scene(StoryModeSelectScene(world)),
            ),
            MenuButton(
                "멀티플레이",
                button_size,
                self.change_to_multiplay,
            ),
            MenuButton(
                "업적",
                button_size,
                lambda _: world.director.change_scene(AchievementScene(world)),
            ),
            MenuButton(
                "설정",
                button_size,
                lambda _: world.director.change_scene(SettingScene(world)),
            ),
            MenuButton(
                "나가기",
                button_size,
                lambda _: world.exit(),
            ),
        ]

        for item in button_list:
            self.focus_controller.add(item)

        menu_area = Vertical(pygame.Vector2(), 10, button_list)
        self.add(
            menu_area, LayoutConstraint(LayoutAnchor.MIDDLE_LEFT, pygame.Vector2(40, 0))
        )

        self.time = 0

        self.on("keydown", self.handle_keydown)

    def update(self, dt: float) -> None:
        super().update(dt)
        self.time += dt

        self.layout.get_constraint(self.logo).margin.y = math.sin(self.time * 3) * 6
        self.layout.get_constraint(self.logo_icon).margin.y = (
            -80 + math.sin(self.time * 3 + 1) * 4
        )

    def render(self, surface: pygame.Surface) -> None:
        upper_y = (
            self.time * 120 % self.background_tile_rect.height
        ) - self.background_tile_rect.height
        self.background_surface.fill((0, 0, 0, 0))
        self.background_surface.blit(self.background_tile_surface, (0, upper_y))
        self.background_surface.blit(
            self.background_tile_surface,
            (0, upper_y + self.background_tile_rect.height),
        )
        surface.blit(
            pygame.transform.rotate(self.background_surface, -10),
            (self.rect.right - 1000, -150),
        )
        super().render(surface)

    def handle_keydown(self, e: Event) -> None:
        if e.data["key"] == pygame.K_n:
            self.world.director.change_scene(NetworkTestScene(self.world))

    def change_to_multiplay(self, e: Event) -> None:
        if self.try_connect("http://127.0.0.1:10008"):
            self.world.director.change_scene(MultiLobbyScene(self.world))

    def try_connect(self, server_ip: str) -> bool:
        try:
            clientio.connect(server_ip, auth={"username": "Test Player"})

        except socketio.client.exceptions.ConnectionError as e:
            self.open_modal(MessageModal(self, "서버에 접속하지 못했습니다."))
            logger.error(f"방 접속 실패 {e}")
            return False

        return True
