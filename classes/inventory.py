import arcade
from engine.settings import TEXT_COLOR, TEXT_HOVER_COLOR, SCREEN_HEIGHT
from engine.settings import FONT_NAME, FONT_SIZE
from engine.utils import get_arcade_text_size, is_cursor_on_object
from interface.buttons import BackButton, DeleteItemButton


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
        self.delete_item_button = DeleteItemButton()

    def add_item_by_id(self, items_list, item_id):
        item = get_item_by_id(items_list, item_id)
        self.items.append(item)

    def remove_item_by_id(self, items_list, item_id):
        item = get_item_by_id(items_list, item_id)
        self.items.remove(item)

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_items(self):
        return self.items

    def is_item_id_in_inventory(self, items_list, item_id):
        item = get_item_by_id(items_list, item_id)
        return item in self.items

    def clean_colors(self):
        for item in self.items:
            item.is_checked = False

    def draw(self):
        title = arcade.Text(
            "Инвентарь",
            50,
            SCREEN_HEIGHT - 50,
            arcade.color.BLUEBERRY,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        title.draw()
        last_item_y = 0
        if self.items:
            for index, item in enumerate(self.items):
                item_y = (index + 1) * 25
                item.draw(self.x, self.y - item_y - 25)
                last_item_y = item_y

            if self.checked_item is not None:
                description_height = self.checked_item.draw_description(350, 500)
                self.checked_item.is_checked = True
                self.delete_item_button.draw(520, self.y - description_height - 55)
        else:
            empty_text = arcade.Text(
                "Пусто",
                self.x,
                self.y - 50,
                TEXT_COLOR,
                font_name=FONT_NAME,
                font_size=FONT_SIZE,
                anchor_x="left",
                anchor_y="top"
            )
            empty_text.draw()
            last_item_y = 25

        self.back_button.draw(self.x, self.y - last_item_y - 80)


class Item:
    def __init__(self, item_id, text, description):
        self.x = 50
        self.y = 0
        self.color = TEXT_COLOR

        self.id = item_id
        self.text = text
        self.description = description

        self.is_hovered = False
        self.is_checked = False

        _size = get_arcade_text_size(self)
        self.width = _size["width"]
        self.height = _size["height"]

    def draw(self, x, y):
        self.x = x
        self.y = y
        if self.is_hovered:
            self.color = TEXT_HOVER_COLOR
        elif self.is_checked:
            self.color = arcade.color.GREEN
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
        description_height = description.content_height
        description.draw()
        return description_height

    def check_hover(self, x, y):
        self.is_hovered = is_cursor_on_object(self, x, y)


