from UI.Window import *
from UI.ui import *

pygame.init()

# Фазы игры
# показать меню старта программы
P_MENUSTART = 1
# играем в бесконечную игры
P_GAMELOOP = 2
# выбираем карту
P_MENUMAPS = 3
# Играем на уже созданной карте
P_GAMEMAP = 4

class Game(Window):
    def __init__(self, size):
        super().__init__(size)
        self.size = size

    def setPhasa(self, phasa):
        super().setPhasa(phasa)
        if self.phasa == P_MENUSTART:
            self.scene = self.startMenu

    def initGame(self):
        self.startMenu = StartMenu(self.size, lambda: print("START"))
        self.setPhasa(P_MENUSTART)


if __name__ == '__main__':
    game = Game(SIZE)
    game.main()