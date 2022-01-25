from common_things.loggers import LOGGER

# dict which contains object_name: obj_class
ALL_NAMES_OBJECTS_DICT = {}

ALL_OBJ_TYPES: set = set()
ALL_OBJ_NAMES: set = set()


def all_names_objects_dict_wrapper(cls):
    """
    :param cls: any object which will be created in game
    :return:
    """
    if cls.OBJ_NAME in ALL_NAMES_OBJECTS_DICT:
        raise Exception(f'Object {cls.OBJ_NAME} already exists in dict')

    ALL_OBJ_TYPES.add(cls.OBJ_TYPE)
    ALL_OBJ_NAMES.add(cls.OBJ_NAME)

    ALL_NAMES_OBJECTS_DICT[cls.OBJ_NAME] = cls
    LOGGER.info(f'Defined {cls.OBJ_NAME}')
    return cls
