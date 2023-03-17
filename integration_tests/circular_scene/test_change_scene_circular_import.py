import pytest

from engine.world import World
from integration_tests.circular_scene.scene1 import Scene1

@pytest.fixture(scope='module')
def world():
    world = World((0, 0), 60)
    yield world

def test_change_scene(world: World):
    '''
    문제가 있다면 circular import 에러로 테스트 실행 자체가 터지거나 NameError가 raise된다.
    '''
    scene1 = Scene1(world)
    world.director.change_scene(scene1)
    scene1.open_scene2()
