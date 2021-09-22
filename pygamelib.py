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
        # Here checking that all the default attributes is available in the give object or not.
        attributes = element.__dir__()
        for attribute in attributes:
            if attribute not in self.defaultAttributes:
                print(f"'{attribute}' is not available in the give object")
                return

        # here adding the element in the list.
        self.elements.append(element)
        return True

    def show(self):
        pass


