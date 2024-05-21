import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR
from engine.settings import FONT_NAME, FONT_SIZE


class Stat:
    def __init__(self, number, text, value):
        self.id = number
        self.text = text
        self.value = value

        self.x = DESCRIPTION_WIDTH + 20
        self.y = 0
        self.color = TEXT_COLOR

    def set(self, value):
        self.value = value

    def change(self, value):
        self.value += value

    def draw(self, y):
        self.y = y
        action = arcade.Text(
            f"{self.text}: {self.value}",
            self.x,
            self.y,
            self.color,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        action.draw()
