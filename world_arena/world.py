from pygame import Surface
from pygame.transform import scale

from obj_properties.rect_form import Rectangle

from settings.window_settings import MAIN_SCREEN, SCREEN_W, SCREEN_H

from settings.world_settings import CELL_PICTURE_SIZE, WORLD_ARENA_PICTURE_SIZE, \
    WORLD_COLUMNS, WORLD_LINES

from common_things.exceptions.world_arena_exceptions import ClosedCellError, DeadCellError, CellOutOfWorld
from common_things.global_mouse import GLOBAL_MOUSE
from world_arena.base.arena_cell import ArenaCell


class World(Rectangle):
    WA_PICTURE_SIZE = WORLD_ARENA_PICTURE_SIZE
    C_PICTURE_SIZE = CELL_PICTURE_SIZE
    DIRECTIONS = {
        'left_top': (-1, -1), 'top': (0, 1), 'right_top': (1, -1),
        'left': (-1, 0), 'right': (1, 0),
        'left_bot': (-1, 1), 'bot': (0, -1), 'right_bot': (1, 1),
    }

    def __init__(self, cells: dict = [{}, ],
                 x: int = 0, y: int = 0,
                 size_x: int = WA_PICTURE_SIZE[0],
                 size_y: int = WA_PICTURE_SIZE[1],
                 screen=MAIN_SCREEN,
                 ):
        """
        :param x: position of World window
        :type x: int
        :param y: position of World window
        :type y: int

        :param size_x: size of World window
        :type size_x: int
        :param size_y: size of World window
        :type size_y: int

        :param cells: data of all cells
        """

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.__mouse = GLOBAL_MOUSE

        self._SCREEN = screen

        self._cells_data = cells
        self._cells_dict: dict = {}
        self.build_cells_dict()

        self._MAIN_surface = self.get_surface(self.size_x, self.size_y)

        self._map_pic_pos = [x, y]

        self._scale_k = 1

        self._current_arena_cell_coordinates = (0, 0)

        self._CURRENT_CELL = None

    def build_cell(self, cell_coordinates=None, draw_grid=True):
        if cell_coordinates:
            self._current_arena_cell_coordinates = cell_coordinates

        self._CURRENT_CELL = ArenaCell(**self._cells_dict[self._current_arena_cell_coordinates], draw_grid=True)

    def build_cells_dict(self):
        y = 0
        x = 0
        for cell in self._cells_data:
            self._cells_dict[x, y] = cell
            x += 1
            if x >= WORLD_COLUMNS:
                x = 0
                y += 1

    def move(self, direction: str):
        """
        Make step

        :param direction: 'top' or 'bot' or 'left' or 'right'
        :type direction: str
        :return:
        """

        direction = World.DIRECTIONS[direction]

        new_x, new_y = self._current_arena_cell_coordinates[0] + direction[0],\
                       self._current_arena_cell_coordinates[1] + direction[1]

        # change direction if new position is on the map/ inside the map
        if (new_x, new_y) not in self._cells_dict:
            raise CellOutOfWorld(new_x, new_y)

        cell = self._cells_dict[(new_x, new_y)]

        if not cell.get('open',True):
            raise ClosedCellError(new_x, new_y)

        elif cell.dead:
            raise DeadCellError(new_x, new_y)

        # change position if all ok
        else:
            self._current_arena_cell_coordinates = [new_x, new_y]

    def update(self):
        # TODO: do
        pass

    def get_surface(self, size_x, size_y):
        surface = Surface((size_x, size_y), 0, 32)

        surface.convert_alpha()

        return surface

    def draw(self, dx=0, dy=0):
        m_surface = self._MAIN_surface.copy()
        # m_surface.blit(
        #     scale(self._Map_Picture, (World.WA_PICTURE_SIZE * self._scale_k, World.WA_PICTURE_SIZE * self._scale_k)),
        #     self._map_pic_pos)

    def GET_CURRENT_CELL(self):
        return self._CURRENT_CELL

    @property
    def current_cell_coord(self):
        return self._current_arena_cell_coordinates


GLOBAL_WORLD = World()
