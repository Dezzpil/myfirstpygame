if __name__ == '__main__':
    import pygame

    pygame.init()

    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)

    for test in tests:
        while test.elapse():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            test.run(screen)
            screen.fill((0, 0, 0))
            pygame.display.flip()


