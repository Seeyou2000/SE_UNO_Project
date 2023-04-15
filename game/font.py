from enum import Enum

import pygame

_font_cache = {}


class FontType(Enum):
    UI_BOLD = "resources/fonts/GmarketSansTTFBold.ttf"
    UI_NORMAL = "resources/fonts/GmarketSansTTFMedium.ttf"
    YANGJIN = "resources/fonts/Yangjin.ttf"


def get_font(type: FontType, size: int) -> pygame.font.Font:
    path = type.value
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.Font(path, size)
    return _font_cache[key]
