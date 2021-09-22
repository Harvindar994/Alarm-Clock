import pygame


class Frame:
    def __init__(self, name, area):
        self.name = name
        self.area = area

        """
        this list is containing all the default attribute that should be available in Component.
        """
        self.defaultAttributes = ['show', 'x', 'y']

        """
        This list will be containing all the elements that user will add in the frame
        """
        self.elements = []

    def addComponents(self, element):
        attributes = element.__dir__()

        if 'show' in attributes and 'x' in attributes and 'y' in attributes:


    def show(self):
        pass


