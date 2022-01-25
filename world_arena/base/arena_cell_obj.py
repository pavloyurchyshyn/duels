from obj_properties.rect_form import Rectangle
from settings.arena_settings import STANDARD_ARENA_X_SIZE, STANDARD_ARENA_BORDER_SIZE, ELEMENT_SIZE, \
    STANDARD_ARENA_Y_SIZE
from common_things.common_objects_lists_dicts import BULLETS_LIST, OBJECTS_LIST, PARTICLE_LIST_L1, \
    ALL_OBJECT_DICT, NEW_OBJECTS_KEYS, DEAD_OBJECTS_KEYS, MELEE_HITS_LIST
from settings.weapon_settings.types_and_names import BULLETS_TYPE
from object_controller import AllObjectsController
from settings.global_parameters import its_client_instance


class ArenaCellObject(Rectangle):
    """

    REAL ARENA

    ARENA, BULLETS, UNITS and ITEMS CONTROLLER

    """
    ARENA_SIZE = STANDARD_ARENA_X_SIZE, STANDARD_ARENA_Y_SIZE  # world cell_size
    BORDER_SIZE = STANDARD_ARENA_BORDER_SIZE  # borders of cell
    ELEMENT_SIZE = ELEMENT_SIZE

    def __init__(self, data: dict = {}, server_instance=not its_client_instance()):
        self.server_instance = server_instance
        self._size = ArenaCellObject.ARENA_SIZE
        self._border_size = STANDARD_ARENA_X_SIZE * ArenaCellObject.BORDER_SIZE

        super().__init__(x=0, y=0, size_x=STANDARD_ARENA_X_SIZE, size_y=STANDARD_ARENA_Y_SIZE)

        self._data = data

        self._sub_cells = {}

        self._exit_borders = {}
        self.__create_borders()

        self._object_controller = AllObjectsController(arena=self)

    def update(self):
        self._update()

    def _update(self):
        pass

    def __create_borders(self):
        """
        Border for exit from Arena Cell
        :return:
        """
        BORDER_POSITIONS = {
            # top border
            'top': {'x': 0, 'y': 0, 'size_x': self.size_x, 'size_y': self._border_size},
            # right border
            'right': {'x': self.size_x - self._border_size, 'y': 0, 'size_x': self._border_size, 'size_y': self._size},
            # bot border
            'bot': {'x': 0, 'y': self.size_y - self._border_size, 'size_x': self.size_x, 'size_y': self._border_size},
            # left border
            'left': {'x': 0, 'y': 0, 'size_x': self._border_size, 'size_y': self.size_y},
        }

        for key in BORDER_POSITIONS:
            data = BORDER_POSITIONS[key]
            self._exit_borders[key] = Rectangle(**data)

    def check_for_exit(self, xy) -> str or 0:
        for way, border in self._exit_borders.items():
            if border.collide_point(xy):
                return 1

        return 0

