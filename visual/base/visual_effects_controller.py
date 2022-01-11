from common_things.common_objects_lists_dicts import PARTICLE_LIST_L1, PARTICLE_LIST_L0
from common_things.singletone import Singleton
from settings.game_stages_constants import ROUND_PAUSE_STAGE, MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE, ROUND_STAGE, MULTIPLAYER_CLIENT_ROUND_STAGE


class VisualEffectsController(metaclass=Singleton):
    LAYERS = {0: PARTICLE_LIST_L0,
              1: PARTICLE_LIST_L1}

    last_stage = None

    @staticmethod
    def cleaner_decorator(func):
        round_stages = (ROUND_PAUSE_STAGE, ROUND_STAGE)
        m_round_stages = (MULTIPLAYER_CLIENT_ROUND_STAGE, MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE)

        def wrapper(*args, **kwargs):
            s = kwargs.get('stage')
            l_s = VisualEffectsController.last_stage

            if l_s in round_stages:
                if l_s == ROUND_STAGE and s != ROUND_PAUSE_STAGE:
                    VisualEffectsController.clear()

                elif l_s == ROUND_PAUSE_STAGE and s != ROUND_STAGE:
                    VisualEffectsController.clear()

            elif l_s in m_round_stages:
                if l_s == MULTIPLAYER_CLIENT_ROUND_STAGE and s != MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE:
                    VisualEffectsController.clear()
                if l_s == MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE and s != MULTIPLAYER_CLIENT_ROUND_STAGE:
                    VisualEffectsController.clear()
            else:
                VisualEffectsController.clear()

            VisualEffectsController.last_stage = s
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def add_effect(effect, layer=1, layers=None):
        if layers:
            for layer_ in layers:
                VisualEffectsController.LAYERS[layer_].append(effect)
        else:
            VisualEffectsController.LAYERS[layer].append(effect)

    @staticmethod
    def update():
        for layer, effects in VisualEffectsController.LAYERS.items():
            for effect in effects.copy():
                effect.update()
                if effect.dead:
                    VisualEffectsController.LAYERS[layer].remove(effect)

    @staticmethod
    def clear():
        for layer in VisualEffectsController.LAYERS.values():
            layer.clear()

    @staticmethod
    def draw():
        for effects in VisualEffectsController.LAYERS.values():
            for effect in effects:
                effect.draw()

    @staticmethod
    def draw_layer(layer):
        for effect in VisualEffectsController.LAYERS[layer]:
            effect.draw()

    @staticmethod
    def effects():
        return PARTICLE_LIST_L1
