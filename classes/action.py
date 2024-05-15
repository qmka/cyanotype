import arcade
from engine.settings import DESCRIPTION_WIDTH, TEXT_COLOR, TEXT_HOVER_COLOR


class Action:
    def __init__(self, number, parent_scene, text):
        self.x = 50
        self.y = 0
        self.color = TEXT_COLOR
        self.text = text
        self.id = number
        self.parent_scene = parent_scene

        self.is_hovered = False

        _action = arcade.Text(
            self.text,
            self.x,
            self.y,
            self.color,
            font_name="Fira Code SemiBold",
            font_size=12,
            multiline=True,
            width=DESCRIPTION_WIDTH - 100,
            anchor_x="left",
            anchor_y="top"
        )
        self.width = _action.content_width
        self.height = _action.content_height
        del _action

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
            font_name="Fira Code SemiBold",
            font_size=12,
            multiline=True,
            width=DESCRIPTION_WIDTH - 100,
            anchor_x="left",
            anchor_y="top"
        )
        action.draw()

    def check_hover(self, x, y):
        # check coords of top left corner of action text
        top_left_x = self.x
        top_left_y = self.y + self.height / 2 - 10

        # check cursor is inside action text area
        if top_left_x < x < top_left_x + self.width + 10 and \
                top_left_y - self.height < y < top_left_y:
            self.is_hovered = True
        else:
            self.is_hovered = False
