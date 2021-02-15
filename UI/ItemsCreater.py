from UI.Button import *
from UI.Window import *
from UI.ScrollArea import *

pygame.init()

P_MAIN = 1


class ItemsCreater(Frame):
    def __init__(self, rect):
        super().__init__(rect, Color("Blue"))
        self.initUI()

    def initUI(self):
        w_item, h_item = 60, 30
        space_items = 5;
        self.scrollArea = ScrollArea((10, 10, 300, 400), orientation=VERTICAL, bg=WHITE, step=2 *(h_item + space_items - 5),
                                     spaceItems=space_items
                                     )
        n = 10
        for i in range(n):
            frame = Frame(((0, 0), (w_item, h_item)), bg=(15 * i, 20 * i + 3, 100))
            self.scrollArea.addItem(frame)

        n = 3
        for i in range(n):
            # frame = Frame(((0, 0), (w_item, h_item)), bg=(15 * i, 20 * i + 3, 100))
            # frame = Button(((0, 0), (w_item, h_item)), bg=(15 * i, 20 * i + 3, 100))
            imgB_up, imgB_in, imgB_down = openImagesButton(r"data\sprites\buttons\StartBut.png")
            butStart = Button((0, 0), imgB_up, imgB_in, imgB_down, lambda ii=i: print(f"START {ii}"), size=(170, 40))
            self.scrollArea.addItem(butStart)

        # self.add_frame(scrollArea)

    def draw(self, screen):
        self.scrollArea.draw(screen)
        # print(self.scrollArea)

    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5:
                    self.scrollArea.shift(FORWARD)
                if event.button == 4:
                    self.scrollArea.shift(BACK)
            self.scrollArea.update(event)


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
    itMainCreater = ItemsCreaterMain((700, 600))
    itMainCreater.main()
