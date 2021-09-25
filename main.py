from pygamelib import *

pygame.init()
windowWidth = 1200
windowHeight = 600
window = pygame.display.set_mode((windowWidth, windowHeight))


def closeApplication():
    exit()


def MianMenu():
    run = True
    # just Testing.
    frame_1 = Frame(window, 'frame', (100, 100, 300, 400), (25, 27, 125), borderRadius=(10, 10, 10, 10),
                    partition={70:(67, 55, 100), 30:(150, 175, 155)})
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeApplication()

        window.fill((255, 255, 255))
        frame_1.show()
        pygame.display.update()

MianMenu()

