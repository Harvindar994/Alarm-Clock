import pygame
import pygamelib

pygame.init()
width = 600
height = 300
window = pygame.display.set_mode((width, height))


class ScrollArea:
    def __init__(self, surface, area, background_properties=None):
        self.background_properties = background_properties
        self.surface = surface
        self.area = area

    @staticmethod
    def get_surface(rect):
        return pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)

    def show(self):
        pass


class Layout:
    def __init__(self, surface, x, y, margin=0, spacing=0, visibility_area=None, name="VLayout"):
        self.name = name
        self.visibility_area = visibility_area
        self.margin = margin
        self.spacing = spacing
        self.x = x
        self.y = y
        self.height = 0
        self.width = 0

        # components
        self.total_component = 0
        self.component = []

        """
        this list is containing all the default attribute that should be available in Component.
        """
        self.defaultAttributes = ['show', 'x', 'y', 'height', 'width']

        if self.name == "VLayout":
            self.Layout = self.VLayout
        elif self.name == "HLayout":
            self.Layout = self.HLayout
        else:
            raise TypeError("Invalid Layout, it can only HLayout, VLayout")

    def validate_component(self, element):
        # Here checking that all the default attributes is available in the give object or not.
        attributes = element.__dir__()
        for attribute in self.defaultAttributes:
            if attribute not in attributes:
                print(f"'{attribute}' is not available in the give object")
                return False
        return True

    def add_component(self, component, alignment='center'):
        """
        :type alignment: str
        """
        if self.validate_component(component):
            self.component.append({'component': component, 'alignment': alignment})

    def VLayout(self):
        pass

    def HLayout(self):
        pass

    def show(self):
        pass


run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((145, 34, 110))
    pygame.display.update()

