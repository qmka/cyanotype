import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR, TEXT_HOVER_COLOR


class SidebarMenuItem:
    def __init__(self, x, y, text, target_game_state):
        self.x = x
        self.y = y
        self.target_game_state = target_game_state
        self.text = text
        self.color = TEXT_COLOR
        self.is_hovered = False

        _item = arcade.Text(
            self.text,
            self.x,
            self.y,
            self.color,
            font_name="Fira Code SemiBold",
            font_size=12,
            anchor_x="left",
            anchor_y="top"
        )
        self.width = _item.content_width
        self.height = _item.content_height
        del _item

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
            font_name="Fira Code SemiBold",
            font_size=12,
            anchor_x="left",
            anchor_y="top"
        )
        item.draw()

    def check_hover(self, x, y):
        # check coords of top left corner of action text
        top_left_x = self.x
        top_left_y = self.y

        # check cursor is inside action text area
        if top_left_x < x < top_left_x + self.width + 10 and \
                top_left_y - self.height < y < top_left_y:
            self.is_hovered = True
        else:
            self.is_hovered = False


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