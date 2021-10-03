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
    frame_1 = Frame(window, 'frame', (600, 100, 300, 400), borderRadius=(10, 10, 10, 10),
                    partition=[{'area': 90, 'color': (0, 0, 255), 'outline': 0},
                               {'area': 10, 'color': (150, 175, 155), 'outline': 0}])
    video = VideoPlayer(window, 0, 0, 0)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeApplication()

        window.fill((255, 255, 255))

        video.show()
        frame_1.show()
        pygame.display.update()

MianMenu()

