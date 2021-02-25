from random import randint, choice
from Tiles import *

LEVEL_AUTO = -1
LEVEL_PATTERN = -2

CHUNK_SIZE = 16
CHUNK_SIZE_DIS = CHUNK_SIZE * TILE_SIZE

EMPTY_CHUNK = [] * CHUNK_SIZE

TYPE_TXT = ".pat"
PATTERNS_PATH = "data\\patterns\\"


def load_pattern(name, typep=TYPE_TXT):
    if typep == TYPE_TXT:
        file_path = PATTERNS_PATH + name + typep
        with open(file_path) as f:
            ar_pat = f.read().split("\n")
            print(ar_pat)
            y = 0
            out_ar = [[None] * CHUNK_SIZE for i in range(CHUNK_SIZE)]

            for st in (ar_pat[i] for i in range(CHUNK_SIZE)):
                a_st = [None] * CHUNK_SIZE
                x = 0
                for char in st:
                    if char != " ":
                        a_st[x] = tiles_chars.get(char, N_NONE)
                    x += 1
                out_ar[y] = a_st
                y += 1
        return out_ar


START_PATTERN = load_pattern("Start")
START_PATTERN_1 = load_pattern("Start-1")
PLAT_PATTERN = load_pattern("Plat")  # металлическая платформа...
LAVA_PATTERN = load_pattern("Lava")
RANDOM_PATTERN_NAMES = ["r1", "r2", "r3", "r4", "r5"]
RANDOM_PATTERNS = []
for i in RANDOM_PATTERN_NAMES:
    RANDOM_PATTERNS.append(load_pattern(i))
OLD_PATTERN = 0
patternGenOrder = [[1, 2], [3, 4], [2, 4, 5], [1, 2, 3], [4], [1]]  # Определяет порядок в котором генерируются паттерны
# Первый подмассив, это те паттерны, которые могут появиться после чанка спавна,
# 2 подмассив, это те паттерны, которые могут появиться после чанка с номером 2 и т.д.
# Сами паттерны берутся из RANDOM_PATTERN_NAMES(отсчет идет с единицы(0 обозначает чанк спавна))
print("PLAT_PATTERN", PLAT_PATTERN)


def generation_chunk(xy, level=-1):
    if level == LEVEL_AUTO:
        chunk_data = auto_generation(xy)
    elif level == LEVEL_PATTERN:
        chunk_data = pattern_generation(xy)
    return chunk_data


def get_chunk_of_pattern(xy, pattern):
    chunk = [((x + xy[0], y + xy[1]), pattern[y][x])
             for y in range(CHUNK_SIZE) for x in range(CHUNK_SIZE)
             if pattern[y][x] is not None]
    # print(*chunk, sep="\n")
    return chunk


def auto_generation(xy):
    x, y = xy
    # print("auto_generation", xy)
    chunk_data = []
    tile_xy = x * CHUNK_SIZE, y * CHUNK_SIZE
    if x == 0 and y == 0:
        chunk_data = get_chunk_of_pattern(tile_xy, START_PATTERN)
    # elif x == -1 and y == 0:
    #     chunk_data = get_chunk_of_pattern(tile_xy, START_PATTERN_1)
    elif x < 0 and y == 0:
        chunk_data = get_chunk_of_pattern(tile_xy, LAVA_PATTERN)
    elif x != 0 and y == 0 and randint(1, 5) == 1 and x % 2 == 0:
        chunk_data = get_chunk_of_pattern(tile_xy, PLAT_PATTERN)
    else:
        chunk_data = random_chunk(xy)
    return chunk_data


def random_chunk(xy):  # генерация случайного чанка
    x, y = xy
    i = 0
    m_a_g = [None] * CHUNK_SIZE
    old_tile_type = None
    chunk_data = []
    for y_pos in range(CHUNK_SIZE - 1, -1, -1):
        m_a_g_old = m_a_g
        m_a_g = [None] * CHUNK_SIZE
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing
            if target_y == 0 and randint(0, 3) == 1:
                tile_type = N_DIRT
            if target_y == 6 and randint(0, 4) == 1:
                tile_type = N_DIRT
            elif target_y == 3 and randint(0, 3) == 1:
                tile_type = N_DIRT
            elif target_y == 9 and (randint(0, 5) == 1 or old_tile_type == N_LAVA and randint(0, 5) == 1):
                tile_type = N_LAVA
            elif target_y == 9:
                tile_type = N_DIRT
            elif target_y > 9:
                tile_type = N_DIRTDOWN  # dirt
            if m_a_g_old[x_pos] == N_DIRT and randint(0, 3) == 1:
                tile_type = N_SPIKE
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
            m_a_g[x_pos] = tile_type
            old_tile_type = tile_type
            i += 1
    # print(chunk_data)
    return chunk_data


def pattern_generation(xy):
    global OLD_PATTERN
    x, y = xy
    if y == 0 and x == 0:
        OLD_PATTERN = 0
    chunk_data = []
    if y >= 1:
        for y_pos in range(CHUNK_SIZE - 1, -1, -1):
            for x_pos in range(CHUNK_SIZE):
                chunk_data.append([[x * CHUNK_SIZE + x_pos, y * CHUNK_SIZE + y_pos], 4])
        return chunk_data
    if y != 0:
        return EMPTY_CHUNK
    print(OLD_PATTERN)
    OLD_PATTERN = choice(patternGenOrder[OLD_PATTERN])
    tile_xy = x * CHUNK_SIZE, y * CHUNK_SIZE
    if x == 0 and y == 0:
        chunk_data = get_chunk_of_pattern(tile_xy, START_PATTERN)
    elif x < 0 and y == 0:
        chunk_data = get_chunk_of_pattern(tile_xy, LAVA_PATTERN)
    elif x != 0 and y == 0 and randint(1, 5) == 1 and x % 2 == 0:
        chunk_data = get_chunk_of_pattern(tile_xy, PLAT_PATTERN)
    else:
        chunk_data = get_chunk_of_pattern(tile_xy, RANDOM_PATTERNS[OLD_PATTERN - 1])
    return chunk_data