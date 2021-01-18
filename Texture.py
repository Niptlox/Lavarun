import pygame
import os
import sys

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

COLORKEY = GREEN


def get_texture(texture, colorkey=None):
    if texture is None:
        return None
    if type(texture) == str:
        return load_image(texture, colorkey)
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
