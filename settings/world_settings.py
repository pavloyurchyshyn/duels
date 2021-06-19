CELL_PICTURE_SIZE = 200
WORLD_ARENA_PICTURE_SIZE = [1000, 1000]

WORLD_LINES = WORLD_ARENA_PICTURE_SIZE[1] // CELL_PICTURE_SIZE + 1
WORLD_COLUMNS = WORLD_ARENA_PICTURE_SIZE[0] // CELL_PICTURE_SIZE + 1


if WORLD_ARENA_PICTURE_SIZE[0] % CELL_PICTURE_SIZE or WORLD_ARENA_PICTURE_SIZE[1] % CELL_PICTURE_SIZE:
    raise Exception('Wrong CELL or World_Arena pictures size')
