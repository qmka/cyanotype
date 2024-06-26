import arcade
from engine.settings import SCREEN_HEIGHT, DESCRIPTION_WIDTH, TEXT_COLOR
from engine.settings import FONT_NAME, FONT_SIZE


class Scene:
    def __init__(self, number, text):
        self.id = number
        self.scene = arcade.Text(
            text,
            50,
            SCREEN_HEIGHT - 50,
            TEXT_COLOR,
            font_size=FONT_SIZE,
            font_name=FONT_NAME,
            multiline=True,
            width=DESCRIPTION_WIDTH - 100,
            anchor_x="left",
            anchor_y="top"
        )
        self.height = self.scene.content_height

    def draw(self):
        self.scene.draw()
