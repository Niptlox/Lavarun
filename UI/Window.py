import pygame
import  os


# os.environ['SDL_VIDEO_CENTERED'] = '0'

STATIC_SIZE = (800, 500)

SIZE = STATIC_SIZE
# SIZE = (700, 400)
# SIZE = (1200, 900)

SIZE_COF = (SIZE[0] * SIZE[1]) / (STATIC_SIZE[0] * STATIC_SIZE[1])

class Window:
    RECT = pygame.Rect(((0, 0), SIZE))

    def __init__(self, size):
        self.size = size
        self.screen = None
        self.phasa = None
        self.scene = None
        self.fps = 30
        self.inFullScreen = False
        self.initPG()
        self.initGame()

    def main(self):
        self.mainLoop()

    def initPG(self):
        self.screen = pygame.display.set_mode(self.size)

    def full_screen(self):
        pos_x = 400
        pos_y = 400
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        self.inFullScreen = not self.inFullScreen
        if self.inFullScreen:
            self.screen = pygame.display.set_mode(self.size, flags=pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode(self.size)



    def setPhasa(self, phasa):
        self.phasa = phasa
        if self.phasa is None:
            self.scene = None

    def newScene(self):
        self.scene.start_scene(self)

    def initGame(self):
        self.setPhasa(None)

    def mainLoop(self):
        self.clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    running = False
                self.scene.update(event)

            # screen.fill((0, 0, 0))
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

    def quit(self):
        self.scene.quit()
        pygame.quit()
        exit()




