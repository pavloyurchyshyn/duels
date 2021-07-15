from obj_properties.rect_form import Rectangle
from settings.arena_settings import STANDARD_ARENA_CELL_SIZE, STANDARD_ARENA_BORDER_SIZE, \
    ELEMENT_SIZE, SUB_CELL_SIZE
from common_things.common_lists import BULLETS_LIST, WALLS_SET, \
    ITEMS_LIST, PLAYERS_LIST, UNITS_LIST, PARTICLE_LIST, DOORS_LIST, BREAKABLE_WALLS


class ArenaCell:
    """

    REAL ARENA

    ARENA, BULLETS, UNITS and ITEMS CONTROLLER

    """
    CELL_SIZE = STANDARD_ARENA_CELL_SIZE  # world cell_size
    BORDER_SIZE = STANDARD_ARENA_BORDER_SIZE  # borders of cell
    ELEMENT_SIZE = ELEMENT_SIZE

    SUB_CELL_SIZE = SUB_CELL_SIZE

    BORDER_POSITIONS = {
        # top border
        'top': {'x': 0, 'y': 0, 'size_x': CELL_SIZE, 'size_y': BORDER_SIZE},
        # right border
        'right': {'x': CELL_SIZE - BORDER_SIZE, 'y': 0, 'size_x': BORDER_SIZE, 'size_y': CELL_SIZE},
        # bot border
        'bot': {'x': 0, 'y': CELL_SIZE - BORDER_SIZE, 'size_x': CELL_SIZE, 'size_y': BORDER_SIZE},
        # left border
        'left': {'x': 0, 'y': 0, 'size_x': BORDER_SIZE, 'size_y': CELL_SIZE},
    }

    def __init__(self, data: dict = {}):
        self._size = ArenaCell.CELL_SIZE

        self._data = data

        self._sub_cells = {}
        self._build_sub_cells()

        self._exit_borders = {}
        self.__create_borders()

        # -------- LISTS --------
        self._breakable_walls = BREAKABLE_WALLS
        self._walls = WALLS_SET

        self._doors = DOORS_LIST
        self._items = ITEMS_LIST
        self._bullets = BULLETS_LIST
        self._units = UNITS_LIST
        self._particles = PARTICLE_LIST

    def update(self):
        pass

    def can_go(self):
        # TODO
        pass

    def get_position_dict(self) -> dict:
        # TODO: make logic
        return {}

    def build_cell(self):
        pass

    def __create_borders(self):
        """
        Border for exit from Arena Cell
        :return:
        """
        for key in ArenaCell.BORDER_POSITIONS:
            data = ArenaCell.BORDER_POSITIONS[key]
            self._exit_borders[key] = Rectangle(**data)

    def _build_sub_cells(self):
        """
        Subcells for improve collide
        :return:
        """
        sub_cells = {}
        for x in range(0, self._size, ArenaCell.SUB_CELL_SIZE):
            for y in range(0, self._size, ArenaCell.SUB_CELL_SIZE):
                # x0, y0
                #   +-------------------+
                #   |                   |
                #   |                   |
                #   |               <---+--0
                #   |                   |
                #   |                   |
                #   +-------------------+
                sub_cells[self.normalize_xy_for_subcell(x, y)] = list()

        self._sub_cells = sub_cells

    def add_element(self, x, y, element):
        self._sub_cells[self.normalize_xy_for_subcell(x, y)].append(element)

    def check_for_exit(self, xy) -> str or 0:
        for way, border in self._exit_borders.items():
            if border.collide_point(xy):
                return way  # returns direction

        return 0

    def normalize_xy_for_subcell(self, x, y):
        return (x // ArenaCell.SUB_CELL_SIZE) * ArenaCell.SUB_CELL_SIZE, \
               (y // ArenaCell.SUB_CELL_SIZE) * ArenaCell.SUB_CELL_SIZE

    def normalize_xy_for_element(self, x, y):
        return (x // ArenaCell.ELEMENT_SIZE) * ArenaCell.ELEMENT_SIZE, \
               (y // ArenaCell.ELEMENT_SIZE) * ArenaCell.ELEMENT_SIZE
