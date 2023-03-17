import pygame
from engine.button import Button
from engine.scene import Scene
from engine.sprite import Sprite
from engine.world import World

class InGameScene(Scene):
    def __init__(self, world: World):
        super().__init__(world)

        self.sprite = Sprite(pygame.image.load('resources/uno.jpg'))

        from game.scene.menu import MenuScene
        menu_button = Button('Back to menu', pygame.Rect(10, 10, 200, 100), pygame.font.SysFont('Arial', 20), lambda event: self.world.director.change_scene(MenuScene(self.world)))
        
        self.children.extend([
            self.sprite,
            menu_button
        ])

    def update(self):
        super().update()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.sprite.rect.left -= 5
        if pressed[pygame.K_RIGHT]:
            self.sprite.rect.right += 5
        if pressed[pygame.K_UP]:
            self.sprite.rect.top -= 5
        if pressed[pygame.K_DOWN]:
            self.sprite.rect.bottom += 5
        