import pygame


class Frame:
    def __init__(self, name, area):
        self.name = name
        self.area = area

        """
        This list will be containing all the elements that user will add in the frame
        """
        self.elements = []

    def addElement(self, element):
        pass

    def show(self):
        pass
