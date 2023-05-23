import asyncio

from engine.world import World
from game.menu.menuscene import MenuScene
from network.server.server import run_server


def main() -> None:
    world = World((800, 600), 120)
    world.story_clear_status.load()
    world.settings.load()
    world.achievements.load()
    world.director.change_scene(MenuScene(world))

    # run_server(world.loop)
    asyncio.run(world.loop(None))


if __name__ == "__main__":
    main()
