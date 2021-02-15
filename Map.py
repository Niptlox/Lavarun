from UI.Button import *





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
