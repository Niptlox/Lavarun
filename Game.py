from UI.Window import *
from ui import *

pygame.init()

# Фазы игры
# показать меню старта программы
P_MENUSTART = 1
# играем в бесконечную игру
P_GAMELOOP_EASY = 10
P_GAMELOOP_NORMAL = 12
P_GAMELOOP_HARD = 14
P_GAMELOOP_RANDOM = 5
# выбираем карту
P_MENUMAPS = 20
# Играем на уже созданной карте
P_GAMEMAP = 30


class Game(Window):
    def __init__(self, size):
        super().__init__(size)
        self.size = size

    def setPhase(self, phasa):
        import World
        super().setPhase(phasa)
        if self.phasa == P_MENUSTART:  # начальное меню
            self.scene = self.startMenu
        elif self.phasa == P_GAMELOOP_EASY:  # легкий режим
            self.frameGame.newGame(-2, diff=World.EASY)
            self.frameGame.world.clear_map()
            self.scene = self.frameGame
        elif self.phasa == P_GAMELOOP_HARD:  # сложный режим
            self.frameGame.newGame(-2, diff=World.HARD)
            self.frameGame.world.clear_map()
            self.scene = self.frameGame
        elif self.phasa == P_GAMELOOP_RANDOM:  # рандомный режим
            self.frameGame.newGame(-1, diff=World.NORMAL)
            self.frameGame.world.clear_map()
            self.scene = self.frameGame
        self.newScene()

    def initGame(self):
        import World
        super().initGame()
        self.startMenu = StartMenu(lambda: self.setPhase(P_GAMELOOP_EASY),
                                   lambda: self.setPhase(P_GAMELOOP_HARD),
                                   lambda: self.setPhase(P_GAMELOOP_RANDOM),
                                   self.full_screen,
                                   self.quit)  # указываем что будут делать кнопки на главном меню
        # world = World.World(display_size=self.size)
        world = World.World()
        self.frameGame = World.GameFrame(((0, 0), self.size), world, to_main_menu=lambda: self.setPhase(P_MENUSTART))
        self.frameGame.setPhasa(World.P_GAMELOOPW)
        self.setPhase(P_MENUSTART)
        # self.setPhase(P_GAMELOOP)


if __name__ == '__main__':
    game = Game(SIZE)
    game.main()
