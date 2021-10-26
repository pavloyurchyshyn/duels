from math import atan2


def get_angle_between_dots(dot_pos_1, dot_pos_2):
    x1, y1 = dot_pos_1
    x2, y2 = dot_pos_2

    d_x = 0.00001 if x1 - x2 == 0 else x1 - x2
    d_y = 0.00001 if y1 - y2 == 0 else y1 - y2

    return atan2(d_y, d_x)
