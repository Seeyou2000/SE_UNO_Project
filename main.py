from engine.world import World
from game.scene.menu import MenuScene

def main():
    world = World((800, 600), 60)
    world.director.change_scene(MenuScene(world))

    world.loop()

if __name__ == '__main__':
    main()