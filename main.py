from engine.world import World
from game.menu.menuscene import MenuScene


def main() -> None:
    world = World((800, 600), 120)
    world.settings.load()
    world.director.change_scene(MenuScene(world))

    world.loop()


if __name__ == "__main__":
    main()
