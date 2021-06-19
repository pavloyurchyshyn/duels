from game_tests.window_for_tests import *
from UI.UI_base.button_UI import Button
from UI.UI_base.transition_UI import TransitionUI

# import clipboard
# clipboard.copy("abc")


trans = TransitionUI(transparent=1)


def action():
    trans.move()


if __name__ == '__main__':
    TEST_ELEMENT_DRAW(
        trans,
        Button(x=100, y=200, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='Move',
               on_click_action=action,
               text_size=35,
               transparent=0, moveable=1,
               click_delay=0
               ),
        Button(x=100, y=300, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='Fast close',
               on_click_action=trans.fast_close,
               text_size=35,
               transparent=0, moveable=1,
               click_delay=0
               ),
        Button(x=100, y=400, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='fast open',
               on_click_action=trans.fast_open,
               text_size=35,
               transparent=0, moveable=1,
               click_delay=0
               ),

    )
