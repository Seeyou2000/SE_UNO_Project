import pygame

# https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame
_circle_cache = {}


def _circlepoints(r: float) -> list[tuple[float, float]]:
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(
    text: str,
    font: pygame.font.Font,
    text_color: pygame.Color,
    outline_color: pygame.Color = pygame.Color(255, 255, 255),
    outline_px: int = 2,
) -> pygame.Surface:
    text_surface = font.render(text, True, text_color).convert_alpha()

    w = text_surface.get_width() + 2 * outline_px
    h = font.get_linesize() + 4 * outline_px
    outline_surface = pygame.Surface((w, h)).convert_alpha()
    outline_surface.fill((0, 0, 0, 0))

    final_surface = outline_surface.copy()

    outline_surface.blit(font.render(text, True, outline_color).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(outline_px):
        final_surface.blit(outline_surface, (dx + outline_px, dy + outline_px))

    final_surface.blit(text_surface, (outline_px, outline_px))
    return final_surface
