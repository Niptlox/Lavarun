from Window import *
from Frame import *

HORIZONTAL = 1
VERTICAL = 2
BACK = -1
FORWARD = 1


class ScrollArea(Frame):

    def __init__(self, rect, items=(), bg=None, orientation=HORIZONTAL, step=5, spaceItems=5, hspace=5, vspace=5,
                 lockScrollBorderItem=True):
        """ Поверхность для отображение скролируемых объектов
            rect - ограничивающий прямоуголиник
            bg - фон задней поверхности (imagePath/pygame.Surface)
            orientation - ориентация прокрутки (HORIZONTAL/VERTICAL)
            step - шаг в пикселях при прокрутке
            spaceItems - расстояние между элементами
            vspace, hspace - расстояния от элемента до края
            lockScrollBorderItem - если True, то не выходим за граници скролинга
            """
        if bg is None:
            bg = Color("Black")
        super().__init__(rect, bg)
        self.orientation = orientation
        self.step = step
        self.spaceItems = spaceItems
        self.vspace, self.hspace = vspace, hspace
        self.lockScrollBorderItem = lockScrollBorderItem
        self.addItem(*items)

    def addOffset(self, ax=0, ay=0):
        oox, ooy = self.offsetXY
        self.offsetXY[0] += ax
        self.offsetXY[1] += ay
        if self.lockScrollBorderItem and not self.groupObjs.empty():
            firstItemR = self.groupObjs.get_sprite(0).rect
            lastItemR = self.groupObjs.get_sprite(0).rect
            if self.orientation == HORIZONTAL:
                if self.offsetXY[0] > 0:
                    self.offsetXY[0] = 0
                if lastItemR.x < ax + self.hspace:
                    self.offsetXY[0] = 0


    def shift(self, direction=FORWARD):
        if self.orientation == HORIZONTAL:
            self.addOffset(ax=self.step * direction)
        elif self.orientation == VERTICAL:
            self.addOffset(ay=self.step * direction)

    def addItemOne(self, item):
        if len(self.groupObjs) > 0:
            lastItem = self.groupObjs.get_sprite(-1)
            if self.orientation == HORIZONTAL:
                xy = (lastItem.rect.x + lastItem.rect.width + self.spaceItems,
                      self.vspace)
            else:
                xy = (self.hspace,
                      lastItem.rect.y + lastItem.rect.height + self.spaceItems)
        else:
            xy = (self.hspace, self.vspace)
        item.rect.move_ip(*xy)
        self.add_frame(item)

    def addItem(self, *items):
        if items:
            for item in items:
                self.addItemOne(item)
            self.redraw()
