from engine.scene import Scene


class Scene2(Scene):
    def open_scene1(self):
        from integration_tests.circular_scene.scene1 import Scene1
        self.world.director.change_scene(Scene1(self.world))