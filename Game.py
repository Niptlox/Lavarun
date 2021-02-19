from UI.Window import *
from ui import *

pygame.init()

# Фазы игры
# показать меню старта программы
P_MENUSTART = 1
# играем в бесконечную игры
P_GAMELOOP_EASY = 10
P_GAMELOOP_NORMAL = 12
P_GAMELOOP_HARD = 14
# выбираем карту
P_MENUMAPS = 20
# Играем на уже созданной карте
P_GAMEMAP = 30


class Game(Window):
    def __init__(self, size):
        super().__init__(size)
        self.size = size

    def setPhasa(self, phasa):
        super().setPhasa(phasa)
        if self.phasa == P_MENUSTART:
            self.scene = self.startMenu
        elif self.phasa == P_GAMELOOP_EASY:
            self.frameGame.newGame(-1)
            self.frameGame.world.clear_map()
            self.scene = self.frameGame
        self.newScene()

    def initGame(self):
        import World
        self.startMenu = StartMenu(self.size, lambda :self.setPhasa(P_GAMELOOP_EASY))
        world = World.World(display_size=self.size)
        self.frameGame = World.GameFrame(((0, 0), self.size), world, to_main_menu=lambda :self.setPhasa(P_MENUSTART))
        self.setPhasa(P_MENUSTART)
        # self.setPhasa(P_GAMELOOP)




if __name__ == '__main__':
    game = Game(SIZE)
    game.main()
