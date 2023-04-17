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

    def get_time(self) -> float:  # 화면에 남은 시간 오브젝트 띄울때 사용될 남은시간, 총 시간 리턴하는 함수입니다.
        return self._time, self._duration

    def set_duration(self, duration: float) -> None:
        self._duration = duration

    def reset(self) -> None:
        self._time = 0
