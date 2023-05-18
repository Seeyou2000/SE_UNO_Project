from engine.world import World
from game.menu.menuscene import MenuScene


def main() -> None:
    world = World((800, 600), 120)
    world.story_clear_status.load()
    world.settings.load()
    world.achievements.load()
    world.director.change_scene(MenuScene(world))

    world.loop()


if __name__ == "__main__":
    main()
