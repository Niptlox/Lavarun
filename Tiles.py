from Texture import *

TILE_SIZE = 40
TILE_SIZEL = (TILE_SIZE, TILE_SIZE)

N_DIRT = 1
# со всеми с кем взамидоцствуем 100 < N < 200
N_SPIKE = 101
N_LAVA = 102
path_tile = r"data\sprites\tiles\\"
tiles_frames = {
    N_DIRT: get_texture_size(path_tile + "dirt.png", size=TILE_SIZEL),
    N_SPIKE: get_texture_size(path_tile + "spike.png", size=TILE_SIZEL, colorkey=COLORKEY),
    N_LAVA: get_texture_size(path_tile + "lava.png", size=TILE_SIZEL, colorkey=COLORKEY)
}
