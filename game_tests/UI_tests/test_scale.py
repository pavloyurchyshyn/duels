from game_tests.window_for_tests import *
from UI.UI_base.button_UI import Button


# import clipboard
# clipboard.copy("abc")

def test_message(*args):
    args = ' '.join(list(filter(bool, args)))
    fps_text = DEFAULT_FONT.render(f'TEST{args}', 1, WHITE, (20, 20, 20))

    MAIN_SCREEN.blit(fps_text, (310, 310))


con_b = Button(x=1200, y=200, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='TEST', on_click_action=test_message,
               text_size=35,
               transparent=0, click_delay=0, moveable=1)

if __name__ == '__main__':
    TEST_ELEMENT_DRAW(

        Button(x=100, y=200, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='Up',
               on_click_action=con_b.scale,
               on_click_action_args=(1.2, ),
               text_size=35,
               transparent=0, moveable=1,
               click_delay=0
               ),

        Button(x=100, y=300, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='Down',
               on_click_action=con_b.scale,
               on_click_action_args=(0.9, ),
               text_size=35,
               transparent=0, click_delay=0, moveable=1,
               ),

        Button(x=100, y=400, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='Original Size', text_size=25,
               on_click_action=con_b.make_original_size,
               transparent=0, click_delay=0, moveable=1,
               ),

        con_b,
    )
