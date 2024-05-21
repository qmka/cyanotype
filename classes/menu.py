import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR, TEXT_HOVER_COLOR
from engine.settings import FONT_NAME, FONT_SIZE
from engine.utils import get_arcade_text_size, is_hovered


class SidebarMenuItem:
    def __init__(self, x, y, text, target_game_state):
        self.x = x
        self.y = y
        self.target_game_state = target_game_state
        self.text = text
        self.color = TEXT_COLOR
        self.is_hovered = False

        _size = get_arcade_text_size(self)
        self.width = _size["width"]
        self.height = _size["height"]

    def draw(self, x, y):
        self.y = y
        if self.is_hovered:
            self.color = TEXT_HOVER_COLOR
        else:
            self.color = TEXT_COLOR

        item = arcade.Text(
            self.text,
            self.x,
            self.y,
            self.color,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        item.draw()

    def check_hover(self, x, y):
        self.is_hovered = is_hovered(self, x, y)


class SidebarMenu:
    def __init__(self):
        self.x = DESCRIPTION_WIDTH + 20
        self.y = 200
        self.items_counter = 0
        self.buttons = []

    def add_item(self, text, target_game_state):
        self.buttons.append(SidebarMenuItem(self.x, self.y + 40 * self.items_counter, text, target_game_state))
        self.items_counter += 1

    def draw(self):
        if self.buttons:
            for button in self.buttons:
                button.draw(self.x, self.y)