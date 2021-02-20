import pygame



STATIC_SIZE = (800, 500)

SIZE = STATIC_SIZE
SIZE = (700, 400)

class Window:
    RECT = pygame.Rect(((0, 0), SIZE))

    def __init__(self, size):
        self.size = size
        self.screen = None
        self.phasa = None
        self.scene = None
        self.fps = 30
        self.initPG()
        self.initGame()

    def main(self):
        self.mainLoop()

    def initPG(self):
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
                    self.scene.quit()
                    running = False
                self.scene.update(event)

            # screen.fill((0, 0, 0))
            self.scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()




