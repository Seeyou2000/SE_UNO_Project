import json

STORY_CLEAR_STATUS_FILE_PATH = "storyclearstatus.json"

DEFAULT_STORY_CLEAR_STATUS = {
    "1": False,
    "2": False,
    "3": False,
    "4": False,
}


class StoryClearStatus:
    def __init__(self) -> None:
        self.data = {}

    def save(self) -> None:
        with open(STORY_CLEAR_STATUS_FILE_PATH, "w") as f:
            json.dump(
                self.data,
                f,
            )

    def load(self) -> None:
        try:
            with open(STORY_CLEAR_STATUS_FILE_PATH) as f:
                self.load_dict(json.load(f))
        except FileNotFoundError:
            print("기존 스토리 클리어 파일을 찾지 못했습니다. 새 스토리 클리어 파일을 만듭니다.")
            self.reset()

    def load_dict(self, value: dict[str, bool]) -> None:
        self.data = value

    def update_status(self, key: int, value: bool) -> None:
        self.data[str(key)] = value
        self.save()

    def reset(self) -> None:
        self.load_dict(DEFAULT_STORY_CLEAR_STATUS)
        self.save()

    def is_playable_area(self, area: int) -> bool:
        return area < 2 or self.data[str(area - 1)]
