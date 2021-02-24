from UI.Button import *
from UI.Frame import *
from UI.Text import *
from UI.Window import SIZE
from DataLoader import get_max_score

pygame.init()


class Menu(Frame):
    def __init__(self, rect, background, fromXY, puncts, step_xy=(10, 0),
                 font=TEXTFONT, color_scheme=DEF_COLOR_SCHEME_BUT):
        super().__init__(rect, self.background)
        for punct in puncts:
            text, imgs, func = punct
            if text is not None:
                but = Button(rect)


class StartMenu(Frame):
    background = get_texture(r"data\sprites\bgStart.png")

    def __init__(self, funcStartEasy, funcStartHard, funcFullScreen, funcQuit):
        super().__init__(((0, 0), SIZE), self.background)
        # super().__init__(SIZE, self.background)
        imgB_up, imgB_in, imgB_down = openImagesButton(r"data\sprites\buttons\StartBut.png", None)

        # xy_but_1 = self.convert_func_coords((100, 120), STATIC_SIZE)
        size_but = (imgB_up.get_width() // 5, imgB_up.get_height() // 5)
        step = 60
        bx, by = self.proc_coords((0.08, 0.29))
        self.butStart = Button(((bx, by), size_but), imgB_up, imgB_in, imgB_down, funcStartEasy)
        by += step * 2
        self.butStart2 = Button(((bx, by), size_but), imgB_up, imgB_in, imgB_down, funcStartHard)
        by += step * 2
        # self.butStart2 = Button(((bx, by), size_but), imgB_up, imgB_in, imgB_down, funcStartHard)
        # by += step
        # xy_labelScore = self.convert_func_coords((300, 120), STATIC_SIZE)

        but_surf_full = createImagesButton(size_but, "FullScreen")
        self.butFullS = Button(((bx, by), size_but), *but_surf_full, func=funcFullScreen)
        by += step * 2
        but_surf_quit = createImagesButton(size_but, "Exit")
        self.butQuit = Button(((bx, by), size_but), *but_surf_quit, func=funcQuit)

        xy_labelScore = self.proc_coords((0.38, 0.29))
        self.labelScore = Label((xy_labelScore, (170, 30)), bg=BLACK)
        self.score_update()
        self.groupBts = pygame.sprite.LayeredUpdates((self.butStart, self.butStart2, self.butFullS, self.butQuit))

    def update(self, *args):
        if args:
            event = args[0]
            self.groupBts.update(event)

    def draw(self, screen):
        if self.background.get_size != self.rect.size:
            self.background = pygame.transform.scale(StartMenu.background, self.rect.size)

        self.image.blit(self.background, (0, 0))
        self.groupBts.draw(self.image)
        self.labelScore.draw(self.image)
        screen.blit(self.image, self.rect)

    def score_update(self):
        self.labelScore.setText(f"RECORD: {get_max_score()}")

    def start_scene(self, window):
        self.score_update()


# class StartMenu_old(pygame.sprite.Sprite):
#     background = get_texture(r"data\sprites\bgStart.png")
#
#     def __init__(self, size, funcStart):
#         super().__init__()
#         self.rect = pygame.Rect((0, 0), size)
#         self.image = pygame.Surface(self.rect.size)
#         self.background = StartMenu.background
#         imgB_up, imgB_in, imgB_down = openImagesButton(r"data\sprites\buttons\StartBut.png")
#         self.butStart = Button((100, 120), imgB_up, imgB_in, imgB_down, funcStart, size=(170, 40))
#         self.butStart2 = Button((100, 190), imgB_up, imgB_in, imgB_down, lambda: print("START2"), size=(170, 40))
#         self.labelScore = Label(((100, 80), (170, 30)), bg=BLACK, text=f"RECORD: {get_max_score()}")
#         self.groupBts = pygame.sprite.LayeredUpdates((self.butStart, self.butStart2))
#
#     def update(self, *args):
#         if args:
#             event = args[0]
#             self.groupBts.update(event)
#
#     def draw(self, screen):
#         if self.background.get_size != self.rect.size:
#             self.background = pygame.transform.scale(StartMenu.background, self.rect.size)
#
#         self.image.blit(self.background, (0, 0))
#         self.groupBts.draw(self.image)
#         self.labelScore.draw(self.image)
#         screen.blit(self.image, self.rect)


def main():
    size = (1200, 700)
    screen = pygame.display.set_mode(size)
    startMenu = StartMenu(size, lambda: print("START"))
    # group = pygame.sprite.LayeredUpdates((but))
    fps = 30
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                running = False
            startMenu.update(event)

        screen.fill((0, 0, 0))
        startMenu.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
