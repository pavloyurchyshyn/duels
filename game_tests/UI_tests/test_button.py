from game_tests.window_for_tests import *
from UI.UI_base.button_UI import Button


# import clipboard
# clipboard.copy("abc")

def test_message(*args):
    args = ' '.join(list(filter(bool, args)))
    fps_text = DEFAULT_FONT.render(f'TEST{args}', 1, WHITE, (20, 20, 20))

    MAIN_SCREEN.blit(fps_text, (310, 310))


def make_active():
    n_a_after_click.active = 1


n_a_after_click = Button(x=100, y=200, screen=MAIN_SCREEN,
                         text='test2 \n\t- non active after click', on_click_action=test_message,
                         on_click_action_args=' 2', text_size=12,
                         border_non_active_color=(0, 0, 0),
                         transparent=1, non_active_after_click=1)
if __name__ == '__main__':
    TEST_ELEMENT_DRAW(

        Button(x=100, y=100, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='test1', on_click_action=test_message,
               transparent=1),

        Button(x=300, y=200, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='make active', on_click_action=make_active,
               transparent=1),

        n_a_after_click,

        Button(x=100, y=300, screen=MAIN_SCREEN,
               text='test3 \n\t- non active after click\n\t- non visible after click',
               text_size=10,  # text_x=10, text_y=-10,
               on_click_action=test_message, transparent=1, non_active_after_click=1,
               on_click_action_args=' 3',
               non_visible_after_click=1),

        Button(x=100, y=400, screen=MAIN_SCREEN, non_visible_after_click=1,
               text='test1', on_click_action=test_message, transparent=1),

        Button(x=100, y=500, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='No Delay', on_click_action=test_message,
               text_size=35,
               transparent=0, click_delay=0),

        Button(x=100, y=600, screen=MAIN_SCREEN,
               border_color=(100, 100, 255),
               text='moveable', on_click_action=test_message,
               text_size=35,
               transparent=0, click_delay=0, moveable=1),
    )
