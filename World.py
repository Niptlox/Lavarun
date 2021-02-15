import pygame
import Texture
from UI.Frame import *
from math import ceil  # округление в большую сторону

TILE_SIZE = 32
TILE_SIZEL = (TILE_SIZE, TILE_SIZE)
CHUNK_SIZE = 16

N_DIRT = 1
path_tile = r"data\sprites\tiles\ "
tiles_frames = {
    N_DIRT: get_texture_size(path_tile + "dirt.png", size=TILE_SIZEL)
}

PLAYER_RECT = pygame.Rect(((0,0),(TILE_SIZE, TILE_SIZE * 2)))
path_player = r"data\sprites\player\ "
player_frames = {
    "idle": load_animation(path_player + r"idle\idle", [10, 5], size=PLAYER_RECT.size),
    "run": load_animation(path_player + r"idle\run", [5, 5, 5], size=PLAYER_RECT.size)
}


def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

class EntityStatic(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, animation: dict, animation_action="idle"):
        self.rect = rect
        self.animation = animation
        self.animation_action = animation_action
        self.start_animation_action = animation_action
        self.num_frame = 0

    def draw(self, screen, xy=None):
        """Если xy is None, то используется записане в спрайт координаты иначе xy"""
        if xy is None:
            xy = self.rect
        screen.blit(self.image, xy)

    def new_tick(self, timeTick=None):
        self.image = self.animation[self.animation_action][self.num_frame]
        self.num_frame = (self.num_frame + 1) % len(self.animation[self.animation_action])

    def get_display_xy(self, scroll):
        return self.rect.x - scroll[0], self.rect.y - scroll[1]

    def change_action(self, animation_action):
        self.animation_action = animation_action
        self.num_frame = 0

    def new_game(self):
        self.change_action(self.start_animation_action)

    def update(self, *args):
        if args:
            pass
        else:
            self.new_tick()


class Entity(EntityStatic):
    def __init__(self, rect: pygame.Rect, animation: dict, animation_action="idle"):
        super().__init__(rect, animation, animation_action)


class Player(Entity):
    def __init__(self, xy):
        rect = PLAYER_RECT.move(*xy) # is copy rect
        super().__init__(rect, player_frames, "idle")

    def new_game(self):
        super().new_game()
        self.moving_right = False
        self.moving_left = False
        self.air_timer = 0
        self.vertical_momentum = 0
        self.player_flip = 0

    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.moving_right = True
                if event.key == pygame.K_LEFT:
                    self.moving_left = True
                if event.key == pygame.K_UP:
                    if self.air_timer < 6:
                        self.vertical_momentum = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
        else:
            self.new_tick(**kwargs)

    def new_tick(self, timeTick=None, tile_rects=[]):
        player_movement = [0, 0]
        if self.moving_right == True:
            player_movement[0] += 2
        if self.moving_left == True:
            player_movement[0] -= 2
        player_movement[1] += self.vertical_momentum
        self.vertical_momentum += 0.2
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

        if player_movement[0] == 0:
            self.change_action('idle')
        if player_movement[0] > 0:
            self.change_action('run')
            self.player_flip = False
        if player_movement[0] < 0:
            self.change_action('run')
            self.player_flip = True

        ox, oy = self.rect.x, self.rect.y
        self.rect, collisions = self.move(self.rect, player_movement)
        true_movement = [self.rect.x - ox, self.rect.y - oy]
        if collisions['bottom'] == True:
            self.air_timer = 0
            self.vertical_momentum = 0
        else:
            self.air_timer += 1

        super().new_tick()
        return true_movement

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        rect.x += movement[0]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True
        rect.y += movement[1]
        hit_list = collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types, ()

class World:
    def __init__(self, level=-1, game_map={}, display_size=(720, 480)):
        self.game_map = game_map
        self.level = level
        self.display_size = display_size
        self.display = pygame.Surface(display_size)

        ss = CHUNK_SIZE * TILE_SIZE
        self.display_chanks_size = (ceil((display_size[0]) / ss + 1), ceil((display_size[1]) / ss + 1))

        self.scroll = [0, 0]

        self.tile_rects = []  # для отображения физики
        self.tiles = []  # для отображения на экран
        self.entitys = []  # для взаимодействий

        self.player = None

    def get_chunk(self, xy):
        if xy not in self.game_map:
            if self.level < 0:
                self.game_map[xy] = self.generation_chunk(self, xy, level=self.level)
            else:
                return
        return self.game_map[xy]

    def generation_chunk(self, xy, level=-1):
        x, y = xy
        chunk_data = []
        i = 0
        m_a_g = [None] * CHUNK_SIZE
        for y_pos in range(CHUNK_SIZE - 1, -1, -1):
            for x_pos in range(CHUNK_SIZE):
                target_x = x * CHUNK_SIZE + x_pos
                target_y = y * CHUNK_SIZE + y_pos
                tile_type = 0  # nothing
                if target_y > 10:
                    tile_type = 2  # dirt
                if tile_type != 0:
                    chunk_data.append([[target_x, target_y], tile_type])
                i += 1
        return chunk_data

    def new_game(self, game_map=None, level=None):
        self.game_map = game_map if game_map is not None else self.game_map
        self.level = level if level is not None else self.level
        self.scroll = [0, 0]
        self.player = Player((self.display_size[0] // 2, self.display_size[1] // 2))


    def update(self):
        # Скользящие перемещение камеры
        self.scroll[0] += (self.Player.rect.x - self.scroll[0] - self.display_size[0] // 2) / 20
        self.scroll[1] += (self.Player.rect.y - self.scroll[1] - self.display_size[1] // 2) / 20

        scroll = [int(self.scroll[0]), int(self.scroll[1])]
        # Обновление, нахождение, всех спрайтов на экране
        self.tile_rects, self.tiles, self.entitys = self.update_display(scroll, self.display_size)
        # Обновление игрока, движение и тд
        self.player.update(tile_rects=self.tile_rects)

    def redraw(self, surface):
        self.display.fill((246, 144, 255))
        for tile in self.tiles:
            xy_tile = (tile[0][0] * TILE_SIZE, tile[0][1] * TILE_SIZE)
            type_tile = tile[1]
            self.display.blit(tiles_frames[type_tile], xy_tile)
        scroll = [int(self.scroll[0]), int(self.scroll[1])]
        self.player.draw(self.display, (self.player.rect.x - scroll[0], self.player.y - scroll[1]))
        surface.blit( pygame.transform.scale(self.display, surface.rect.size))

    def get_event(self, event):
        self.player.update(event)

    def update_display(self, scroll, display_size):
        self.tile_rects = tile_rects = []  # для отображения физики
        self.tiles = tiles = []  # для отображения на экран
        self.entitys = entitys = []  # для взаимодействий
        display_rect_for_tiles = (scroll[0] // TILE_SIZE, scroll[1] // TILE_SIZE), (
            (display_size[0] + scroll[0] - 1) // TILE_SIZE, (display_size[1] + scroll[1] - 1) // TILE_SIZE)
        for y in range(self.display_chanks_size[1]):
            for x in range(self.display_chanks_size[0]):
                target_x = x - 1 + int(round(scroll[0] / (CHUNK_SIZE * TILE_SIZE)))
                target_y = y - 1 + int(round(scroll[1] / (CHUNK_SIZE * TILE_SIZE)))
                target_chunk = (target_x, target_y)
                chank = self.get_chunk(target_chunk)
                for tile in chank:
                    tile_xy = tile[0]
                    if not (display_rect_for_tiles[0][0] <= tile_xy[0] <= display_rect_for_tiles[0][1] and
                            display_rect_for_tiles[1][0] <= tile_xy[1] <= display_rect_for_tiles[1][1]):
                        # за экраном
                        continue
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
        return  tile_rects, tiles, entitys


class GameFrame(Frame):
    def __init__(self, rect, world):
        super().__init__(rect, bg=world.background)
        self.world = world

    def update(self, args):
        if args:
            self.world.get_event(args)
        else:
            self.world.update()

    def redraw(self):
        self.world.redraw(self.image)
