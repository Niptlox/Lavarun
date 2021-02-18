from random import randint
from Tiles import *

LEVEL_AUTO = -1
LEVEL_PATTERN = -2

CHUNK_SIZE = 16


def generation_chunk(xy, level=-1):
    if level == LEVEL_AUTO:
        chunk_data = auto_generation(xy)
    elif level == LEVEL_PATTERN:
        chunk_data = pattern_generation(xy)
    return chunk_data


def auto_generation(xy):
    x, y = xy
    chunk_data = []
    i = 0
    m_a_g = [None] * CHUNK_SIZE
    old_tile_type = None
    for y_pos in range(CHUNK_SIZE - 1, -1, -1):
        m_a_g_old = m_a_g
        m_a_g = [None] * CHUNK_SIZE
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing
            if target_y == 6 and randint(0, 2) == 1:
                tile_type = N_DIRT
            elif target_y == 3 and randint(0, 3) == 1:
                tile_type = N_DIRT

            elif target_y == 9 and (randint(0, 5) == 1 or old_tile_type == N_LAVA and randint(0, 10) == 1):
                tile_type = N_LAVA
            elif target_y > 8:
                tile_type = N_DIRT  # dirt
            elif m_a_g_old[x_pos] == N_DIRT and randint(0, 5) == 1:
                tile_type = N_SPIKE
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
            m_a_g[x_pos] = tile_type
            old_tile_type = tile_type
            i += 1

    return chunk_data


def pattern_generation(xy):
    x, y = xy
    chunk_data = []
    i = 0
    m_a_g = [None] * CHUNK_SIZE
    old_tile_type = None
    for y_pos in range(CHUNK_SIZE - 1, -1, -1):
        m_a_g_old = m_a_g
        m_a_g = [None] * CHUNK_SIZE
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0  # nothing
            if target_y == 6 and randint(0, 2) == 1:
                tile_type = N_DIRT
            elif target_y == 3 and randint(0, 3) == 1:
                tile_type = N_DIRT

            elif target_y == 9 and (randint(0, 5) == 1 or old_tile_type == N_LAVA and randint(0, 10) == 1):
                tile_type = N_LAVA
            elif target_y > 8:
                tile_type = N_DIRT  # dirt
            elif m_a_g_old[x_pos] == N_DIRT and randint(0, 5) == 1:
                tile_type = N_SPIKE
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
            m_a_g[x_pos] = tile_type
            old_tile_type = tile_type
            i += 1

    return chunk_data
