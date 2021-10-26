from obj_properties.rect_form import Rectangle
from settings.arena_settings import STANDARD_ARENA_SIZE, STANDARD_ARENA_BORDER_SIZE, ELEMENT_SIZE
from common_things.common_objects_lists_dicts import BULLETS_LIST, WALLS_SET, \
    ITEMS_LIST, PLAYERS_LIST, UNITS_LIST, PARTICLE_LIST, DOORS_LIST, BREAKABLE_WALLS, ALL_OBJECT_DICT
# from settings.screen_size import GAME_SCALE
from settings.weapon_settings.types_and_names import BULLETS_TYPE
from settings.all_objects_names_classes_dict import ALL_NAMES_OBJECTS_DICT


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
        self._size = ArenaCellObject.ARENA_SIZE  # if server_instance else int(ArenaCellObject.ARENA_SIZE * GAME_SCALE)
        self._border_size = ArenaCellObject.BORDER_SIZE  # if server_instance else int(ArenaCellObject.BORDER_SIZE * GAME_SCALE)

        super().__init__(x=0, y=0, size_x=self._size)

        self._data = data

        self._sub_cells = {}

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

        self.all_objects_dict = ALL_OBJECT_DICT
        self.all_objects_counter = 1
        self.dead_objects_keys = set()

        self._dead_objects = []
        self._new_objects = []
        # if not self.server_instance:
        #     from settings.screen_size import X_SCALE, Y_SCALE
        #     self._x_scale = X_SCALE
        #     self._y_scale = Y_SCALE

    def update(self):
        self._update()

    def _update(self):
        for door in self._doors.copy():
            door.update()
            if not self.server_instance:
                door.draw()

        for bullet in self._bullets.copy():
            bullet.update()
            if bullet.dead:
                self.dead_objects_keys.add(bullet.KEY)

            elif not self.server_instance:
                bullet.draw()

        if self.server_instance and self.dead_objects_keys:
            self._dead_objects.extend(self.dead_objects_keys)

        while self.dead_objects_keys:
            key = self.dead_objects_keys.pop()
            self.delete_object_by_key(obj_key=key)

    def delete_object_by_key(self, obj_key):
        if obj_key in self.all_objects_dict:
            obj = self.all_objects_dict.pop(obj_key)
            if obj.TYPE == BULLETS_TYPE:
                self._bullets.remove(obj)

    def add_object(self, obj_data, from_server=False):
        obj_global_key = obj_data.get('key')
        if not obj_global_key:
            obj_global_key = self.all_objects_counter
            self.all_objects_counter += 1

        if from_server:
            obj_data['data']['x'] = obj_data['data']['x']  # * self._x_scale
            obj_data['data']['y'] = obj_data['data']['y']  # * self._y_scale

        obj = ALL_NAMES_OBJECTS_DICT.get(obj_data['name'])(**obj_data['data'], arena=self)
        obj.KEY = obj_global_key

        if obj.TYPE == BULLETS_TYPE:
            self._bullets.append(obj)

        self.all_objects_dict[obj_global_key] = obj

        obj_data['key'] = obj_global_key

        if self.server_instance:
            self._new_objects.append(obj_data)

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
            'top': {'x': 0, 'y': 0, 'size_x': self._size, 'size_y': self._border_size},
            # right border
            'right': {'x': self._size - self._border_size, 'y': 0, 'size_x': self._border_size, 'size_y': self._size},
            # bot border
            'bot': {'x': 0, 'y': self._size - self._border_size, 'size_x': self._size, 'size_y': self._border_size},
            # left border
            'left': {'x': 0, 'y': 0, 'size_x': self._border_size, 'size_y': self._size},
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
        for objects_pull in (self._bullets, self._doors, self._breakable_walls,
                             self._walls, self._items, self._units,
                             self._particles, self.all_objects_dict):
            objects_pull.clear()
