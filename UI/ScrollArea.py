from UI.Frame import *

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
        self.sizeAllFrames = [0, 0]

    def addOffset(self, ax=0, ay=0):
        self.offsetXY[0] += ax
        self.offsetXY[1] += ay

        ss = -1
        if self.lockScrollBorderItem and len(self.groupObjs) > 0:

            if self.orientation == HORIZONTAL:
                if self.offsetXY[0] < 0:
                    self.offsetXY[0] = 0
                ss = self.sizeAllFrames[0] - self.rect.w + self.hspace
                # print("offsetXY", self.offsetXY, ss, self.rect.w, self.sizeAllFrames[0])
                if self.rect.w < self.sizeAllFrames[0] and self.offsetXY[0] > ss:
                    self.offsetXY[0] = ss
            if self.orientation == VERTICAL:
                if self.offsetXY[1] < 0:# or self.rect.h > self.sizeAllFrames[1]:
                    self.offsetXY[1] = 0
                ss = self.sizeAllFrames[1] - self.rect.h + self.vspace
                # print("offsetXY", self.offsetXY, ss, self.rect.h, self.sizeAllFrames[1])
                if self.rect.h < self.sizeAllFrames[1] and self.offsetXY[1] > ss:
                    self.offsetXY[1] = ss



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
        self.sizeAllFrames[0] = xy[0] + item.rect.w
        self.sizeAllFrames[1] = xy[1] + item.rect.h
        item.rect.move_ip(*xy)
        self.add_frame(item)

    def addItem(self, *items):
        if items:
            for item in items:
                self.addItemOne(item)
            self.redraw()
