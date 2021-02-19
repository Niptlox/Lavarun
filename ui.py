from UI.Button import *
from UI.Frame import *
from UI.Text import *
from UI.Window import STATIC_SIZE
from DataLoader import get_max_score

pygame.init()


class StartMenu(Frame):
    background = get_texture(r"data\sprites\bgStart.png")

    def __init__(self, size, funcStartEasy, funcStartHard):
        super().__init__(((0, 0), size), self.background)
        imgB_up, imgB_in, imgB_down = openImagesButton(r"data\sprites\buttons\StartBut.png")
        # xy_but_1 = self.convert_func_coords((100, 120), STATIC_SIZE)
        xy_but_1 = self.proc_coords((0.08, 0.29))
        self.butStart = Button(xy_but_1, imgB_up, imgB_in, imgB_down, funcStartEasy, size=(170, 40))
        xy_but_2 = xy_but_1[0], xy_but_1[1] + 60
        self.butStart2 = Button(xy_but_2, imgB_up, imgB_in, imgB_down, funcStartHard, size=(170, 40))
        # xy_labelScore = self.convert_func_coords((300, 120), STATIC_SIZE)
        xy_labelScore = self.proc_coords((0.38, 0.29))
        self.labelScore = Label((xy_labelScore, (170, 30)), bg=BLACK)
        self.score_update()
        self.groupBts = pygame.sprite.LayeredUpdates((self.butStart, self.butStart2))

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


class StartMenu_old(pygame.sprite.Sprite):
    background = get_texture(r"data\sprites\bgStart.png")

    def __init__(self, size, funcStart):
        super().__init__()
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.Surface(self.rect.size)
        self.background = StartMenu.background
        imgB_up, imgB_in, imgB_down = openImagesButton(r"data\sprites\buttons\StartBut.png")
        self.butStart = Button((100, 120), imgB_up, imgB_in, imgB_down, funcStart, size=(170, 40))
        self.butStart2 = Button((100, 190), imgB_up, imgB_in, imgB_down, lambda: print("START2"), size=(170, 40))
        self.labelScore = Label(((100, 80), (170, 30)), bg=BLACK, text=f"RECORD: {get_max_score()}")
        self.groupBts = pygame.sprite.LayeredUpdates((self.butStart, self.butStart2))

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
