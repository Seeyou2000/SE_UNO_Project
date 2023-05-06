import pygame

from engine.focus import Focusable
from engine.gameobjectcontainer import GameObjectContainer
from engine.sprite import Sprite
from game import text_outline
from game.constant import AbilityType
from game.font import FontType, get_font
from game.gameplay.card import Card

CARD_SIZE_UNIT = 32
CARD_BACK_SIZE_UNIT = CARD_SIZE_UNIT * 0.7

CARD_WIDTH_MULTIPLIER = 3.2
CARD_HEIGHT_MULTIPLIER = 4.5

CARD_BORDER_RADIUS = 8

COLORS = {
    "black": pygame.Color("black"),
    "red": pygame.Color("#FF443F"),
    "yellow": pygame.Color("#FECB3A"),
    "green": pygame.Color("#1CBE02"),
    "blue": pygame.Color("#419AFF"),
}

COLORBLIND_COLORS = {
    "black": pygame.Color("black"),
    "red": pygame.Color("#D41159"),
    "yellow": pygame.Color("#FEFE62"),
    "green": pygame.Color("#1AFF1A"),
    "blue": pygame.Color("#1A85FF"),
}


class CardEntity(GameObjectContainer, Focusable):
    WIDTH = CARD_SIZE_UNIT * CARD_WIDTH_MULTIPLIER
    HEIGHT = CARD_SIZE_UNIT * CARD_HEIGHT_MULTIPLIER

    is_outline_enabled: bool

    def __init__(self, card: Card) -> None:
        super().__init__()
        self.card = card
        self._is_colorblind = False
        self.rect = pygame.Rect(0, 0, CardEntity.WIDTH, CardEntity.HEIGHT)
        self.sprite = create_card_sprite(
            self.card.color,
            False,
            self._is_colorblind,
            self.card.number,
            self.card.ability,
        )
        self.add_child(self.sprite)

    def set_colorblind(self, is_colorblind: bool) -> None:
        if self._is_colorblind == is_colorblind:
            return
        self.remove_child(self.sprite)
        self.sprite = create_card_sprite(
            self.card.color, False, is_colorblind, self.card.number, self.card.ability
        )
        self.add_child(self.sprite)
        self._is_colorblind = is_colorblind

    def render(self, surface: pygame.Surface) -> None:
        super().render(surface)

        if self.has_focus:
            pygame.draw.rect(
                surface,
                pygame.Color("red"),
                self.absolute_rect,
                2,
                border_radius=CARD_BORDER_RADIUS,
            )


def create_card_sprite(
    color: str,
    is_back: bool,
    is_colorblind: bool,
    number: int | None = None,
    ability: AbilityType | None = AbilityType,
    is_small: bool = False,
) -> Sprite:
    width = (
        CARD_BACK_SIZE_UNIT if is_small else CARD_SIZE_UNIT
    ) * CARD_WIDTH_MULTIPLIER
    height = (
        CARD_BACK_SIZE_UNIT if is_small else CARD_SIZE_UNIT
    ) * CARD_HEIGHT_MULTIPLIER
    card_color = get_card_color(color, is_colorblind)
    card_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    card_rect = card_surface.get_rect()

    if is_back:
        # 두꺼운 테두리용
        pygame.draw.rect(
            card_surface,
            pygame.Color("#525252"),
            card_rect,
            border_radius=CARD_BORDER_RADIUS,
        )
        # 색 배경
        pygame.draw.rect(
            card_surface,
            pygame.Color("#262626"),
            card_rect.inflate(-12, -12),
            border_radius=CARD_BORDER_RADIUS - 4,
        )

        # 큰 느낌표
        text_surface = get_font(FontType.YANGJIN, 42).render(
            "!",
            True,
            pygame.Color("#525252"),
        )
        text_surface_rect = text_surface.get_rect(center=card_rect.center)
        card_surface.blit(text_surface, text_surface_rect)
    else:
        # 두꺼운 테두리용
        pygame.draw.rect(
            card_surface,
            pygame.Color("white"),
            card_rect,
            border_radius=CARD_BORDER_RADIUS,
        )
        # 색 배경
        pygame.draw.rect(
            card_surface,
            card_color,
            card_rect.inflate(-12, -12),
            border_radius=CARD_BORDER_RADIUS - 3,
        )
        if is_colorblind is True:
            draw_color_shape(card_surface, color)

        if number is not None:
            draw_number(card_surface, number)
        if ability is not None:
            draw_ability(card_surface, ability)

    # 테두리
    pygame.draw.rect(
        card_surface,
        pygame.Color("#E3E3E3"),
        card_surface.get_rect(),
        border_radius=CARD_BORDER_RADIUS,
        width=1,
    )

    return Sprite(card_surface)


def draw_number(surface: pygame.Surface, number: int) -> None:
    container_rect = surface.get_rect()

    # 큰 텍스트
    text_surface = text_outline.render(
        str(number),
        get_font(FontType.YANGJIN, 42),
        pygame.Color("black"),
        outline_px=4,
    )
    text_surface_rect = text_surface.get_rect(center=container_rect.center)
    surface.blit(text_surface, text_surface_rect)

    # 작은 텍스트
    small_text_margin = 14
    small_text_surface = text_outline.render(
        str(number), get_font(FontType.YANGJIN, 12), pygame.Color("black")
    )
    small_text_rect = small_text_surface.get_rect()
    surface.blit(
        small_text_surface,
        small_text_rect.move(small_text_margin, small_text_margin),
    )

    # 작은 텍스트는 뒤집어서 한번 더 찍음
    bottomright_text_rect = small_text_rect.copy()
    bottomright_text_rect.bottom = container_rect.bottom - small_text_margin
    bottomright_text_rect.right = container_rect.right - small_text_margin
    surface.blit(
        pygame.transform.rotate(small_text_surface, 180), bottomright_text_rect
    )


def draw_ability(surface: pygame.Surface, ability: AbilityType) -> None:
    # 임시로 텍스트로만 그림

    container_rect = surface.get_rect()

    ability_text = ""
    match ability:
        case AbilityType.CHANGE_CARD_COLOR:
            ability_text = "색"
        case AbilityType.ABSOULTE_ATTACK:
            ability_text = "+2"
        case AbilityType.ABSOULTE_PROTECT:
            ability_text = "☆"
        case AbilityType.GIVE_TWO_CARDS:
            ability_text = "+2"
        case AbilityType.GIVE_FOUR_CARDS:
            ability_text = "+4"
        case AbilityType.SKIP_ORDER:
            ability_text = "스킵"
        case AbilityType.REVERSE_ORDER:
            ability_text = "역"

    text_surface = text_outline.render(
        ability_text,
        get_font(FontType.YANGJIN, 40),
        pygame.Color("black"),
        outline_px=4,
    )
    text_surface_rect = text_surface.get_rect(center=surface.get_rect().center)
    surface.blit(text_surface, text_surface_rect)

    # 작은 텍스트
    small_text_margin = 14
    small_text_surface = text_outline.render(
        ability_text,
        get_font(FontType.YANGJIN, 12),
        pygame.Color("black"),
    )
    small_text_rect = small_text_surface.get_rect()
    surface.blit(
        small_text_surface,
        small_text_rect.move(small_text_margin, small_text_margin),
    )

    # 작은 텍스트는 뒤집어서 한번 더 찍음
    bottomright_text_rect = small_text_rect.copy()
    bottomright_text_rect.bottom = container_rect.bottom - small_text_margin
    bottomright_text_rect.right = container_rect.right - small_text_margin
    surface.blit(
        pygame.transform.rotate(small_text_surface, 180), bottomright_text_rect
    )


def draw_color_shape(surface: pygame.Surface, color: str) -> None:
    container_rect = surface.get_rect()

    if color == "red":
        pygame.draw.ellipse(
            surface,
            (255, 255, 255),
            [10, 10, container_rect.centerx * 2 - 20, container_rect.centery * 2 - 20],
        )
    elif color == "yellow":
        pygame.draw.polygon(
            surface,
            (255, 255, 255),
            [
                [5, container_rect.centery / 2],
                [container_rect.centerx, container_rect.centery * 2 - 5],
                [container_rect.centerx * 2 - 5, container_rect.centery / 2],
            ],
        )
    elif color == "green":
        pygame.draw.polygon(
            surface,
            (255, 255, 255),
            [
                [5, (container_rect.centery / 2) * 3],
                [container_rect.centerx, 5],
                [container_rect.centerx * 2 - 5, (container_rect.centery / 2) * 3],
            ],
        )
    elif color == "blue":
        pygame.draw.polygon(
            surface,
            (255, 255, 255),
            [
                [5, container_rect.centery],
                [container_rect.centerx, container_rect.centery * 2 - 5],
                [container_rect.centerx * 2 - 5, container_rect.centery],
                [container_rect.centerx, 5],
            ],
        )


def get_card_color(color: str, is_colorblind: bool) -> pygame.Color:
    return COLORBLIND_COLORS[color] if is_colorblind else COLORS[color]
