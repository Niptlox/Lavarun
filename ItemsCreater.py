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
        super().__init__(rect, Color("Black"))
        self.initUI()

    def initUI(self):
        self.scrollArea = ScrollArea((10, 10, 100, 100))
        for i in range(10):
            frame = Frame(((0, 0), (60, 30)), bg=(25 * i, 25 * i + 3, 100))
            self.scrollArea.addItem(frame)

        # self.add_frame(scrollArea)

    def draw(self, screen):
        self.scrollArea.draw(screen)


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