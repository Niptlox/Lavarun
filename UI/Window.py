import pygame
import os
from Texture import FPSFONT


# os.environ['SDL_VIDEO_CENTERED'] = '0'

STATIC_SIZE = (1600, 1000)

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
        self.show_fps = True

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



    def setPhase(self, phasa):
        self.phasa = phasa
        if self.phasa is None:
            self.scene = None

    def newScene(self):
        if self.scene:
            self.scene.start_scene(self)

    def initGame(self):
        self.clock = pygame.time.Clock()
        self.setPhase(None)

    def redraw(self):
        self.scene.draw(self.screen)
        if self.show_fps:
            surface_fps = FPSFONT.render(str(round(self.clock.get_fps(), 2))+ "fps", False, (0, 250, 0))
            self.screen.blit(surface_fps, (2, 2))

    def mainLoop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                    running = False
                self.scene.update(event)
            self.redraw()
            # screen.fill((0, 0, 0))
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

    def quit(self):
        self.scene.quit()
        pygame.quit()
        exit()




