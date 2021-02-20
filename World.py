import pygame

from Texture import *
from Entities import *
from Chank import *
from DataLoader import *
from UI.Frame import *
from math import ceil  # округление в большую сторону
import pickle

HARD = 3
NORMAL = 2
EASY = 1


class World:
    COF_CAMERA_FRICTION = 0.1  # коэффициент для скольжения камеры

    def __init__(self, display_size=(720, 480)):
        self.game_map = {}
        self.level = None
        self.difficulty = None
        self.display_size = display_size
        self.display = pygame.Surface(display_size)

        ss = CHUNK_SIZE * TILE_SIZE
        self.display_chanks_size = (ceil((display_size[0]) / ss + 2), ceil((display_size[1]) / ss + 2))

        self.scroll = [0, 0]

        self.tile_rects = []  # для отображения физики
        self.tiles = []  # для отображения на экран
        self.entitys = []  # для взаимодействий
        self.player = Player((0, 0))

    def get_chunk(self, xy):
        if xy not in self.game_map:
            if self.level < 0:
                self.game_map[xy] = self.generation_chunk(xy, self.level)
            else:
                return
        return self.game_map[xy]

    def generation_chunk(self, xy, level=-1):
        chunk_data = generation_chunk(xy, level)
        return chunk_data

    def new_game(self, game_map=None, level=None, difficulty=None):
        self.game_map = game_map if game_map is not None else self.game_map
        self.level = level if level is not None else self.level
        if difficulty is not None:
            self.set_difficulty(difficulty)
        self.player.new_game()
        self.player.set_xy((self.display_size[0] // 2, self.display_size[1] // 2))
        self.scroll = [0, 0]

    def set_difficulty(self, diff):
        self.difficulty = diff
        player = self.player
        cof = 0.5
        if diff == EASY:
            player.max_oxygen = 5000 * cof
            player.oxygen_normal_spending = 1
            player.oxygen_jump_spending = 20
            player.score_coff = 1
        elif diff == NORMAL:
            player.max_oxygen = 3500 * cof
            player.oxygen_normal_spending = 1
            player.oxygen_jump_spending = 30
            player.score_coff = 1.3
        elif diff == HARD:
            player.max_oxygen = 1500 * cof
            player.oxygen_normal_spending = 1
            player.oxygen_jump_spending = 40
            player.score_coff = 2

    def clear_map(self):
        self.game_map = {}

    def update(self, *args):
        if args:
            self.get_event(*args)
        else:
            return self.update_rects()

    def update_rects(self):

        # Скользящие перемещение камеры
        offset = (self.display_size[0] // 2 - self.player.rect.w // 2,
                  self.display_size[1] // 2 - self.player.rect.h // 2)
        self.scroll[0] += (self.player.rect.x - self.scroll[0] - offset[0]) \
                          * self.COF_CAMERA_FRICTION
        self.scroll[1] += (self.player.rect.y - self.scroll[1] - offset[1]) \
                          * (self.COF_CAMERA_FRICTION * 2)

        scroll = [int(self.scroll[0]), int(self.scroll[1])]
        # Обновление, нахождение, всех спрайтов на экране
        self.tile_rects, self.tiles, self.entitys = self.update_display(scroll, self.display_size)
        # Обновление игрока, движение и тд
        self.player.update(tile_rects=self.tile_rects, entitys=self.entitys)
        if not self.player.alive:
            self.save_data()
            return False
        return True

    def redraw(self):
        self.display.fill((146, 144, 255))
        for tile in self.tiles:
            xy_tile = (tile[0][0] * TILE_SIZE - self.scroll[0], tile[0][1] * TILE_SIZE - self.scroll[1])
            type_tile = tile[1]
            self.display.blit(tiles_frames[type_tile], xy_tile)
        scroll = [int(self.scroll[0]), int(self.scroll[1])]
        self.player.draw(self.display, (self.player.rect.x - scroll[0], self.player.rect.y - scroll[1]))
        self.display.blit(self.player.surface_oxygen_bar, (20, 20))
        self.display.blit(self.player.surface_score, (self.display_size[0] - 120, 20))

    def draw(self, surface):
        self.redraw()
        surface.blit(pygame.transform.scale(self.display, surface.get_size()), (0, 0))

    def get_event(self, event):
        self.player.update(event)

    def update_display(self, scroll, display_size):
        self.tile_rects = tile_rects = []  # для отображения физики
        self.tiles = tiles = []  # для отображения на экран
        self.entitys = entitys = []  # для взаимодействий
        # display_rect_for_tiles = (scroll[0] // TILE_SIZE, scroll[1] // TILE_SIZE), (
        #     (display_size[0] + scroll[0] - 1) // TILE_SIZE, (display_size[1] + scroll[1] - 1) // TILE_SIZE)
        for y in range(self.display_chanks_size[1]):
            for x in range(self.display_chanks_size[0]):
                target_x = x + int(round(scroll[0] / (CHUNK_SIZE * TILE_SIZE))) - 1
                target_y = y + int(round(scroll[1] / (CHUNK_SIZE * TILE_SIZE))) - 1
                target_chunk = (target_x, target_y)
                chank = self.get_chunk(target_chunk)
                for tile in chank:
                    tile_xy = tile[0]
                    # if not (display_rect_for_tiles[0][0] <= tile_xy[0] <= display_rect_for_tiles[0][1] and
                    #         display_rect_for_tiles[1][0] <= tile_xy[1] <= display_rect_for_tiles[1][1]):
                    #     # за экраном
                    #     continue
                    tiles.append(tile)
                    # display.blit(tile_index[tile[1]], (tile[0][0] * 16 - scroll[0], tile[0][1] * 16 - scroll[1]))
                    # tile_xy =
                    if 1 <= tile[1] < 100:
                        # твердые блоки по типу земли
                        rect = pygame.Rect(tile_xy[0] * TILE_SIZE, tile_xy[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        tile_rects.append(rect)
                    if 101 <= tile[1] < 200:
                        # может твердые а может и нет, обекты для взаимного действия, допустим человечки
                        rect = pygame.Rect(tile_xy[0] * TILE_SIZE, tile_xy[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        entitys.append((rect, tile[1]))
        return tile_rects, tiles, entitys

    def save_data(self):
        max_score = max(get_max_score(), self.player.score)
        put_max_score(max_score)

    def pause(self):
        self.player.moving_right = False
        self.player.moving_left = False


P_GAMELOOPW = 1
P_GAMEPAUSEW = 2


class GameFrame(Frame):
    def __init__(self, rect, world, to_main_menu=None):
        super().__init__(rect, bg=BLACK)
        self.world = world
        self.to_main_menu = to_main_menu
        self.phasa = None
        self.scene = None
        self.running = True
        self.initUI()

    def initUI(self):
        self.frame_pause_menu = GamePause(self.proc_size((0.3, 0.5)), self.rect,
                                          lambda: self.setPhasa(P_GAMELOOPW),
                                          lambda: self.restart(),
                                          lambda: self.quit())

    def setPhasa(self, phasa):
        self.phasa = phasa
        if self.phasa == P_GAMELOOPW:
            self.scene = self.world
        if self.phasa == P_GAMEPAUSEW:
            self.scene = self.frame_pause_menu
            self.world.pause()

    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.setPhasa(P_GAMEPAUSEW)
            self.scene.update(event)

    def redraw(self):
        if self.phasa == P_GAMELOOPW:
            self.running = self.world.update()
        self.scene.draw(self.image)
        if not self.running:
            self.to_main_menu()

    def restart(self):
        self.setPhasa(P_GAMELOOPW)
        self.newGame(self.world.level, self.world.difficulty)

    def newGame(self, level, diff=NORMAL):
        self.world.new_game(level=level, difficulty=diff)
        self.setPhasa(P_GAMELOOPW)
        self.running = True

    def quit(self):
        self.world.save_data()
        self.running = False


from UI.Button import *


class GamePause(Frame):
    def __init__(self, size, window_rect, func_back, func_restart, func_menu):
        bg = get_texture_size(WHITE, size=size)
        super().__init__(pygame.Rect((0, 0), size), bg=bg)
        self.set_pos_center(window_rect)

        but_size = self.proc_size((0.6, 0.2))
        but_surf_back = createImageButton(but_size, "Back"), createImageButton(but_size, "Back", bg=GRAY)
        but_surf_restart = createImageButton(but_size, "Restart"), createImageButton(but_size, "Restart", bg=GRAY)
        but_surf_menu = createImageButton(but_size, "Menu"), createImageButton(but_size, "Menu", bg=GRAY)
        buts = createVSteckButtons(but_size, self.rect.w // 2, 20, 20,
                                   [but_surf_back, but_surf_restart, but_surf_menu],
                                   [func_back, func_restart, func_menu])
        self.add_frames(buts)
