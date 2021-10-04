import pygame
import cv2
import numpy
import os


# Common Functions
def openCVFrameToPygameSurface(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = numpy.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame


def extractFramesFromVideo(video, output_dir="", frameCount=None, mirror_effect=False, counterStartPoint=0,
                           skipFrame=0):
    video = cv2.VideoCapture(video)
    counter = counterStartPoint
    frameCounter = 0
    converting = True
    while converting:
        flag, frame = video.read()
        if flag:
            if skipFrame > 0:
                skipFrame -= 1
                continue
            if not mirror_effect:
                frame = cv2.flip(frame, 1)
            cv2.imwrite(os.path.join(output_dir, str(counter)+".jpg"), frame)
            counter += 1
            if frameCount is not None:
                frameCounter += 1
                if not frameCounter < frameCount:
                    converting = False
        else:
            break

    video.release()


class Frame:
    def __init__(self, surface, name, area, backgroundColor=None, partition=None, borderRadius=None, outline=0):
        self.name = name
        self.x, self.y, self.width, self.height = area
        self.areaUnit = self.height / 100
        self.borderRadius = borderRadius
        self.surface = surface
        self.outline = outline

        """
        data structure of partition will be in percentage.
        structure: {'area': area_in_percentage, 'color': RGB_color, 'outline': Width_of_outline_in_pixel}
        note: partition will work to define different area with different color, and it will be in the vertical way.
        """
        self.partitions = None
        self.totalPartitions = 0
        self.rePartition(partition)
        self.backgroundColor = backgroundColor

        """
        this list is containing all the default attribute that should be available in Component.
        """
        self.defaultAttributes = ['show', 'x', 'y']

        """
        This list will be containing all the elements that user will add in the frame
        """
        self.elements = []

    def addComponents(self, element):
        # Here checking that all the default attributes is available in the give object or not.
        attributes = element.__dir__()
        for attribute in self.defaultAttributes:
            if attribute not in attributes:
                print(f"'{attribute}' is not available in the give object")
                return

        # defining the actual position of element according to the frame.
        element.x = self.x + element.x
        element.y = self.y + element.y

        # here adding the element in the list.
        self.elements.append(element)
        return True

    def rePartition(self, partitions):
        if partitions is None:
            self.partitions = None
        else:
            totalArea = 100
            Current_y = self.y
            self.partitions = []
            for partition in partitions:
                area = partition['area']
                if totalArea >= area:
                    totalArea -= area
                    height = (self.areaUnit*area)
                    partition['area'] = (self.x, Current_y, self.width, height)
                    self.partitions.append(partition)
                    Current_y += height
                else:
                    print(f'There is not enough space create partition, Partition Info:{partition}')
                    break
            self.totalPartitions = len(self.partitions)

    def show(self):
        if self.backgroundColor is not None and self.partitions is not None:
            if self.borderRadius is not None:
                pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height),
                                 width=self.outline,
                                 border_top_left_radius=self.borderRadius[0],
                                 border_top_right_radius=self.borderRadius[1],
                                 border_bottom_right_radius=self.borderRadius[2],
                                 border_bottom_left_radius=self.borderRadius[3])
            else:
                pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height),
                                 width=self.outline)
        elif self.partitions is not None:
            counter = 0
            while counter < self.totalPartitions:
                partition = self.partitions[counter]
                area = partition['area']
                if 'color' in partition:
                    color = partition["color"]
                else:
                    if self.backgroundColor is not None:
                        color = self.backgroundColor
                    else:
                        color = (60, 63, 65)
                if 'outline' in partition:
                    outline = partition['outline']
                else:
                    outline = self.outline
                if self.borderRadius is not None:
                    if counter == 0:
                        pygame.draw.rect(self.surface, color, area, width=outline,
                                         border_top_left_radius=self.borderRadius[0],
                                         border_top_right_radius=self.borderRadius[1])
                    elif counter == self.totalPartitions - 1:
                        pygame.draw.rect(self.surface, color, area, width=outline,
                                         border_bottom_right_radius=self.borderRadius[2],
                                         border_bottom_left_radius=self.borderRadius[3])
                    else:
                        pygame.draw.rect(self.surface, color, area, width=outline)
                else:
                    pygame.draw.rect(self.surface, color, area, width=self.outline)
                counter += 1
            self.showElements()

    def showElements(self):
        for element in self.elements:
            element.show()
            

class VideoPlayer:
    def __init__(self, surface, x, y, video, play_in_loop=False, mirror_effect=False):
        self.video = video
        self.surface = surface
        self.VideoReader = None
        self.FileOpened = False
        self.x = x
        self.y = y
        self.playInLoop = play_in_loop
        self.open()
        self.FrameResizer = False
        self.mirrorEffect = mirror_effect
        self.height = None
        self.width = None
        self.frameCrop = None

    def maintainAspectRatio(self):
        video = cv2.VideoCapture(self.video)
        flag, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = numpy.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        height = frame.get_height()
        width = frame.get_width()
        self.height = int((self.width * (height/width)))
        video.release()

    def activeFrameCropper(self, area):
        """
        :param area: (x, y, width, height)
        :return: None
        """
        self.frameCrop = area

    def deactivateFrameCropper(self):
        self.frameCrop = None

    def activeMirrorEffect(self):
        self.mirrorEffect = True

    def deactivateMirrorEffect(self):
        self.mirrorEffect = False

    def activeFrameResizer(self, width=600, height=600, aspectRatio=False):
        self.FrameResizer = True
        self.width = width
        self.height = height
        if aspectRatio:
            self.maintainAspectRatio()

    def deactivateFrameResizer(self):
        self.FrameResizer = False

    def open(self):
        try:
            self.VideoReader = cv2.VideoCapture(self.video)
        except:
            self.FileOpened = False
            return False
        self.FileOpened = True

    def close(self):
        self.VideoReader.release()
        self.FileOpened = False

    def show(self):
        if self.FileOpened:
            repeat = True
            while repeat:
                flag, frame = self.VideoReader.read()
                if flag:
                    if not self.mirrorEffect:
                        frame = cv2.flip(frame, 1)

                    if self.FrameResizer:
                        frame = cv2.resize(frame, (self.width, self.height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                    if self.frameCrop is not None:
                        x, y, width, height = self.frameCrop
                        frame = frame[y:y+height, x:x+width]  # frame[y:y+height, x:x+width]
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = numpy.rot90(frame)
                    frame = pygame.surfarray.make_surface(frame)
                    self.surface.blit(frame, (self.x, self.y))
                    repeat = False
                else:
                    self.close()
                    if self.playInLoop:
                        self.open()
