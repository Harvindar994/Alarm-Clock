import pygame


class Frame:
    def __init__(self, name, area, backgroundColor=None, partition=None):
        self.name = name
        self.x, self.y, self.width, self.height = area

        """
        data structure of partition will be in percentage.
        structure: {area in percentage: color, area in percentage: color}
        note: partition will work to define diffrent area with diffrent color, and it will be in the vertical way.
        """
        self.partition = partition
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

    def rePartition(self):
        pass

    def show(self):
        if self.backgroundColor is not None:
            if self.partition is None:
                pass
            else:
                pass


    def showElement(self):
        for element in self.elements:
            element.show()


