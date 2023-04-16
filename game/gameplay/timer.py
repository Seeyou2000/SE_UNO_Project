from engine.event import Event, EventEmitter


class Timer(EventEmitter):
    _time: float
    _duration: float

    def __init__(self, duration: float) -> None:
        super().__init__()
        self._time = 0
        self._duration = duration

    def update(self, dt: float) -> None:
        self._time += dt

        if self._time >= self._duration:
            # self.reset()
            self.emit("tick", Event({}))

    def reset(self) -> None:
        self._time = 0
