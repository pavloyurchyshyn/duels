class ArenaErrors(Exception):
    pass


class ClosedCellError(ArenaErrors):
    """
    Raise when cell is closed.
    """

    def __init__(self, *cell_coordinates):
        self.cell_coordinates = cell_coordinates

    def __str__(self):
        return f'Cell {self.cell_coordinates} is closed.'


class CellOutOfWorld(ArenaErrors):
    """
    Raise when cell is not in world.
    """

    def __init__(self, *cell_coordinates):
        self.cell_coordinates = cell_coordinates

    def __str__(self):
        return f'Cell {self.cell_coordinates} out of map.'


class DeadCellError(ArenaErrors):
    """
    Raise when cell is dead/non playable.
    """

    def __init__(self, *cell_coordinates):
        self.cell_coordinates = cell_coordinates

    def __str__(self):
        return f'Cell {self.cell_coordinates} is dead.'
