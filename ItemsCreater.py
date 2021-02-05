import pygame
from Texture import *
from Button import *
from Window import *
from Frame import *
from ScrollArea import *

pygame.init()

P_MAIN = 1


class ItemsCreater(Frame):
    def __init__(self, rect):
        super().__init__(rect, Color("Blue"))
        self.initUI()

    def initUI(self):
        w_item, h_item = 60, 30
        space_items = 5;
        self.scrollArea = ScrollArea((10, 10, 300, h_item + 10), orientation=VERTICAL, bg=WHITE, step=h_item + space_items,
                                     spaceItems=space_items,
                                     )

        for i in range(10):
            frame = Frame(((0, 0), (w_item, h_item)), bg=(15 * i, 20 * i + 3, 100))
            self.scrollArea.addItem(frame)

        # self.add_frame(scrollArea)

    def draw(self, screen):
        self.scrollArea.draw(screen)
        # print(self.scrollArea)

    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scrollArea.shift(FORWARD)
                if event.button == 5:
                    self.scrollArea.shift(BACK)


class ItemsCreaterMain(Window):
    def __init__(self, size):
        super().__init__(size)
        self.size = size

    def setPhasa(self, phasa):
        super().setPhasa(phasa)
        if self.phasa == P_MAIN:
            self.scene = self.mainFrame

    def initGame(self):
        self.mainFrame = ItemsCreater(Window.RECT)
        self.setPhasa(P_MAIN)


if __name__ == '__main__':
    itMainCreater = ItemsCreaterMain(SIZE)
    itMainCreater.main()
