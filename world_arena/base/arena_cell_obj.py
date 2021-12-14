from obj_properties.rect_form import Rectangle
from settings.arena_settings import STANDARD_ARENA_SIZE, STANDARD_ARENA_BORDER_SIZE, ELEMENT_SIZE, STANDARD_ARENA_Y_SIZE
from common_things.common_objects_lists_dicts import BULLETS_LIST, ITEMS_LIST, PARTICLE_LIST_L1,\
    ALL_OBJECT_DICT, NEW_OBJECTS, DEAD_OBJECTS
from settings.weapon_settings.types_and_names import BULLETS_TYPE
from common_things.object_creator import add_object


class ArenaCellObject(Rectangle):
    """

    REAL ARENA

    ARENA, BULLETS, UNITS and ITEMS CONTROLLER

    """
    ARENA_SIZE = STANDARD_ARENA_SIZE  # world cell_size
    BORDER_SIZE = STANDARD_ARENA_BORDER_SIZE  # borders of cell
    ELEMENT_SIZE = ELEMENT_SIZE

    def __init__(self, data: dict = {}, server_instance=False):
        self.server_instance = server_instance
        self._size = ArenaCellObject.ARENA_SIZE
        self._border_size = ArenaCellObject.ARENA_SIZE * ArenaCellObject.BORDER_SIZE

        super().__init__(x=0, y=0, size_x=self._size, size_y=STANDARD_ARENA_Y_SIZE)

        self._data = data

        self._sub_cells = {}

        self._exit_borders = {}
        self.__create_borders()

        # -------- LISTS --------
        self._items = ITEMS_LIST
        self._bullets = BULLETS_LIST
        self._particles = PARTICLE_LIST_L1

        self.all_objects_dict = ALL_OBJECT_DICT
        self.all_objects_counter = 1
        self.dead_objects_keys = set()

        self._dead_objects = DEAD_OBJECTS
        self._new_objects = NEW_OBJECTS

    def update(self):
        self._update()

    def _update(self):
        for bullet in self._bullets.copy():
            bullet.update()
            if bullet.dead:
                self.dead_objects_keys.add(bullet.KEY)

            elif not self.server_instance:
                bullet.draw()

        if self.server_instance and self.dead_objects_keys:
            self._dead_objects.extend(self.dead_objects_keys)

        while self.dead_objects_keys:
            self.delete_object_by_key(obj_key=self.dead_objects_keys.pop())

    def delete_object_by_key(self, obj_key):
        if obj_key in self.all_objects_dict:
            obj = self.all_objects_dict.pop(obj_key)
            if obj.TYPE == BULLETS_TYPE:
                self._bullets.remove(obj)

    def add_object(self, obj_data):
        add_object(self, obj_data)

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

    @staticmethod
    def normalize_xy_for_element(x, y):
        return (x // ArenaCellObject.ELEMENT_SIZE) * ArenaCellObject.ELEMENT_SIZE, \
               (y // ArenaCellObject.ELEMENT_SIZE) * ArenaCellObject.ELEMENT_SIZE

    @property
    def dead_objects(self):
        dead_obj = self._dead_objects.copy()
        self._dead_objects.clear()
        return dead_obj

    @property
    def new_objects(self):
        new_obj = self._new_objects.copy()
        self._new_objects.clear()
        return new_obj

    def __del__(self):
        for objects_pull in (self._bullets, self._items,
                             self._particles, self.all_objects_dict,
                             self._dead_objects, self._new_objects
                             ):
            objects_pull.clear()
