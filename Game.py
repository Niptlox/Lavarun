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
        elif self.phasa == P_GAMELOOP:
            self.frameGame.newGame(-1)
            self.scene = self.frameGame

    def initGame(self):
        import World
        self.startMenu = StartMenu(self.size, lambda :self.setPhasa(P_GAMELOOP))
        world = World.World(display_size=self.size)
        self.frameGame = World.GameFrame(((0, 0), self.size), world)
        self.setPhasa(P_MENUSTART)
        # self.setPhasa(P_GAMELOOP)


if __name__ == '__main__':
    game = Game(SIZE)
    game.main()
