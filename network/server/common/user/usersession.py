from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserSession:
    """
    접속한 실제 플레이어와 관련된 정보를 담는 클래스
    """

    id: str
    name: str
    sid: str

    def __hash__(self) -> int:
        return hash(self.sid)

    def __str__(self) -> str:
        return self.sid
