import pygame
from structures import Vec2

pygame.init()

UI_FONT = pygame.font.SysFont("Fira-Code", 16)
LINE_SPACING = 20
FONT_COLOR = (255, 255, 255)

class Gui:
    def __init__(self, **kwargs):
        self.members = set(["data", "prev_mouse_x", "value_rects", "active_value"])
        self.data = kwargs
        self.prev_mouse_x = None
        self.value_rects = {}
        self.active_value = None

    def __getattr__(self, name):
        if self.data[name][1] == True:
            return int(self.data[name][2])
        return self.data[name][2]
    
    def __setattr__(self, name, value):
        if name == "members" or name in self.members:
            self.__dict__[name] = value
        else:
            self.data[name][2] = value
    
    def draw(self, screen):
        self.value_rects = {}
        counter = 0
        for slider_name, slider_properties in self.data.items():
            min, max, value = slider_properties

            slider_name_font = UI_FONT.render(f"{slider_name} = ", True, FONT_COLOR)
            slider_name_width, slider_name_height = slider_name_font.get_size()
            draw_height = LINE_SPACING * counter

            screen.blit(slider_name_font, (0, draw_height))

            value_str = ""
            if slider_properties[1] == True:
                value_str = str(int(value))
            else:
                value_str = str(value)[:10]

            value_font = UI_FONT.render(value_str, True, FONT_COLOR, (50, 50, 50))
            screen.blit(value_font, (slider_name_width, draw_height))

            value_font_width, value_font_height = value_font.get_size()
            self.value_rects[(slider_name_width, draw_height, value_font_width, value_font_height)] = slider_name

            counter += 1

    def update(self, mouse_pos):
        if self.active_value is not None:
            mouse_x = mouse_pos[0]
            active_value = self.active_value
            self.data[active_value][2] += (mouse_x - self.prev_mouse_x) * self.data[active_value][0]
            self.prev_mouse_x = mouse_x

    def on_mouse_down(self, mouse_pos):

        for rect, value_name in self.value_rects.items():
            if pygame.Rect(rect).collidepoint(mouse_pos):
                self.active_value = value_name

        self.prev_mouse_x = mouse_pos[0]
    
    def on_mouse_up(self):
        self.prev_mouse_x = None
        self.active_value = None