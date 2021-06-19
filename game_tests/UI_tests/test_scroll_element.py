from game_tests.window_for_tests import *
from UI.UI_base.button_UI import Button
from UI.UI_base.scroll_UI import Scroll

# import clipboard
# clipboard.copy("abc")

def test_message(*args):
    args = ' '.join(list(filter(bool, args)))
    fps_text = DEFAULT_FONT.render(f'TEST{args}', 1, WHITE, (20, 20, 20))

    MAIN_SCREEN.blit(fps_text, (310, 310))


if __name__ == '__main__':
    TEST_ELEMENT_DRAW(
        Scroll(x=300, y=100, screen=MAIN_SCREEN,
               columns=3, rows=3),


        Button(x=100, y=600, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='moveable', on_click_action=test_message,
               text_size=35,
               transparent=0, click_delay=0, moveable=1),
    )
