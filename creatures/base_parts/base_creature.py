from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
from world_arena.world import GLOBAL_WORLD
from creatures.base_parts.base_brain import BaseBrain


class Creature:
    """
    Creature consist of brains and body.
    Firs of brains control body.

    """
    WORLD = GLOBAL_WORLD
    G_CLOCK = GLOBAL_CLOCK
    R_CLOCK = ROUND_CLOCK

    def __init__(self, brain: BaseBrain,
                 body: object
                 ):
        """
        :param brain: parts which calculating steps, first brain -> main
        :param body: body which contain legs, arms, head, etc doing commands from braiin

        In any list using only first alive element.
        """
        self._brain = brain  # parts which controlling body
        self._body = body

        brain.set_body(body)

    def _update(self):
        commands = self._brain.update()
