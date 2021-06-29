from pygame import image, error, transform, Color
from sys import exit

try:
    # maybe another pictures will load
    ERROR_PICTURE = image.load('sprites/error.png').convert_alpha()
    ERROR_PICTURE = transform.rotate(ERROR_PICTURE, 90).convert_alpha()
except:
    pass
    ERROR_PICTURE = None


def load_image(path, size: (int, int) = None, a=90, redraw_color=None):
    try:
        pic = image.load(path).convert_alpha()

        if redraw_color:
            pic = recolor_picture(pic, redraw_color)

        if size:
            pic = transform.smoothscale(pic, size).convert_alpha()

        pic = transform.rotate(pic, a).convert_alpha()
        return pic
    except (error, FileNotFoundError):
        print(f'No file {path}')
        return transform.smoothscale(ERROR_PICTURE, size).convert_alpha()
        # exit()


def load_animation(pic_list, timings_list, size=None, anim_dict=None, redraw_color=None) -> dict:
    anim_dict = anim_dict if type(anim_dict) is dict else {}

    for i, path in enumerate(pic_list):
        anim_dict[i] = {'frame': load_image(path, size, redraw_color=redraw_color),
                        'cd': timings_list[i]}

    return anim_dict


def recolor_picture(picture, color):
    w, h = picture.get_size()
    t = Color((0, 0, 0, 0))
    new_c = Color(color)

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
