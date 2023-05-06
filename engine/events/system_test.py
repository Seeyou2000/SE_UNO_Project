import pygame

from engine.events.system import EventSystem
from engine.gameobject import GameObject
from engine.gameobjectcontainer import GameObjectContainer


def test_hit_test_one() -> None:
    root = GameObjectContainer()
    root.rect = pygame.Rect(0, 0, 200, 200)

    target = GameObject()
    target.rect = pygame.Rect(50, 50, 50, 50)

    root.add_child(target)

    event_system = EventSystem(root)

    assert event_system.hit_test(pygame.Vector2(55, 55)) is target, "단일 대상 히트테스트"


def test_hit_test_nested() -> None:
    root = GameObjectContainer()
    root.rect = pygame.Rect(0, 0, 500, 500)
    root.update_absolute_rect()

    level1 = GameObjectContainer()
    level1.rect = pygame.Rect(50, 50, 400, 400)

    level2 = GameObjectContainer()
    level2.rect = pygame.Rect(50, 50, 300, 300)

    target = GameObject()
    target.rect = pygame.Rect(50, 50, 50, 50)

    root.add_child(level1)
    level1.add_child(level2)
    level2.add_child(target)

    event_system = EventSystem(root)

    hit_path = event_system.hit_test_recursive(
        event_system.root, pygame.Vector2(155, 155)
    )
    assert hit_path == [target, level2, level1, root]

    hit_target = event_system.hit_test(pygame.Vector2(155, 155))
    assert hit_target is target, "여러 레이어 히트테스트"


def test_hit_test_overlapped() -> None:
    root = GameObjectContainer()
    root.rect = pygame.Rect(0, 0, 500, 500)
    root.update_absolute_rect()

    level1 = GameObjectContainer()
    level1.rect = pygame.Rect(50, 50, 400, 400)

    level2 = GameObjectContainer()
    level2.rect = pygame.Rect(50, 50, 300, 300)

    target_sibling = GameObject()
    target_sibling.rect = pygame.Rect(25, 25, 50, 50)

    target = GameObject()
    target.rect = pygame.Rect(50, 50, 50, 50)

    root.add_child(level1)
    level1.add_child(level2)

    # target_sibling을 먼저 add해서 scene graph 상에서 target이 나중에 렌더링되도록 보장
    level2.add_child(target_sibling)
    level2.add_child(target)

    event_system = EventSystem(root)
    assert (
        event_system.hit_test(pygame.Vector2(130, 130)) is target_sibling
    ), "겹쳐 있을 때 아래에 그려지는 오브젝트의 온전히 보여지는 부분에 히트테스트"
    assert (
        event_system.hit_test(pygame.Vector2(150, 150)) is target
    ), "겹쳐 있을 때 위의 그려지는 오브젝트의 겹치지만 온전히 보여지는 부분에 히트테스트"
