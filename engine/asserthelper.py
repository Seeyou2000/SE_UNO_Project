from engine.events.emitter import EventEmitter
from engine.events.event import Event


def assert_event_occured(
    emitter: EventEmitter,
    event_name: str,
    message: str,
    capturing: bool = True,
    bubbling: bool = False,
) -> None:
    flag = False

    def handler(_: Event) -> None:
        nonlocal flag
        flag = True

    emitter.on(event_name, handler, capturing, bubbling)

    assert flag, message


def assert_not_event_occured(
    emitter: EventEmitter,
    event_name: str,
    message: str,
    capturing: bool = True,
    bubbling: bool = False,
) -> None:
    flag = False

    def handler(_: Event) -> None:
        nonlocal flag
        flag = True

    emitter.on(event_name, handler, capturing, bubbling)

    assert not flag, message
