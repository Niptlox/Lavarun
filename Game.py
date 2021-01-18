import pygame
from Texture import *
from Button import *
from ui import *

pygame.init()

SIZE = (700, 400)

# Фазы игры
# показать меню старта программы
P_MENUSTART = 1
# играем в бесконечную игры
P_GAMELOOP = 2
# выбираем карту
P_MENUMAPS = 3
# Играем на уже созданной карте
P_GAMEMAP = 4

class Game():
    def __init__(self, size):
        self.size = size
        self.initPG()
        self.initGame()

    def main(self):
        self.mainLoop()

    def initPG(self):
        self.screen = pygame.display.set_mode(self.size)

    def setPhasa(self, phasa):
        self.phasa = phasa
        if self.phasa == P_MENUSTART:
            self.scene = self.startMenu


    def initGame(self):
        self.scene = None
        self.fps = 30
        self.startMenu = StartMenu(self.size, lambda: print("START"))


        self.setPhasa(P_MENUSTART)


    def mainLoop(self):
        self.clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.scene.update(event)


            screen.fill((0, 0, 0))
            self.scene.draw(screen)
            self.clock.tick(self.fps)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game(SIZE)
    game.main()