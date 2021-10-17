import random

import pygame
import pygamelib

pygame.init()
width = 1200
height = 600
window = pygame.display.set_mode((width, height))


class ScrollArea:
    def __init__(self, surface, x, y, background_properties=None, layout=None):
        self.background_properties = background_properties
        self.surface = surface
        self.x = x
        self.y = y

        # Scroll Surface
        self.ScrollAreaSurface = None

        # it will be containing layout
        self.Layout = layout

    @staticmethod
    def get_surface(rect):
        return pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)

    def validate_layout(self, layout):
        # Here checking that all the default attributes is available in the give object or not.
        attributes = layout.__dir__()
        for attribute in ['width', 'name', 'height', 'x', 'y']:
            if attribute not in attributes:
                print(f"'{attribute}' is not available in the give object")
                return False
        return True

    def set_layout(self, layout):
        if self.validate_layout(layout):
            self.Layout = layout
        else:
            raise TypeError('Invalid Layout')

    def show(self, event=None):
        if event is None:
            pass

        else:
            pass


class Layout:
    def __init__(self, surface, x, y, margin=(0, 0, 0, 0),
                 spacing=0, visibility_area=None, name="VLayout", min_width=0):
        self.surface = surface
        self.name = name
        self.visibility_area = visibility_area
        self.spacing = spacing
        self.margin_left, self.margin_top, self.margin_right, self.margin_bottom = margin
        self.x = x
        self.y = y
        self.height = 0
        self.width = 0

        # components
        self.total_component = 0
        self.components = []

        """
        this list is containing all the default attribute that should be available in Component.
        """
        self.defaultAttributes = ['show', 'x', 'y', 'height', 'width']

        self.width += (self.margin_left + self.margin_right)
        self.height += (self.margin_top + self.margin_bottom)

        if self.name is not "VLayout" and self.name is not "HLayout":
            raise TypeError("Invalid Layout, it can only HLayout, VLayout")

        if self.name == 'VLayout':
            self.width += min_width
        else:
            self.height += min_width

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
            if self.name == "VLayout":
                if self.width < component.width:
                    self.width = component.width + self.margin_left + self.margin_right
                self.height += component.height
                if self.total_component > 0:
                    self.height += self.spacing
            else:
                if component.height > self.height:
                    self.height = component.height + self.margin_top + self.margin_bottom
                self.width += component.width
                if self.total_component > 0:
                    self.width += self.spacing

            self.components.append({'component': component, 'alignment': alignment})
            self.total_component += 1

    def VLayout(self):
        x = self.x + self.margin_left
        y = self.y + self.margin_top
        for component in self.components:
            alignment = component['alignment']
            component = component['component']
            if alignment == 'center':
                component.x = x + (((self.width-(self.margin_left + self.margin_right)) / 2) - (component.width / 2))
            elif alignment == 'left':
                component.x = x
            elif alignment == 'right':
                component.x = (x + (self.width-(self.margin_left + self.margin_right))) - component.width
            else:
                component.x = x
            component.y = y
            if self.visibility_area is not None:
                v_y, height = self.visibility_area
                pygame.draw.rect(self.surface, (255, 255, 255), (self.x, v_y, self.width, height), 1)
                pygame.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)
                if component.y >= v_y and component.y+component.height <= v_y + height:
                    component.show()
                elif component.y > v_y + height:
                    break
            else:
                component.show()
            y += component.height + self.spacing

    def HLayout(self):
        x = self.x + self.margin_left
        y = self.y + self.margin_top
        for component in self.components:
            alignment = component['alignment']
            component = component['component']
            if alignment == 'center':
                component.y = y + (((self.height-(self.margin_bottom + self.margin_top)) / 2) - (component.height / 2))
            elif alignment == 'top':
                component.y = y
            elif alignment == 'bottom':
                component.y = (y + (self.height-(self.margin_bottom + self.margin_top))) - component.height
            else:
                component.y = y
            component.x = x
            if self.visibility_area is not None:
                v_x, height = self.visibility_area
                pygame.draw.rect(self.surface, (255, 255, 255), (v_x, self.y, height, self.height), 1)
                pygame.draw.rect(self.surface, (0, 0, 0), (self.x, self.y, self.width, self.height), 1)
                if component.x >= v_x and component.x+component.width <= v_x + height:
                    component.show()
                elif component.x > v_x + height:
                    break
            else:
                component.show()
            x += component.width + self.spacing

    def show(self):
        if self.name == "VLayout":
            self.VLayout()
        else:
            self.HLayout()


layout = Layout(window, 10, 10, spacing=10, visibility_area=(10, 900), margin=(10, 10, 10, 10), name="VLayout")

for e in range(20):
    layout.add_component(pygamelib.Frame(window, 'frame_1', (0, 0, random.randint(600, 800), 30), (45, 67, 44)), alignment=random.choice(('left', 'right')))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                layout.y -= 10
            elif event.key == pygame.K_s:
                layout.y += 10

    window.fill((145, 34, 110))
    layout.show()
    pygame.display.update()
