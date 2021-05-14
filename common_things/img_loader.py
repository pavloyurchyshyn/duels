from pygame import image, error, transform
from sys import exit

ERROR_PICTURE = image.load('sprites/error.png').convert_alpha()
ERROR_PICTURE = transform.rotate(ERROR_PICTURE, 90).convert_alpha()


def load_image(path, size: (int, int), a=90):
    try:
        pic = image.load(path).convert_alpha()
        pic = transform.smoothscale(pic, size).convert_alpha()
        pic = transform.rotate(pic, a).convert_alpha()
        return pic
    except (error, FileNotFoundError):
        print(f'No file {path}')
        return transform.smoothscale(ERROR_PICTURE, size).convert_alpha()
        #exit()

