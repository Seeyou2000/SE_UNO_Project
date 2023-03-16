from engine.world import World
from game.scene.menu import MenuScene, InGameScene, InGameScene2

def main():
    world = World((800, 600), 60)
    world.director.add(MenuScene(world))
    world.director.change_scene(MenuScene)

    world.director.add(InGameScene(world))
    world.director.add(InGameScene2(world))

    world.loop()

if __name__ == '__main__':
    main()