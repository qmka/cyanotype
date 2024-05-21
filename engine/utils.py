import json
import arcade
from engine.settings import FONT_SIZE, FONT_NAME, DESCRIPTION_WIDTH


def json_to_dict(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File '{json_file}' Not Found")
        return None
    except json.decoder.JSONDecodeError:
        print(f"Unable to extract JSON from '{json_file}'")
        return None


def get_arcade_text_size(arcade_object, multiline=False, multiline_width=None):
    obj = arcade.Text(
        arcade_object.text,
        arcade_object.x,
        arcade_object.y,
        arcade_object.color,
        font_name=FONT_NAME,
        font_size=FONT_SIZE,
        multiline=multiline,
        width=multiline_width,
        anchor_x="left",
        anchor_y="top"
    )
    width = obj.content_width
    height = obj.content_height
    del obj
    return {
        "width": width,
        "height": height
    }


def is_cursor_on_object (arcade_object, x, y):
    # check coords of top left corner of action text
    top_left_x = arcade_object.x
    top_left_y = arcade_object.y  # + self.height / 2 - 10

    # check cursor is inside action text area
    if top_left_x < x < top_left_x + arcade_object.width + 10 and top_left_y - arcade_object.height < y < top_left_y:
        return True
    return False
