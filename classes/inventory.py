import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR, TEXT_HOVER_COLOR, SCREEN_HEIGHT
from engine.settings import FONT_NAME, FONT_SIZE
from engine.utils import get_arcade_text_size


def get_item_by_id(items_list, item_id):
    filtered_items = [item for item in items_list if item.id == item_id]
    return filtered_items[0]


class Inventory:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - 50
        self.items_count = 0
        self.items = []
        self.color = arcade.color.GOLDEN_YELLOW
        self.checked_item = None
        self.back_button = BackButton()

    def add_item(self, items_list, item_id):
        item = get_item_by_id(items_list, item_id)
        self.items.append(item)

    def remove_item(self, items_list, item_id):
        item = get_item_by_id(items_list, item_id)
        self.items.remove(item)

    def get_items(self):
        return self.items

    def draw(self):
        title = arcade.Text(
            "Инвентарь",
            50,
            SCREEN_HEIGHT - 50,
            self.color,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        title.draw()
        last_item_y = 0
        for index, item in enumerate(self.items):
            item_y = (index + 1) * 40
            item.draw(self.x, self.y - item_y)
            last_item_y = item_y

        if self.checked_item is not None:
            self.checked_item.draw_description(350, 510)

        self.back_button.draw(self.x, self.y - last_item_y - 40)


class Item:
    def __init__(self, item_id, text, description):
        self.x = 50
        self.y = 0
        self.color = TEXT_COLOR

        self.id = item_id
        self.text = text
        self.description = description

        self.is_hovered = False

        _size = get_arcade_text_size(self)
        self.width = _size["width"]
        self.height = _size["height"]

    def draw(self, x, y):
        self.x = x
        self.y = y
        if self.is_hovered:
            self.color = TEXT_HOVER_COLOR
        else:
            self.color = TEXT_COLOR

        action = arcade.Text(
            self.text,
            self.x,
            self.y,
            self.color,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        action.draw()

    def draw_description(self, x, y):
        description = arcade.Text(
            self.description,
            x,
            y,
            TEXT_COLOR,
            font_size=FONT_SIZE,
            font_name=FONT_NAME,
            multiline=True,
            width=250,
            anchor_x="left",
            anchor_y="top"
        )
        description.draw()

    def check_hover(self, x, y):
        # check coords of top left corner of action text
        top_left_x = self.x
        top_left_y = self.y  # + self.height / 2 - 10

        # check cursor is inside action text area
        if top_left_x < x < top_left_x + self.width + 10 and \
                top_left_y - self.height < y < top_left_y:
            self.is_hovered = True
        else:
            self.is_hovered = False


class BackButton:
    def __init__(self):
        self.x = 50
        self.y = 0
        self.color = arcade.color.ELECTRIC_CYAN
        self.text = "Назад"

        self.is_hovered = False

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
        # check coords of top left corner of action text
        top_left_x = self.x
        top_left_y = self.y  # + self.height / 2 - 10

        # check cursor is inside action text area
        if top_left_x < x < top_left_x + self.width + 10 and \
                top_left_y - self.height < y < top_left_y:
            self.is_hovered = True
        else:
            self.is_hovered = False

