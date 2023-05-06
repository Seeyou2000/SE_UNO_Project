import pygame


def lighten_ip(surface: pygame.Surface, amount: float) -> None:
    surface.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_ADD)


def lighten(surface: pygame.Surface, amount: float) -> pygame.Surface:
    new_surface = surface.copy()
    lighten_ip(new_surface, amount)
    return new_surface


def darken_ip(surface: pygame.Surface, amount: float) -> None:
    surface.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_SUB)


def darken(surface: pygame.Surface, amount: float) -> pygame.Surface:
    new_surface = surface.copy()
    darken_ip(new_surface, amount)
    return new_surface
