import pygame
from Texture import *
from Button import *

pygame.init()


class StartMenu(pygame.sprite.Sprite):
    background = get_texture(r"data\sprites\bgStart.png")
    def __init__(self, size, funcStart):
        super().__init__()
        self.rect = pygame.Rect((0, 0), size)
        self.image = pygame.Surface(self.rect.size)
        self.background = StartMenu.background
        imgB_up, imgB_in, imgB_down = openImagesButton(r"data\sprites\buttons\StartBut.png")
        self.butStart = Button((100, 120),  imgB_up, imgB_in, imgB_down, lambda: print("START"), size=(170, 40))
        self.butStart2 = Button((100, 190), imgB_up, imgB_in, imgB_down, lambda: print("START2"), size=(170, 40))
        self.groupBts = pygame.sprite.LayeredUpdates((self.butStart, self.butStart2))

    def update(self, *args):
        if args:
            event = args[0]
            self.groupBts.update(event)

    def draw(self, screen):
        if self.background.get_size != self.rect.size:
            self.background = pygame.transform.scale(StartMenu.background, self.rect.size)

        self.image.blit(self.background, (0, 0))
        self.groupBts.draw(self.image)
        screen.blit(self.image, self.rect)



# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

def main():
    size = (1200, 700)
    screen = pygame.display.set_mode(size)
    startMenu = StartMenu(size, lambda: print("START"))
    # group = pygame.sprite.LayeredUpdates((but))
    fps = 30
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            startMenu.update(event)

        screen.fill((0, 0, 0))
        startMenu.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
