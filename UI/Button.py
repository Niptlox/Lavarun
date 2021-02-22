import pygame
from Texture import *

DEF_COLOR_SCHEME_BUT = ((WHITE, GRAY, BLACK), (BLACK, BLACK, WHITE))


def openImagesButton(nameImg: str, colorkey=COLORKEY):
    path, extension = os.path.splitext(nameImg)
    imgUp = load_image(path + "_up" + extension, colorkey)
    imgIn = load_image(path + "_in" + extension, colorkey)
    imgDown = load_image(path + "_down" + extension, colorkey)
    return imgUp, imgIn, imgDown


def createImageButton(size, text="", bg=BLACK, font=TEXTFONT, text_color=WHITE, colorkey=COLORKEY):
    surf = get_texture_size(bg, size, colorkey=colorkey)

    texframe = font.render(text, False, text_color)
    texframe_rect = pygame.Rect(((0, 0), texframe.get_size()))
    # print("texframe_rect.center", texframe_rect, size)
    texframe_rect.centerx, texframe_rect.centery = size[0] // 2, size[1] // 2
    surf.blit(texframe, texframe_rect)
    return surf


def createImagesButton(size, text="", color_schema=DEF_COLOR_SCHEME_BUT, font=TEXTFONT, colorkey=COLORKEY):
    print("color_schema", [(bg, colort) for bg, colort in zip(color_schema[0], color_schema[1])])
    imgs_but = [createImageButton(size, text, bg, font=font, text_color=colort, colorkey=colorkey)
                for bg, colort in zip(color_schema[0], color_schema[1])]
    return imgs_but


def createVSteckButtons(size, center_x, start_y, step, images_buttons, funcs):
    y = start_y
    x = center_x - size[0] // 2
    step += size[1]
    buts = []
    for images_button, func in zip(images_buttons, funcs):
        but = Button(((x, y), size), *images_button, func=func)
        y += step
        buts.append(but)
    return buts


class Button(pygame.sprite.Sprite):
    # image = load_image("bomb.png")
    # image_boom = load_image("boom.png")

    def __init__(self, rect, imgUpB, imgInB=None, imgDownB=None, func=None, group=None, screenXY=None):
        # если рамеры == -1 то берётся размер кнопки
        self.func = func
        if group is not None:
            super().__init__(group)
        else:
            super().__init__()
        self.rect = rect = pygame.Rect(rect)
        xy = self.rect.x, self.rect.y
        if self.rect.w == -1 and self.rect.h == -1:
            size = None
        else:
            size = rect.size
        self.imgUpB = get_texture(imgUpB, colorkey=COLORKEY)
        self.image = self.imgUpB
        imgDownB = self.imgUpB if imgDownB is None else imgDownB
        imgInB = self.imgDownB if imgInB is None else imgInB
        self.imgDownB = get_texture(imgDownB, colorkey=COLORKEY)
        self.imgInB = get_texture(imgInB, colorkey=COLORKEY)

        self.mauseInButton = False
        self.mauseDownButton = False
        if size is None:
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = xy
        else:
            self.rect = pygame.Rect(xy, size)
            self.imgUpB = pygame.transform.scale(self.imgUpB, self.rect.size)
            self.imgDownB = pygame.transform.scale(self.imgDownB, self.rect.size)
            self.imgInB = pygame.transform.scale(self.imgInB, self.rect.size)
        self.image = self.imgUpB
        self.screenRect = self.rect if screenXY is None else pygame.Rect(screenXY, self.rect.size)
        # self.screenXY = screenXY

    def setXY(self, xy):
        x, y = xy
        ax, ay = x - self.rect.x, y - self.rect.y
        self.rect.move_ip(*xy)
        if self.rect is not self.screenRect:
            sx, sy = self.screenRect.x + ax, self.screenRect.y + ay
            self.screenRect.move_ip(sx, sy)

    def update(self, *args):
        if args:
            but = 1
            event = args[0]
            if event.type == pygame.MOUSEBUTTONUP and event.button == but:
                if self.mauseDownButton:
                    self.click()
                self.mauseDownButton = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == but:
                if self.screenRect.collidepoint(event.pos):
                    self.mauseInButton = True
                    self.mauseDownButton = True
            if event.type == pygame.MOUSEMOTION:
                if self.mauseInButton:
                    if not self.screenRect.collidepoint(event.pos):
                        self.mauseInButton = False
                        self.mauseDownButton = False
                else:
                    if self.screenRect.collidepoint(event.pos):
                        self.mauseInButton = True
        self.redraw()

    def click(self):
        if self.func:
            self.mauseInButton = False
            self.mauseDownButton = False
            self.redraw()
            self.func()
        else:
            print("Button down, but function not defined!!!")

    def inButton(self):
        if self.imgInB:
            self.image = self.imgInB

    def redraw(self):
        if self.mauseDownButton:
            self.image = self.imgDownB
        elif self.mauseInButton:
            self.image = self.imgInB
        else:
            self.image = self.imgUpB
