import pygame
import cv2
import numpy

class Frame:
    def __init__(self, surface, name, area, backgroundColor=None, partition=None, borderRadius=None):
        self.name = name
        self.x, self.y, self.width, self.height = area
        self.areaUnit = self.height / 100
        self.borderRadius = borderRadius
        self.surface = surface

        """
        data structure of partition will be in percentage.
        structure: ((area in percentage), color), (area in percentage), color))
        note: partition will work to define diffrent area with diffrent color, and it will be in the vertical way.
        """
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
        for attribute in attributes:
            if attribute not in self.defaultAttributes:
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
                area, color = partition
                if totalArea >= area:
                    totalArea -= area
                    height = (self.areaUnit*area)
                    self.partitions.append(((self.x, Current_y, self.width, height), color))
                    Current_y += height
                else:
                    print(f'There is not enough space create partition, Partition Info:{(area, color)}')
                    break
            self.totalPartitions = len(self.partitions)


    def show(self):
        if self.backgroundColor is not None:
            if self.partitions is None:
                if self.borderRadius is not None:
                    pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height),
                                     border_top_left_radius=self.borderRadius[0], border_top_right_radius=self.borderRadius[0],
                                     border_bottom_right_radius=self.borderRadius[0], border_bottom_left_radius=self.borderRadius[0])
                else:
                    pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height))
            else:
                counter = 0
                while counter < self.totalPartitions:
                    area, color = self.partitions[counter]
                    if self.borderRadius is not None:
                        if counter == 0:
                            pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height),
                                             border_top_left_radius=self.borderRadius[0],
                                             border_top_right_radius=self.borderRadius[0])
                        elif counter == self.totalPartitions - 1:
                            pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height),
                                             border_bottom_right_radius=self.borderRadius[0],
                                             border_bottom_left_radius=self.borderRadius[0])
                        else:
                            pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height))


    def showElement(self):
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

    def activeMirrorEffact(self):
        self.mirrorEffect = True

    def deactiveMirrorEffact(self):
        self.mirrorEffect = False

    def activeFrameResizer(self, width=600, height=600, aspectRatio=False):
        self.FrameResizer = True
        self.width = width
        self.height = height
        if aspectRatio:
            self.maintainAspectRatio()

    def deactiveFrameResizer(self):
        self.FrameResizer = False

    def open(self):
        try:
            self.VideoReader = cv2.VideoCapture(self.video)
            self.VideoReader.setExceptionMode(False)
        except:
            self.FileOpend = False
            return False
        self.FileOpend = True

    def close(self):
        self.VideoReader.release()
        self.FileOpend = False

    def show(self):
        if self.FileOpend:
            flag, frame = self.VideoReader.read()
            if flag:
                if not self.mirrorEffect:
                    frame = cv2.flip(frame, 1)

                if self.FrameResizer:
                    frame = cv2.resize(frame, (self.width, self.height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = numpy.rot90(frame)
                frame = pygame.surfarray.make_surface(frame)
                self.surface.blit(frame, (self.x, self.y))
            else:
                self.close()
                if self.playInLoop:
                    self.open()



