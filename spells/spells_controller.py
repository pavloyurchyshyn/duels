from common_things.common_objects_lists_dicts import SPELLS_LIST


def update_spells():
    for spell in SPELLS_LIST.copy():
        spell.update()
        if spell.dead:
            SPELLS_LIST.remove(spell)
