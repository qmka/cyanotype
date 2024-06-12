import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR, TEXT_HOVER_COLOR, SCREEN_HEIGHT
from engine.settings import FONT_NAME, FONT_SIZE
from engine.utils import get_arcade_text_size, is_cursor_on_object
from interface.buttons import BackButton


def get_consumable_by_id(consumables_list, consumable_id):
    for t in consumables_list.consumable_types:
        for c in t.consumables:
            if c.id == consumable_id:
                return c
    return None


class ConsumablesList:
    def __init__(self, consumable_types):
        self.x = 50
        self.y = SCREEN_HEIGHT - 50
        self.consumable_types = consumable_types
        self.color = arcade.color.GOLDEN_YELLOW
        # self.checked_item = None
        self.back_button = BackButton()

    def set_consumable_value(self, consumable_id, value):
        consumable = get_consumable_by_id(self, consumable_id)
        consumable.set_value(value)

    def clean_colors(self):
        for consumable_type in self.consumable_types:
            consumable_type.checked_item = None
            for consumable in consumable_type.consumables:
                consumable.is_checked = False

    def draw(self):
        cursor_y = SCREEN_HEIGHT - 50
        title = arcade.Text(
            "Расходники",
            50,
            cursor_y,
            arcade.color.BLUEBERRY,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        title.draw()
        # cursor_y -= 50
        # consumable type
        if self.consumable_types:
            for index, consumable_type in enumerate(self.consumable_types):
                consumable_y = (index + 1) * 25
                cursor_y = cursor_y - consumable_y - 25
                cursor_y = consumable_type.draw(cursor_y)
        else:
            empty_text = arcade.Text(
                "Пусто",
                self.x,
                cursor_y,
                TEXT_COLOR,
                font_name=FONT_NAME,
                font_size=FONT_SIZE,
                anchor_x="left",
                anchor_y="top"
            )
            empty_text.draw()
            cursor_y -= 25

        self.back_button.draw(self.x, cursor_y - 80)

class ConsumableType:
    # Зелья, заклинания, еда
    def __init__(self, consumable_type_id, name, consumables):
        self.id = consumable_type_id
        self.name = name
        self.consumables = consumables
        self.x = 50
        self.checked_item = None

    def draw(self, cursor_y):
        # выводим заголовок
        title = arcade.Text(
            self.name,
            self.x,
            cursor_y,
            arcade.color.PINK,
            font_name=FONT_NAME,
            font_size=FONT_SIZE,
            anchor_x="left",
            anchor_y="top"
        )
        title.draw()

        if self.consumables:
            cursor_y -= 25
            for index, item in enumerate(self.consumables):
                cursor_y = cursor_y - index * 25
                item.draw(self.x, cursor_y)

            if self.checked_item is not None:
                description_height = self.checked_item.draw_description(350, 500)
                self.checked_item.is_checked = True
        else:
            cursor_y = cursor_y - 50
            empty_text = arcade.Text(
                "Пусто",
                self.x,
                cursor_y,
                TEXT_COLOR,
                font_name=FONT_NAME,
                font_size=FONT_SIZE,
                anchor_x="left",
                anchor_y="top"
            )
            empty_text.draw()
        return cursor_y

class Consumable:
    def __init__(self, consumable_id, consumable_type_id, text, description, max_value, effects):
        self.x = 50
        self.y = 0
        self.color = TEXT_COLOR

        self.id = consumable_id
        self.type = consumable_type_id
        self.text = text
        self.description = description
        self.max_value = max_value
        self.value = 0
        self.effects = effects

        self.is_hovered = False
        self.is_checked = False

        _size = get_arcade_text_size(self)
        self.width = _size["width"]
        self.height = _size["height"]

    def set_value(self, value):
        self.value = value

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