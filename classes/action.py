import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR, TEXT_HOVER_COLOR
from engine.settings import FONT_NAME, FONT_SIZE
from engine.utils import get_arcade_text_size, is_cursor_on_object


class Action:
    def __init__(self, number, parent_scene, target_scene, text, effects, visibility_flag):
        self.x = 50
        self.y = 0
        self.color = TEXT_COLOR
        self.text = text
        self.id = number
        self.parent_scene = parent_scene
        self.target_scene = target_scene
        self.effects = effects
        self.visibility_flag = visibility_flag

        self.is_hovered = False

        _size = get_arcade_text_size(self, multiline=True, multiline_width=DESCRIPTION_WIDTH-100)
        self.width = _size["width"]
        self.height = _size["height"]

    def draw(self, y):
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
            multiline=True,
            width=DESCRIPTION_WIDTH - 100,
            anchor_x="left",
            anchor_y="top"
        )
        action.draw()

    def check_hover(self, x, y):
        self.is_hovered = is_cursor_on_object(self, x, y)
