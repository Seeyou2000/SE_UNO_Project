import pygame
import socketio
from loguru import logger

from engine.events.event import Event
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World
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

        sprite = Sprite(pygame.image.load("resources/uno.jpg"))

        button_list = [
            MenuButton(
                "Single Play",
                button_size,
                lambda _: world.director.change_scene(LobbyScene(world)),
            ),
            MenuButton(
                "Story Mode",
                button_size,
                lambda _: world.director.change_scene(StoryModeSelectScene(world)),
            ),
            MenuButton(
                "Multi Play",
                button_size,
                self.change_to_multiplay,
            ),
            MenuButton(
                "Settings",
                button_size,
                lambda _: world.director.change_scene(SettingScene(world)),
            ),
            MenuButton(
                "Exit",
                button_size,
                lambda _: world.exit(),
            ),
        ]

        self.layout.add(sprite, pygame.Vector2(0.5, 0.5), pygame.Vector2(0, -130))

        for i, item in enumerate(button_list):
            self.layout.add(
                item, pygame.Vector2(0.5, 0.5), pygame.Vector2(0, 60 * i + 80)
            )
            self.focus_controller.add(item)

        self.add_children([sprite] + button_list)

        self.on("keydown", self.handle_keydown)

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
