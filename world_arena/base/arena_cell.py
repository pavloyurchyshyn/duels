from settings.arena_settings import ELEMENT_SIZE
from settings.colors import GREY_DARK
from settings.window_settings import MAIN_SCREEN
from common_things.camera import GLOBAL_CAMERA
from pygame import Surface, SRCALPHA

from world_arena.base.arena_cell_obj import ArenaCellObject


class ArenaCell(ArenaCellObject):
    def __init__(self, data: dict = {}, draw_grid=False, server_instance=False):
        super().__init__(data=data, server_instance=server_instance)
        self._ARENA_SURFACE = self.get_surface(self.size_x, self.size_y)  # MAIN SURFACE OF CELL
        self._ARENA_SURFACE.fill(GREY_DARK)

        if draw_grid:
            self.draw_grid()

        self.draw_markup()

    def update(self):
        self._update()

    def draw(self):
        MAIN_SCREEN.blit(self._ARENA_SURFACE, GLOBAL_CAMERA.camera)

    def build_cell(self):
        pass

    @staticmethod
    def get_surface(size_x, size_y, transparent=0):
        flags = 0
        if transparent:
            flags = SRCALPHA
        surface = Surface((size_x, size_y), flags, 32)
        surface.convert_alpha()
        return surface

    def draw_markup(self):
        from pygame import draw

        arena_center = self.ARENA_SIZE[0]//2, self.ARENA_SIZE[1]//2
        center_circle_r = self.ARENA_SIZE[1] // 6

        draw.line(self._ARENA_SURFACE, (100, 100, 100), (arena_center[0], 0), (arena_center[0], self.ARENA_SIZE[1]), 6)
        draw.line(self._ARENA_SURFACE, (200, 200, 200), (arena_center[0], 0), (arena_center[0], self.ARENA_SIZE[1]), 2)

        draw.circle(self._ARENA_SURFACE, (100, 100, 100), arena_center, center_circle_r, 3)
        draw.circle(self._ARENA_SURFACE, (200, 200, 200), arena_center, center_circle_r, 1)

        # draw.circle(self._ARENA_SURFACE, (100, 100, 100), arena_center, center_circle_r//12+2)
        draw.circle(self._ARENA_SURFACE, (200, 200, 200), arena_center, center_circle_r//12)

    def draw_grid(self):
        from pygame import draw
        x_size, y_size = self._ARENA_SURFACE.get_size()

        for x in range(0, x_size, ELEMENT_SIZE):
            draw.line(self._ARENA_SURFACE, (115, 115, 115), (x, 0), (x, y_size))
        for y in range(0, y_size, ELEMENT_SIZE):
            draw.line(self._ARENA_SURFACE, (115, 115, 115), (0, y), (x_size, y))

        for border in self._exit_borders.values():
            draw.lines(self._ARENA_SURFACE, (255, 50, 50), True, border._dots[1:], 2)

    @property
    def surface(self):
        return self._ARENA_SURFACE
