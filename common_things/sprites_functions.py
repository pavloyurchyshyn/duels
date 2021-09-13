from pygame import Surface, SRCALPHA


def get_surface(size_x, size_y=None, transparent: bool = 0, flags=SRCALPHA, color=None):
    size_y = size_y if size_y else size_x

    if not transparent:
        flags = 0

    surface = Surface((size_x, size_y), flags, 32)

    if color:
        surface.fill(color)

    surface.convert_alpha()
    return surface
