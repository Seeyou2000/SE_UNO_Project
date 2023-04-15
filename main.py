from engine.world import World
from game.scene.menu import MenuScene


def main() -> None:
    world = World((800, 600), 60)
    world.director.change_scene(MenuScene(world))
<<<<<<< HEAD
    world.load_settings()
=======
    world.settings.load()
>>>>>>> 6245d18a75cbe7f80686b914df9574cbf60fc067

    world.loop()


if __name__ == "__main__":
    main()
