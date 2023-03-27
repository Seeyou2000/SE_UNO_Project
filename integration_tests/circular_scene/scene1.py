from engine.scene import Scene


class Scene1(Scene):
    def open_scene2(self) -> None:
        from integration_tests.circular_scene.scene2 import Scene2

        self.world.director.change_scene(Scene2(self.world))
