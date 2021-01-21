import pygame
import os
import sys
from pygame import Color

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

COLORKEY = GREEN

def isColor(arg):
    if type(arg) is pygame.Color or (type(arg) in (tuple, list) and 3 <= len(arg) <= 4):
        return True
    return False

def get_texture(texture, colorkey=None):
    if texture is None:
        return None
    if type(texture) is str:
        return load_image(texture, colorkey)
    # if type(texture) is pygame.Color:
    #     return
    return texture

def get_texture_size(texture, size=None, colorkey=None):
    if texture is None:
        return None
    if type(texture) is str:
        return load_image(texture, colorkey)
    if isColor(texture) and size is not None:
        surf = pygame.Surface(size)
        surf.fill(texture)
        texture = surf
    return texture

def load_image(name, colorkey=None):
    fullname = name #os.path.join('data', name)
    # если файл не существует, то выходим
    # fullname = r"BetaIMG.png"
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    return image
