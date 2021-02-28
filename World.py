import pygame
from UI.Window import STATIC_SIZE
from Texture import *
from Entities import *
from Chunk import *
from DataLoader import *
from UI.Frame import *
from math import ceil  # округление в большую сторону
import pickle

HARD = 3
NORMAL = 2
EASY = 1


class World:
    COF_CAMERA_FRICTION = 0.1  # коэффициент для скольжения камеры

    def __init__(self, display_size=STATIC_SIZE, clock=None):
        self.clock = clock
        self.game_map = {}
        # при level < 0  авто генерация, иначе из файла
        self.level = -1
        self.difficulty = None
        self.display_size = display_size
        self.display = pygame.Surface(display_size)
        self.GAME_BACKGROUND = pygame.transform.scale(load_image('data/sprites/gamebg.png'), self.display_size)

        ss = CHUNK_SIZE * TILE_SIZE
        self.display_chanks_size = (ceil((display_size[0]) / ss + 2), ceil((display_size[1]) / ss + 2))

        self.scroll = [0, 0]

        self.tile_rects = []  # для отображения физики
        self.tiles = []  # для отображения на экран
        self.entitys = []  # для взаимодействий
        self.player = Player((0, 0), self)

    # получить новый чанк
    def get_chunk(self, xy):
        if xy not in self.game_map:
            if self.level < 0:
                self.game_map[xy] = self.generation_chunk(xy, self.level)
            else:
                return
        return self.game_map[xy]

    # генерация нового чанка
    def generation_chunk(self, xy, level=-1):
        chunk_data = generation_chunk(xy, level)
        return chunk_data

    # перезапись переменных для начала новой игры
    def new_game(self, game_map=None, level=None, difficulty=None):
        self.game_map = game_map if game_map is not None else self.game_map
        self.level = level if level is not None else self.level
        if difficulty is not None:
            self.set_difficulty(difficulty)
        self.player.new_game()
        self.player.set_xy((self.display_size[0] // 2, self.display_size[1] // 2))
        self.scroll = [0, 0]

    def set_difficulty(self, diff):  # установка сложности
        self.difficulty = diff
        player = self.player
        cof = 0.5
        if diff == EASY:
            player.max_oxygen = 5000 * cof  # кислород
            player.oxygen_normal_spending = 1  # трата кислорода в нормальных условиях
            player.oxygen_jump_spending = 20  # трата кислорода в прыжке
            player.score_coff = 1  # множитель для очков
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

    # обновление экраны и игрока
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
        if not self.player.alive or self.player.win is not None:
            self.save_data()
            return False

        return True

    def redraw(self):  # обновление дисплея
        # self.display.fill((146, 144, 255))
        self.display = vertical_gradient(self.display_size, (0, 0, 0, 250), (5, 5, 37, 200))
        # self.display = self.GAME_BACKGROUND.copy()
        for tile in self.tiles:
            xy_tile = (tile[0][0] * TILE_SIZE - self.scroll[0], tile[0][1] * TILE_SIZE - self.scroll[1])
            type_tile = tile[1]
            self.display.blit(tiles_frames[type_tile], xy_tile)
        scroll = [int(self.scroll[0]), int(self.scroll[1])]
        self.player.draw(self.display, (self.player.rect.x - scroll[0], self.player.rect.y - scroll[1]))
        self.display.blit(self.player.surface_oxygen_bar, (20, 20))
        self.display.blit(self.player.surface_score, (self.display_size[0] - 120, 20))


    def del_obj(self, xy_tile, i_tile):
        xy_chank = xy_tile[0] // CHUNK_SIZE_DIS, xy_tile[1] // CHUNK_SIZE_DIS
        # print("del_obj", xy_chank, xy_tile, i_tile)
        self.game_map[xy_chank][i_tile] = None

    def replace_obj(self, tile_type, xy_tile, i_tile):  # замена обьекта
        xy_chank = xy_tile[0] // CHUNK_SIZE_DIS, xy_tile[1] // CHUNK_SIZE_DIS
        tile = self.game_map[xy_chank][i_tile]
        self.game_map[xy_chank][i_tile] = (tile[0], tile_type)

    def draw(self, surface):
        self.redraw()
        surface.blit(pygame.transform.scale(self.display, surface.get_size()), (0, 0))

    # получение события из pygame
    def get_event(self, event):
        self.player.update(event)

    # ОБНОВЛЕНИЕ прямоугольников и объектов на дисплее,
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
                i_tile = 0
                for tile in chank:
                    if tile is None:
                        i_tile += 1
                        continue
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
                    if 101 <= abs(tile[1]) < 200:
                        # может твердые а может и нет, обекты для взаимного действия, допустим человечки
                        rect = pygame.Rect(tile_xy[0] * TILE_SIZE, tile_xy[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        entitys.append((rect, tile[1], i_tile))
                    i_tile += 1
        return tile_rects, tiles, entitys

    # сохранение данных игры
    def save_data(self):
        max_score = max(get_max_score(), self.get_score())
        put_max_score(max_score)

    def pause(self):
        self.player.moving_right = False
        self.player.moving_left = False

    def get_score(self):
        return self.player.score


P_GAMELOOPW = 1
P_GAMEPAUSEW = 2
P_GAMEFINISHW = 3
P_GAMESPACESHIPW = 4


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
        self.frame_spaceship_menu = GameSpaceship(self.proc_size((0.3, 0.5)), self.rect,
                                          lambda: self.setPhasa(P_GAMELOOPW),
                                          lambda: self.restart(),
                                          lambda: self.quit())
        self.frame_finish_menu = GameFinish(self.proc_size((0.3, 0.5)), self.rect,
                                            lambda: self.restart(),
                                            lambda: self.quit())

    def setPhasa(self, phasa):
        self.phasa = phasa
        if self.phasa == P_GAMELOOPW:
            self.scene = self.world
        if self.phasa == P_GAMEPAUSEW:
            self.scene = self.frame_pause_menu
            self.world.pause()
        if self.phasa == P_GAMEFINISHW:
            self.scene = self.frame_finish_menu
            self.frame_finish_menu.set_score(self.world.get_score())
        if self.phasa == P_GAMESPACESHIPW:
            self.scene = self.frame_spaceship_menu
            self.frame_spaceship_menu.set_score(self.world.get_score())
            self.world.player.set_win(None)

    def update(self, *args):
        if args:
            event = args[0]
            if self.phasa == P_GAMELOOPW:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.setPhasa(P_GAMEPAUSEW)
                        return
            self.scene.update(event)

    def redraw(self):
        if self.phasa == P_GAMELOOPW:
            running = self.world.update()
            if not running:
                if not self.world.player.alive:
                    self.setPhasa(P_GAMEFINISHW)
                elif self.world.player.win:
                    self.setPhasa(P_GAMESPACESHIPW)
        self.scene.draw(self.image)
        if not self.running:
            self.to_main_menu()

    def restart(self):
        self.setPhasa(P_GAMELOOPW)
        self.world.clear_map()
        self.newGame(self.world.level, self.world.difficulty)

    def newGame(self, level, diff=NORMAL):
        self.world.new_game(level=level, difficulty=diff)
        self.setPhasa(P_GAMELOOPW)
        self.running = True

    def quit(self):  # выход
        self.world.save_data()
        self.running = False


from UI.Button import *
from UI.Text import *


class GamePause(Frame):  # меню паузы
    def __init__(self, size, window_rect, func_back, func_restart, func_menu):
        bg = get_texture_size(WHITE, size=size)
        super().__init__(pygame.Rect((0, 0), size), bg=bg)
        self.set_pos_center(window_rect)
        self.func_back = func_back
        but_size = self.proc_size((0.6, 0.2))
        but_surf_back = createImageButton(but_size, "Back"), createImageButton(but_size, "Back", bg=GRAY, font=TEXTFONT_BTN)  # кнопки
        but_surf_restart = createImageButton(but_size, "Restart"), createImageButton(but_size, "Restart", bg=GRAY, font=TEXTFONT_BTN)
        but_surf_menu = createImageButton(but_size, "Menu"), createImageButton(but_size, "Menu", bg=GRAY, font=TEXTFONT_BTN)
        buts = createVSteckButtons(but_size, self.rect.w // 2, 20, 20,
                                   [but_surf_back, but_surf_restart, but_surf_menu],
                                   [func_back, func_restart, func_menu])
        self.add_frames(buts)

    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # print("event", event)
                pass
                self.func_back()
            super().update(*args)



class GameSpaceship(Frame):
    def __init__(self, size, window_rect, func_back, func_restart, func_menu):
        bg = get_texture_size(WHITE, size=size)
        super().__init__(pygame.Rect((0, 0), size), bg=bg)
        self.set_pos_center(window_rect)
        self.func_back = func_back
        frame_size = self.proc_size((0.6, 0.2))
        xy = [self.rect.w // 2 - frame_size[0] // 2, 20]

        but_size = self.proc_size((0.6, 0.1))
        frame_t = Label((xy, (frame_size[0], 35)), text="YOU WIN")  # , bg=WHITE, text_color=BLACK)
        self.add_frame(frame_t)
        xy[1] += frame_size[1] + 5
        self.frame_score = Label((xy, (frame_size[0], 35)), text="0")  # , bg=WHITE, text_color=BLACK)
        self.add_frame(self.frame_score)
        xy[1] += frame_size[1] + 5
        xy[0] += frame_size[0] // 2
        but_surf_back = createImageButton(but_size, "Back"), createImageButton(but_size, "Back", bg=GRAY, font=TEXTFONT_BTN)
        but_surf_restart = createImageButton(but_size, "Restart"), createImageButton(but_size, "Restart", bg=GRAY, font=TEXTFONT_BTN)
        but_surf_menu = createImageButton(but_size, "Menu"), createImageButton(but_size, "Menu", bg=GRAY, font=TEXTFONT_BTN)
        buts = createVSteckButtons(but_size, xy[0], xy[1], 20,
                                   [but_surf_back, but_surf_restart, but_surf_menu],
                                   [func_back, func_restart, func_menu])
        self.add_frames(buts)


    def set_score(self, score):
        self.frame_score.setText("Score: " + str(score))


    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # print("event", event)
                pass
                self.func_back()
            super().update(*args)


class GameFinish(Frame):
    def __init__(self, size, window_rect, func_restart, func_menu):
        bg = get_texture_size(WHITE, size=size)
        super().__init__(pygame.Rect((0, 0), size), bg=bg)
        self.set_pos_center(window_rect)
        frame_size = self.proc_size((0.6, 0.2))
        step = 10
        xy = [(self.rect.w - frame_size[0]) // 2, step]
        # self.add_frame(Label((xy, frame_size), text="Score:", bg=WHITE, text_color=BLACK))
        # xy[1] += frame_size[1]
        self.frame_score = Label((xy, (frame_size[0], 35)), text="0")  # , bg=WHITE, text_color=BLACK)
        self.add_frame(self.frame_score)
        xy[1] += frame_size[1] + step
        but_surf_restart = createImageButton(frame_size, "Restart"), createImageButton(frame_size, "Restart", bg=GRAY)
        but_surf_menu = createImageButton(frame_size, "Menu"), createImageButton(frame_size, "Menu", bg=GRAY)
        buts = createVSteckButtons(frame_size, self.rect.w // 2, xy[1], 20,
                                   [but_surf_restart, but_surf_menu],
                                   [func_restart, func_menu])
        self.add_frames(buts)

    def set_score(self, score):
        self.frame_score.setText("Score: " + str(score))
