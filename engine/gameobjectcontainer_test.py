import pygame

from engine.gameobject import GameObject
from engine.gameobjectcontainer import GameObjectContainer


def test_absolute_rect() -> None:
    level1 = GameObjectContainer()
    level1.rect = pygame.Rect(50, 50, 200, 200)
    level1.update_absolute_rect()

    level2 = GameObjectContainer()
    level2.rect = pygame.Rect(50, 50, 100, 100)

    target = GameObject()
    target.rect = pygame.Rect(50, 50, 50, 50)

    level1.add_child(level2)
    level2.add_child(target)

    assert level1.absolute_rect == pygame.Rect(50, 50, 200, 200)
    assert level2.absolute_rect == pygame.Rect(100, 100, 100, 100)
    assert target.absolute_rect == pygame.Rect(150, 150, 50, 50)
    assert target.absolute_rect.collidepoint(pygame.Vector2(155, 155))
