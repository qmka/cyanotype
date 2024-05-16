import arcade
from engine.settings import SCREEN_WIDTH, SCREEN_HEIGHT, DESCRIPTION_WIDTH, DESCRIPTION_HEIGHT
from engine.settings import CHARACTER_WIDTH, CHARACTER_HEIGHT, BACKGROUND_COLOR, TEXT_COLOR
from engine.settings import START_SCENE_ID
from classes.scene import Scene
from classes.action import Action
from engine.utils import json_to_dict


def filter_actions_by_scene_id(actions_list, scene_id):
    filtered_actions = [action for action in actions_list if action.parent_scene == scene_id]
    return filtered_actions



class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Choose Your Adventure")

        arcade.load_font("fonts/FiraCode-SemiBold.ttf")

        # Определение начальных характеристик персонажа
        self.character_name = "Hero"
        self.health = 100
        self.strength = 10
        self.defense = 5

        # get scenes
        raw_scenes = json_to_dict("content/scenes.json")
        scenes = []
        for s in raw_scenes["scenes"]:
            scenes.append(Scene(s["id"], s["description"]))

        # get actions
        raw_actions = json_to_dict("content/actions.json")
        actions = []
        for a in raw_actions["actions"]:
            actions.append(Action(a["id"], a["parent"], a["target"], a["text"]))

        self.scenes = scenes
        self.actions = actions
        self.current_scene_id = START_SCENE_ID
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, self.current_scene_id)

    def on_draw(self):
        arcade.start_render()

        # Рисуем левую область с описанием сцены и действиями
        arcade.draw_rectangle_filled(
            DESCRIPTION_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            DESCRIPTION_WIDTH,
            DESCRIPTION_HEIGHT,
            BACKGROUND_COLOR
        )
        current_scene = self.scenes[self.current_scene_id]
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, current_scene.id)
        current_scene.draw()
        scene_desc_height = current_scene.height

        arcade.draw_text("Выберите действие:", 50, SCREEN_HEIGHT - scene_desc_height - 100, TEXT_COLOR, 12,
                         font_name="Fira Code SemiBold",
                         anchor_x="left",
                         anchor_y="top")

        for index, action in enumerate(self.current_scene_actions):
            action.draw(SCREEN_HEIGHT - scene_desc_height - 150 - 40 * index)

        # Рисуем правую область с характеристиками персонажа
        arcade.draw_rectangle_filled(DESCRIPTION_WIDTH + CHARACTER_WIDTH / 2, SCREEN_HEIGHT / 2, CHARACTER_WIDTH,
                                     CHARACTER_HEIGHT, arcade.color.BEIGE)
        arcade.draw_text("Характеристики персонажа:", DESCRIPTION_WIDTH + 50, SCREEN_HEIGHT - 50, arcade.color.BLACK,
                         16, anchor_x="left", anchor_y="top")
        arcade.draw_text(f"Имя: {self.character_name}", DESCRIPTION_WIDTH + 50, SCREEN_HEIGHT - 100, arcade.color.BLACK,
                         12, anchor_x="left", anchor_y="top")
        arcade.draw_text(f"Здоровье: {self.health}", DESCRIPTION_WIDTH + 50, SCREEN_HEIGHT - 130, arcade.color.BLACK,
                         12, anchor_x="left", anchor_y="top")
        arcade.draw_text(f"Сила: {self.strength}", DESCRIPTION_WIDTH + 50, SCREEN_HEIGHT - 160, arcade.color.BLACK, 12,
                         anchor_x="left", anchor_y="top")
        arcade.draw_text(f"Защита: {self.defense}", DESCRIPTION_WIDTH + 50, SCREEN_HEIGHT - 190, arcade.color.BLACK, 12,
                         anchor_x="left", anchor_y="top")

    def on_mouse_motion(self, x, y, dx, dy):
        for action in self.actions:
            action.check_hover(x, y)

    def on_mouse_press(self, x, y, action, modifiers):
        for ac in self.current_scene_actions:
            top_left_x = ac.x
            top_left_y = ac.y + ac.height / 2 - 10
            if top_left_x < x < top_left_x + ac.width + 10 and top_left_y - ac.height < y < top_left_y:
                print(f"Выбран action id {ac.id}")
                self.current_scene_id = ac.target_scene


def main():
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
