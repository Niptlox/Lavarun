from Texture import *

# статстический размер кубика
STATIC_TILE_SIZE = 32
# рефльный размер кубика
TILE_SIZE = 40
TILE_SIZEL = (TILE_SIZE, TILE_SIZE)

N_DIRT = 1
N_METAL = 2
N_NONE = 3
# со всеми с кем взамидоцствуем 100 < N < 200
N_SPIKE = 101
N_LAVA = 102
path_tile = r"data\sprites\tiles\\"
tiles_frames = {
    N_DIRT: get_texture_size(path_tile + "dirt.png", size=TILE_SIZEL),
    N_METAL: get_texture_size(path_tile + "metal.png", size=TILE_SIZEL),
    N_NONE: get_texture_size(path_tile + "none.png", size=TILE_SIZEL),
    N_SPIKE: get_texture_size(path_tile + "spike.png", size=TILE_SIZEL, colorkey=COLORKEY),
    N_LAVA: get_texture_size(path_tile + "lava.png", size=TILE_SIZEL, colorkey=COLORKEY)
}


tiles_chars = {
    "#": N_DIRT,
    "w": N_SPIKE,
    "+": N_LAVA,
    "0": N_METAL,
    "?": N_NONE
}
