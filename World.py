import pygame

from Texture import *
from Tiles import *
from Entitys import *
from UI.Frame import *
from random import randint
from math import ceil  # округление в большую сторону

CHUNK_SIZE = 16


class World:
    COF_CAMERA_FRICTION = 0.1  # коофицент для скольжения камеры

    def __init__(self, level=-1, game_map={}, display_size=(720, 480)):
        self.game_map = game_map
        self.level = level
        self.display_size = display_size
        self.display = pygame.Surface(display_size)

        ss = CHUNK_SIZE * TILE_SIZE
        self.display_chanks_size = (ceil((display_size[0]) / ss + 2), ceil((display_size[1]) / ss + 2))

        self.scroll = [0, 0]

        self.tile_rects = []  # для отображения физики
        self.tiles = []  # для отображения на экран
        self.entitys = []  # для взаимодействий

        self.player = None

    def get_chunk(self, xy):
        if xy not in self.game_map:
            if self.level < 0:
                self.game_map[xy] = self.generation_chunk(xy, self.level)
            else:
                return
        return self.game_map[xy]

    def generation_chunk(self, xy, level=-1):
        x, y = xy
        chunk_data = []
        # if x + y == 0:
        #     return chunk_data
        i = 0
        m_a_g = [None] * CHUNK_SIZE
        # m_a_g_old = [None] * CHUNK_SIZE
        for y_pos in range(CHUNK_SIZE - 1, -1, -1):
            m_a_g_old = m_a_g
            m_a_g = [None] * CHUNK_SIZE
            for x_pos in range(CHUNK_SIZE):
                target_x = x * CHUNK_SIZE + x_pos
                target_y = y * CHUNK_SIZE + y_pos
                tile_type = 0  # nothing
                if target_y == 6 and randint(0, 2) == 1:
                    tile_type = N_DIRT
                if target_y == 3 and randint(0, 3) == 1:
                    tile_type = N_DIRT
                if target_y == 8 and randint(0, 7) == 1:
                    tile_type = N_SPIKE
                if target_y > 8:
                    tile_type = N_DIRT  # dirt
                if tile_type == 0:
                    if m_a_g_old[x_pos] == N_DIRT and randint(0, 5) == 1:
                        tile_type = N_SPIKE
                if tile_type != 0:
                    chunk_data.append([[target_x, target_y], tile_type])
                m_a_g[x_pos] = tile_type
                i += 1

        return chunk_data

    def new_game(self, game_map=None, level=None):
        self.game_map = game_map if game_map is not None else self.game_map
        self.level = level if level is not None else self.level
        self.scroll = [0, 0]
        self.player = Player((self.display_size[0] // 2 * 0, self.display_size[1] // 2))
        self.player.new_game()

    def clear_map(self):
        self.game_map = {}

    def update(self):
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
            return False
        return True

    def redraw(self, surface):
        self.display.fill((146, 144, 255))
        for tile in self.tiles:
            xy_tile = (tile[0][0] * TILE_SIZE - self.scroll[0], tile[0][1] * TILE_SIZE - self.scroll[1])
            type_tile = tile[1]
            self.display.blit(tiles_frames[type_tile], xy_tile)
        scroll = [int(self.scroll[0]), int(self.scroll[1])]
        self.player.draw(self.display, (self.player.rect.x - scroll[0], self.player.rect.y - scroll[1]))
        surface.blit(pygame.transform.scale(self.display, surface.get_size()), (0, 0))
        surface.blit(self.player.surface_oxygen_bar, (20, 20))

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


class GameFrame(Frame):
    def __init__(self, rect, world, to_main_menu=None):
        super().__init__(rect, bg=BLACK)
        self.world = world
        self.to_main_menu = to_main_menu

    def update(self, args):
        self.world.get_event(args)

    def redraw(self):
        running = self.world.update()
        self.world.redraw(self.image)
        if not running:
            self.to_main_menu()

    def newGame(self, level):
        self.world.new_game(level=level)
