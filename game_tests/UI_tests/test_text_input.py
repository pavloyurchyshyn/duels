from game_tests.window_for_tests import *
from UI.UI_base.input_element_UI import InputElement

if __name__ == '__main__':
    TEST_ELEMENT_DRAW(
        InputElement(100, 100, 200, 50, default_text='test')
    )
