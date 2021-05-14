from pygame import Surface
from pygame.transform import scale

from obj_properties.rect_form import Rectangle

from settings.window_settings import MAIN_SCREEN

from settings.world_settings import CELL_PICTURE_SIZE, WORLD_ARENA_PICTURE_SIZE, \
    WORLD_COLUMS, WORLD_LINES

from common_things.exceptions.world_arena_exceptions import ClosedCellError, DeadCellError, CellOutOfWorld
from common_things.global_mouse import GLOBAL_MOUSE


class World(Rectangle):
    WA_PICTURE_SIZE = WORLD_ARENA_PICTURE_SIZE
    C_PICTURE_SIZE = CELL_PICTURE_SIZE
    DIRECTIONS = {
        'left_top': (-1, -1), 'top': (0, 1), 'right_top': (1, -1),
        'left': (-1, 0), 'right': (1, 0),
        'left_bot': (-1, 1), 'bot': (0, -1), 'right_bot': (1, 1),
    }

    def __init__(self, cells: list = [],
                 x: int = 0, y: int = 0,
                 size_x: int = WA_PICTURE_SIZE,
                 size_y: int = WA_PICTURE_SIZE,
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

        :param cells: cells
        """

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self.__mouse = GLOBAL_MOUSE

        self._SCREEN = screen

        self._cells = cells
        self._cells_dict: dict = None
        self.__convert_cells()

        self._MAIN_surface = self.get_surface(self.size_x, self.size_y)

        self._Map_Picture = None
        self.build_Map_Picture()

        self._map_pic_pos = [0, 0]

        self._scale_k = 1

        self._current_arena_cell = [-1, -1]

    def move(self, direction: str):
        """
        Make step

        :param direction: 'top' or 'bot' or 'left' or 'right'
        :type direction: str
        :return:
        """

        direction = World.DIRECTIONS[direction]

        new_x, new_y = self._current_arena_cell[0] + direction[0], self._current_arena_cell[1] + direction[1]

        # change direction if new position is on the map/ inside the mapo
        if 0 <= new_x <= WORLD_COLUMS and 0 <= new_y <= WORLD_LINES:
            cell = self._cells_dict[(new_x, new_y)].open
            if not cell.open:
                raise ClosedCellError(new_x, new_y)

            elif cell.dead:
                raise DeadCellError(new_x, new_y)

            # change position if all ok
            else:
                self._current_arena_cell = [new_x, new_y]

        else:
            raise CellOutOfWorld(new_x, new_y)

    def update(self):
        # TODO: do
        pass

    def __convert_cells(self):
        converted_cells = {}
        i = 0
        for column in range(WORLD_COLUMS):
            for line in range(WORLD_LINES):
                converted_cells[line, column] = self._cells[i]
                i += 1

        self._cells_dict = converted_cells

    def build_Map_Picture(self):
        self._Map_Picture = self.get_surface(*World.WA_PICTURE_SIZE)

        for pos, cell in self._cells_dict.items():
            x, y = pos
            cell_pic = scale(cell.picture.copy(), (World.C_PICTURE_SIZE, World.C_PICTURE_SIZE))
            self._Map_Picture.blit(cell_pic, (x * World.C_PICTURE_SIZE, y * World.C_PICTURE_SIZE))

    def get_surface(self, size_x, size_y):
        surface = Surface((size_x, size_y), 0, 32)

        surface.convert_alpha()

        return surface

    def draw(self, dx=0, dy=0):
        m_surface = self._MAIN_surface.copy()
        m_surface.blit(
            scale(self._Map_Picture, (World.WA_PICTURE_SIZE * self._scale_k, World.WA_PICTURE_SIZE * self._scale_k)),
            self._map_pic_pos)
        # self._SCREEN.blit()

    def set_current_position(self, xy: tuple):
        self._current_arena_cell = xy

    @property
    def current_cell(self):
        return self._cells_dict[self._current_arena_cell]


GLOBAL_WORLD = World()
