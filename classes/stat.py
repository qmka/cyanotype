import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR
from engine.settings import FONT_NAME, FONT_SIZE, FADE_DURATION


class Stat:
    def __init__(self, number, text, value):
        self.id = number
        self.text = text
        self.value = value

        self.x = DESCRIPTION_WIDTH + 20
        self.y = 0
        self.color = TEXT_COLOR

        self.start_flashing = 0
        self.flashing_color = arcade.color.RED

    def set(self, value):
        self.value = value

    def change(self, value):
        self.value += value

    def set_flash(self, timer, value):
        self.start_flashing = timer
        if value > 0:
            self.flashing_color = arcade.color.GREEN
        else:
            self.flashing_color = arcade.color.RED

    def draw(self, y, timer):
        if timer > self.start_flashing and timer < (self.start_flashing + FADE_DURATION):
            # color = self.flashing_color
            elapsed_time = timer - self.start_flashing
            if elapsed_time < FADE_DURATION:
                fade_factor = elapsed_time / FADE_DURATION
                red = int(self.flashing_color[0] * (1 - fade_factor) + arcade.color.WHITE[0] * fade_factor)
                green = int(self.flashing_color[1] * (1 - fade_factor) + arcade.color.WHITE[1] * fade_factor)
                blue = int(self.flashing_color[2] * (1 - fade_factor) + arcade.color.WHITE[2] * fade_factor)
                color = (red, green, blue)
            else:
                color = self.color
        else:
            color = self.color

        self.y = y
        action = arcade.Text(
            f"{self.text}: {self.value}",
            self.x,
            self.y,
            color,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        action.draw()
