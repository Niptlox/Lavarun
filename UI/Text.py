import pygame
from UI.Frame import *


class Label(Frame):
    def __init__(self, rect, bg=BLACK, text="", font=TEXTFONT, text_color=WHITE, hspace=5, vspace=5):
        super().__init__(rect, bg)
        self.text = None
        self.font = None
        self.text_color = None
        self.hspace = hspace
        self.vspace = vspace
        self.setText(text, font=font, text_color=text_color)

    def setText(self, text, font=None, text_color=None):
        self.text = str(text)
        self.font = self.font if font is None else font
        self.text_color = self.text_color if text_color is None else text_color
        self.redraw()

    def redraw(self):
        self.image.blit(self.bg, (0, 0))
        texframe = self.font.render(self.text, False, self.text_color)
        self.image.blit(texframe, (self.hspace, self.vspace))

