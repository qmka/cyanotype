import arcade
from engine.utils import get_arcade_text_size, is_cursor_on_object
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR, TEXT_HOVER_COLOR, SCREEN_HEIGHT
from engine.settings import FONT_NAME, FONT_SIZE


class BackButton:
    def __init__(self):
        self.x = 50
        self.y = 0
        self.color = arcade.color.ELECTRIC_CYAN
        self.text = "Назад"

        self.is_hovered = False
        self.is_pressed = False

        _size = get_arcade_text_size(self)
        self.width = _size["width"]
        self.height = _size["height"]

    def draw(self, x, y):
        self.x = x
        self.y = y
        if self.is_hovered:
            self.color = TEXT_HOVER_COLOR
        else:
            self.color = arcade.color.ELECTRIC_CYAN

        action = arcade.Text(
            self.text,
            self.x,
            self.y,
            self.color,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            multiline=True,
            width=DESCRIPTION_WIDTH - 100,
            anchor_x="left",
            anchor_y="top"
        )
        action.draw()

    def check_hover(self, x, y):
        self.is_hovered = is_cursor_on_object(self, x, y)
        return self.is_hovered

    def check_press(self, x, y):
        self.is_pressed = is_cursor_on_object(self, x, y)
        return self.is_pressed


class DeleteItemButton:
    def __init__(self):
        self.x = 50
        self.y = 0
        self.color = arcade.color.RED
        self.text = "Удалить"

        self.is_hovered = False
        self.is_pressed = False

        _size = get_arcade_text_size(self)
        self.width = _size["width"]
        self.height = _size["height"]

    def draw(self, x, y):
        self.x = x
        self.y = y
        if self.is_hovered:
            self.color = TEXT_HOVER_COLOR
        else:
            self.color = arcade.color.RED

        action = arcade.Text(
            self.text,
            self.x,
            self.y,
            self.color,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            multiline=True,
            width=DESCRIPTION_WIDTH - 100,
            anchor_x="left",
            anchor_y="top"
        )
        action.draw()

    def check_hover(self, x, y):
        self.is_hovered = is_cursor_on_object(self, x, y)
        return self.is_hovered

    def check_press(self, x, y):
        self.is_pressed = is_cursor_on_object(self, x, y)
        return self.is_pressed
