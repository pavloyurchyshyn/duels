import time

start = time.time()

num = 1000

test_x, test_y = 200, 200

args = {(x, y) for x in range(num) for y in range(num)}
print('create', time.time() - start)

start = time.time()

a = [(x, y) in args for x in range(test_x) for y in range(test_y)]

print(time.time() - start)

cell_size = 10


# ------------------------------

def normalize_cell(x, y):
    return (x // cell_size) * cell_size, (y // cell_size) * cell_size


start = time.time()
args = {}
for x in range(0, num, cell_size):
    for y in range(0, num, cell_size):
        args[(x, y)] = set()

for x in range(num):
    for y in range(num):
        args[normalize_cell(x, y)].add((x, y))
print('create', time.time() - start)

start = time.time()

a = [(x, y) in args[normalize_cell(x, y)] for x in range(test_x) for y in range(test_y)]


print(time.time() - start)

