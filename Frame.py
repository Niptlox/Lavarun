import pygame
from Texture import *


# Сделаем не сделаем фиг знает..........
# Оно не не рабочее
class Frame(pygame.sprite.Sprite):
    # image = load_image("bomb.png")
    # image_boom = load_image("boom.png")

    def __init__(self, rect, bg=None, group=None):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        if group is not None:
            super().__init__(group)
        else:
            super().__init__()
        self.rect = pygame.Rect(rect)
        if bg is not None:
            if isColor(bg):
                self.bg = get_texture_size(bg, size=self.rect.size)
            else:
                self.bg = get_texture(bg, colorkey=COLORKEY)
                self.bg = pygame.transform.scale(self.bg, self.rect.size)
        else:
            self.bg = pygame.Surface(self.rect.size)

        self.groupObjs = pygame.sprite.LayeredUpdates()
        self.frames = []
        self.image = pygame.Surface(self.rect.size)
        self.screenRect = self.rect
        self.offsetXY = (0, 0)

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

    def draw(self, screen):
        self.image.blit(self.bg, (0, 0))
        self.groupObjs.draw(screen)
        self.drawFrames(screen)

    def drawFrames(self, screen):
        rectArea = pygame.Rect((self.rect.size, self.offsetXY))
        print(rectArea, self.frames[0].rect)
        for item in rectArea.collidelistall(tuple(map(lambda it: it.rect, self.frames))):
            pos = item.rect.x - self.offsetXY[0], item.rect.y - self.offsetXY[1]
            print(pos)
            self.image.blit(item, pos)

        screen.blit(self.image, self.rect, area=self.rect)

    def add_frame(self, item):
        self.frames.append(item)




