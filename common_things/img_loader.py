from pygame import image, error, transform, Color
from common_things.loggers import LOGGER
from sys import exit
import os

from common_things.wrappers import time_control_wrapper

try:
    # maybe another pictures will load
    ERROR_PICTURE = image.load('sprites/error.png').convert_alpha()
    ERROR_PICTURE = transform.rotate(ERROR_PICTURE, 90).convert_alpha()
except:
    ERROR_PICTURE = None
    LOGGER.warning(f'Failed to load error img {"sprites/error.png"}')


def loaded_images_wrapper(func):
    loaded_ = {}

    def wrapper(path, size, *args, **kwargs):
        if (path, size) not in loaded_:
            LOGGER.info(f'Loading {path} {size}')
            loaded_[(path, size)] = func(path, size, *args, **kwargs)

        return loaded_[(path, size)]

    return wrapper


@loaded_images_wrapper
def load_image(path: str, size: (int, int) = None, angle=90, smooth_scale=True):
    try:
        angle = angle if angle else 90
        if not path.startswith('sprites'):
            path = os.path.join('sprites', path)

        pic = image.load(path).convert_alpha()

        if size:
            size = (int(size[0]), int(size[1]))
            if smooth_scale:
                pic = transform.smoothscale(pic, size).convert_alpha()
            else:
                pic = transform.scale(pic, size).convert_alpha()

        pic = transform.rotate(pic, angle).convert_alpha()
        LOGGER.info(f'Loaded {path} {pic.get_size()}')
        return pic
    except (error, FileNotFoundError) as e:
        LOGGER.error(f'Failed to load {path}: {e}')

        return transform.smoothscale(ERROR_PICTURE, size).convert_alpha()
        # exit()


@time_control_wrapper
def load_animation(pic_list, timings_list, size: (int, int) = None, anim_dict=None, angle=90) -> dict:
    anim_dict = anim_dict if type(anim_dict) is dict else {}

    for i, path in enumerate(pic_list):
        anim_dict[i] = {'frame': load_image(path, size, angle=angle),
                        'cd': timings_list[i]}
    LOGGER.info(f'Animation loaded {pic_list}')
    return anim_dict


def _normalize_color(color) -> int:
    if color > 255:
        return 255
    elif color < 0:
        return 0
    else:
        return int(color)


def normalize_color(color) -> tuple:
    return tuple(map(_normalize_color, color))


@time_control_wrapper
def recolor_picture(picture, color):
    w, h = picture.get_size()
    t = Color((0, 0, 0, 0))

    new_c = Color(normalize_color(color))

    for x in range(w):
        for y in range(h):
            c_at = picture.get_at((x, y))
            # print(c_at[:2])
            if c_at[0] >= 10 and c_at[1] >= 10 and c_at[2] >= 10:
                pass
            elif c_at[3] > 250:
                picture.set_at((x, y), new_c)
            else:
                picture.set_at((x, y), t)

    return picture
