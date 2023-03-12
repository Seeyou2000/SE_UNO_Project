from engine.world import World
from game.scene.menu import MenuScene, InGameScene

def main():
    world = World((800, 600), 60)
    world.director.add(MenuScene(world))
    world.director.change_scene(MenuScene)

    world.director.add(InGameScene(world))

    world.loop()

if __name__ == '__main__':
    main()