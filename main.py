from pygamelib import *

pygame.init()
windowWidth = 1280
windowHeight = 720
window = pygame.display.set_mode((windowWidth, windowHeight))


def closeApplication():
    exit()


def MianMenu():
    run = True
    # just Testing.
    MainFrame = Frame(window, 'frame', (0, 0, 1280, 720),
                    partition=[{'area': 90, 'color': (0, 0, 255), 'outline': 0},
                               {'area': 10, 'color': (150, 175, 155), 'outline': 0}])
    video = VideoPlayer(window, 0, 0, 0)

                               {'area': 10, 'color': (56, 67, 73), 'outline': 0}])
    video = VideoPlayer(window, 0, 0, 'video.mov', True)
    video.activeFrameCropper((0, 0, 1280, 648))
    video.activeFrameResizer(1280, aspectRatio=True)

    MainFrame.addComponents(video)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeApplication()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)

        window.fill((255, 255, 255))
        MainFrame.show()
        pygame.display.update()

MianMenu()

