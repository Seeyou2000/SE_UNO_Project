from engine.events.emitter import EventEmitter
from engine.events.event import Event


class Timer(EventEmitter):
    _time: float
    _duration: float
    _initial_count: int
    _count: int
    _enabled: bool

    def __init__(self, duration: float, count: int = 1) -> None:
        super().__init__()
        self._time = 0
        self._duration = duration
        self._enabled = True
        self._initial_count = count
        self._count = count

    def update(self, dt: float) -> None:
        if not self._enabled:
            return
        self._time += dt
        if self._time >= self._duration:
            self.emit("tick", Event({}, self))

            # 음수면 무한히 돌기
            if self._count < 0:
                return
            self._count -= 1
            if self._count == 0:
                self.pause()

    def get_time(self) -> float:  # 화면에 남은 시간 오브젝트 띄울때 사용될 남은시간, 총 시간 리턴하는 함수입니다.
        return self._time, self._duration

    def set_duration(self, duration: float) -> None:
        self._duration = duration

    def reset(self, off: bool = False) -> None:
        self._time = 0
        self._count = self._initial_count
        if off:
            self.pause()
        else:
            self.start()

    @property
    def enabled(self) -> bool:
        return self._enabled

    def pause(self) -> None:
        self._enabled = False

    def start(self) -> None:
        self._enabled = True
