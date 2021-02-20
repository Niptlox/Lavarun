import pygame
from Texture import *


# Сделаем не сделаем фиг знает..........
# Оно не не рабочее
class Frame(pygame.sprite.Sprite):
    # image = load_image("bomb.png")
    # image_boom = load_image("boom.png")

    def __init__(self, rect, bg=None, groups=[]):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(*groups)

        self.rect = pygame.Rect(rect)
        if bg is not None:
            if isColor(bg):
                self.bg = get_texture_size(bg, size=self.rect.size)
                self.color = bg
            else:
                self.bg = get_texture(bg, colorkey=COLORKEY)
                if not (self.rect.width == 0 and self.rect.height == 0):
                    self.bg = pygame.transform.scale(self.bg, self.rect.size)
                else:
                    self.rect.size = self.bg.rect.size[:]
        else:
            self.bg = pygame.Surface(self.rect.size)

        self.groupObjs = pygame.sprite.LayeredUpdates()
        # self.frames = []
        self.image = pygame.Surface(self.rect.size)
        self.screenRect = self.rect
        self.offsetXY = [0, 0]


    def setXY(self, xy):
        x, y = xy
        ax, ay = x - self.rect.x, y - self.rect.y
        self.rect.move_ip(*xy)
        if self.rect is not self.screenRect:
            sx, sy = self.screenRect.x + ax, self.screenRect.y + ay
            self.screenRect.move_ip(sx, sy)

    def setOffset(self, offsetXY):
        self.offsetXY = offsetXY

    def update(self, *args):
        # print("update", self.__class__, args)
        if args:
            event = args[0]
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
                pos = event.pos
                if self.rect.collidepoint(pos):
                    event.pos = pos[0] - self.rect.x + self.offsetXY[0] , pos[1] - self.rect.y + self.offsetXY[1]
                    # event = pygame.event.Event(event.type, pos=npos)
                    self.groupObjs.update(event)
            else:
                self.groupObjs.update(event)

    def redraw(self):
        self.image.blit(self.bg, (0, 0))
        # self.groupObjs.draw(self.image)
        self.drawFrames()
        # self.drawFrames(self.image)

    def draw(self, screen):
        self.redraw()
        screen.blit(self.image, self.rect)
        # print(screen, (self.image, self.rect))

    def drawFrames(self):
        # print("drawFrames start")
        frames = self.groupObjs
        rectArea = pygame.Rect((self.offsetXY, self.rect.size))
        rectFrames = tuple(map(lambda it: it.rect, frames))
        # print(rectArea, rectFrames)
        for itemNum in rectArea.collidelistall(rectFrames):
            # item = frames[itemNum]
            item = frames.get_sprite(itemNum)
            pos = item.rect.x - self.offsetXY[0], item.rect.y - self.offsetXY[1]
            item.redraw()
            self.image.blit(item.image, pos)
            # pygame.image.save(item.image, f"data/exp/sp1{itemNum}.png")
            # print("drawItem", pos, item.rect, item, item.image, item.color)
            # input(" pygame.image.save(self")

        # screen.blit(self.image, self.rect, area=self.rect)
        # print("drawFrames stop")

    def add_frame(self, item):
        self.groupObjs.add(item)
        # self.frames.append(item)

    def add_frames(self, items):
        for item in items:
            self.groupObjs.add(item)
        # self.frames.append(item)

    def convert_func_coords(self, xy, static_size):
        x, y = xy
        sw, sh = static_size
        x = int(x * self.rect.w / sw)
        y = int(y * self.rect.h / sh)
        return x, y

    # Перещёт координат из прцентов
    def proc_coords(self, proc_xy):
        x, y = self.rect.w * proc_xy[0], self.rect.h * proc_xy[1]
        return x, y

    # Перещёт размера из прцентов
    def proc_size(self, proc_size):
        w, h = self.rect.w * proc_size[0], self.rect.h * proc_size[1]
        return w, h

    def set_pos_center(self, rect):
        self.rect.center = rect.center

    def start_scene(self, window):
        pass

    def quit(self):
        pass




