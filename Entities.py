import pygame
from Texture import *
from Tiles import *

PLAYER_RECT = pygame.Rect(((0, 0), (TILE_SIZE * 0.85, TILE_SIZE * 2 * 0.95)))
path_player = r"data\sprites\player\\"
colorkeyI = load_image(path_player + r"idle\idle_0.png").get_at((0, 0))
s = 4
player_frames = {

    "run": load_animation(path_player + r"run\jonny_walk", [s, s, s, s], size=PLAYER_RECT.size),
    "idle": load_animation(path_player + r"idle\idle", [20, 5], size=PLAYER_RECT.size, colorkey=colorkeyI)
}


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def collision_test_entitys(rect, entitys):
    hit_list = []
    for tile_rect, tile_type in entitys:
        if rect.colliderect(tile_rect):
            hit_list.append((tile_rect, tile_type))
    return hit_list


class EntityStatic(pygame.sprite.Sprite):
    def __init__(self, rect: pygame.Rect, animation: dict, animation_action="idle"):
        self.rect = rect
        self.animation = animation
        self.animation_action = None
        self.start_animation_action = animation_action
        self.num_frame = 0
        self.image = None
        self.change_action(animation_action)

    def draw(self, screen, xy=None):
        """Если xy is None, то используется записане в спрайт координаты иначе xy"""
        if xy is None:
            xy = self.rect
        screen.blit(self.image, xy)

    def new_tick(self, timeTick=None):
        self.image = self.animation[self.animation_action][self.num_frame]
        self.num_frame = (self.num_frame + 1) % len(self.animation[self.animation_action])
        print("num_frame", self.num_frame)

    def get_display_xy(self, scroll):
        return self.rect.x - scroll[0], self.rect.y - scroll[1]

    def change_action(self, animation_action):
        if animation_action != self.animation_action:
            self.animation_action = animation_action
            self.num_frame = 0
            self.image = self.animation[self.animation_action][self.num_frame]

    def new_game(self):
        self.change_action(self.start_animation_action)

    def update(self, *args):
        if args:
            pass
        else:
            self.new_tick()

    def set_xy(self, xy):
        self.rect.x, self.rect.y = xy


class Entity(EntityStatic):
    def __init__(self, rect: pygame.Rect, animation: dict, animation_action="idle"):
        super().__init__(rect, animation, animation_action)


class Player(Entity):
    def __init__(self, xy):
        rect = PLAYER_RECT.move(*xy)  # is copy rect
        super().__init__(rect, player_frames, "idle")
        self.jump_speed = 9 / STATIC_TILE_SIZE * TILE_SIZE  # скорость при старте прыжка
        self.speed = 4 / STATIC_TILE_SIZE * TILE_SIZE  # скорость хождения
        self.gravity = 0.4 / STATIC_TILE_SIZE * TILE_SIZE  # скорость падения
        self.alive = True
        self.max_oxygen = 5000
        self.oxygen = self.max_oxygen
        self.oxygen_normal_spending = 1
        self.oxygen_jump_spending = 20
        self.oxygen_jump_speed = 8 / STATIC_TILE_SIZE * TILE_SIZE
        self.surface_oxygen_bar = pygame.Surface((200, 30))
        self.surface_score = pygame.Surface((90, 20))
        self.score = 0
        self.min_y = -155

    def new_game(self):
        super().new_game()
        self.moving_right = False
        self.moving_left = False
        self.tap_oxygen_jump = False
        self.double_jump = False
        self.air_timer = 0
        self.vertical_momentum = 0
        self.player_flip = 0
        self.oxygen = self.max_oxygen
        self.score = 0
        self.alive = True



    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            self.tap_oxygen_jump = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moving_right = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    #self.moving_left = True
                    pass
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    # прыжок от земли
                    if self.air_timer < 6:
                        self.vertical_momentum = -self.jump_speed
                    # elif not self.double_jump:
                    #     self.vertical_momentum = -self.jump_speed
                    #     self.double_jump = True

                if event.key == pygame.K_SPACE:
                    # прыжок на кислороде
                    print("self.vertical_momentum", self.vertical_momentum)
                    if self.vertical_momentum > -self.oxygen_jump_speed // 2:
                        self.vertical_momentum -= self.oxygen_jump_speed
                        self.oxygen -= self.oxygen_jump_spending
                    # self.tap_oxygen_jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.moving_right = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.moving_left = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    self.tap_oxygen_jump = False
        else:
            self.new_tick(**kwargs)

    def new_tick(self, timeTick=None, tile_rects=[], entitys=[]):
        # if self.tap_oxygen_jump and self.vertical_momentum > -self.oxygen_jump_speed:
        #     self.vertical_momentum -= self.oxygen_jump_speed
        #     self.oxygen -= self.oxygen_jump_spending
        player_movement = [0, 0]
        if self.moving_right == True:
            player_movement[0] += self.speed
        if self.moving_left == True:
            player_movement[0] -= self.speed
        player_movement[1] += self.vertical_momentum
        self.vertical_momentum += self.gravity
        max_gravity = self.gravity * 15
        if self.vertical_momentum > max_gravity:
            self.vertical_momentum = max_gravity

        if player_movement[0] == 0:
            self.change_action('idle')
        if player_movement[0] > 0:
            self.change_action('run')
            self.player_flip = False
        if player_movement[0] < 0:
            self.change_action('run')
            self.player_flip = True

        ox, oy = self.rect.x, self.rect.y
        self.rect, collisions = self.move(self.rect, player_movement, tile_rects)
        true_movement = [self.rect.x - ox, self.rect.y - oy]
        if collisions['bottom'] == True:
            self.air_timer = 0
            self.vertical_momentum = 0
            self.double_jump = False
        else:
            self.air_timer += 1
        if collisions["top"] == True:
            self.vertical_momentum = 0
        self.oxygen -= self.oxygen_normal_spending
        hit_list = collision_test_entitys(self.rect, entitys)
        for entity in hit_list:
            if entity[1] in (N_SPIKE, N_LAVA):
                self.damage(1)
        if self.oxygen < 0:
            self.damage(1)
        self.score = self.rect.x // 100
        # print("PlayerRect", (self.rect.x, self.rect.y), (self.rect.x // TILE_SIZE, self.rect.y // TILE_SIZE))
        self.update_image()
        return true_movement

    def damage(self, hp_damage=1):
        self.alive = False

    def update_image(self):
        player_img = self.animation[self.animation_action][self.num_frame]
        self.image = pygame.transform.flip(player_img, self.player_flip, False)
        if self.air_timer < 6:
            self.num_frame = (self.num_frame + 1) % len(self.animation[self.animation_action])
        else:
            self.num_frame = 0
        self.surface_oxygen_bar.fill((50, 50, 100))
        wbord = 2
        w, h = self.surface_oxygen_bar.get_size()
        pygame.draw.rect(self.surface_oxygen_bar, (50, 200, 250),
                         (wbord, wbord, int((w - 2 * wbord) * self.oxygen / self.max_oxygen), h - 2 * wbord))
        pygame.draw.rect(self.surface_oxygen_bar, (110, 0, 50), (0, 0, w, h), wbord)

        textScore = TEXTFONT.render(str(self.score), False,
                          (180, 180, 0))
        self.surface_score.fill((22, 22, 22))
        self.surface_score.blit(textScore, (2, 0))
        print("self.oxygen", self.oxygen)
        # print("num_frame", self.num_frame)

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
            print(self.rect.y, self.min_y)
        if self.rect.y < self.min_y:
            self.rect.y = self.min_y
            self.vertical_momentum = -self.vertical_momentum
            collision_types['top'] = True
        return rect, collision_types
