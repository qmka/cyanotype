import arcade
from engine.settings import SCREEN_WIDTH, SCREEN_HEIGHT, DESCRIPTION_WIDTH, DESCRIPTION_HEIGHT
from engine.settings import CHARACTER_WIDTH, CHARACTER_HEIGHT, BACKGROUND_COLOR, TEXT_COLOR
from classes.scene import Scene
from classes.action import Action


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

        scenes = [
            Scene(0, "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "),
            Scene(1, "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea ")
        ]

        actions = [
            Action(0, 0, "Пустое действие"),
            Action(1, 0, "Переход в сцену 1"),
            Action(2, 1, "Возврат в сцену 0"),
            Action(3, 1, "Ещё одно пустое действие")
        ]

        self.scenes = scenes

        self.current_scene_id = 0
        self.actions = actions

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
        current_scene_actions = filter_actions_by_scene_id(self.actions, current_scene.id)
        current_scene.draw()
        scene_desc_height = current_scene.height

        arcade.draw_text("Выберите действие:", 50, SCREEN_HEIGHT - scene_desc_height - 100, TEXT_COLOR, 12,
                         font_name="Fira Code SemiBold",
                         anchor_x="left",
                         anchor_y="top")

        for index, action in enumerate(current_scene_actions):
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
        for idx, btn in enumerate(self.actions):
            top_left_x = btn.x
            top_left_y = btn.y + btn.height / 2 - 10
            if top_left_x < x < top_left_x + btn.width + 10 and top_left_y - btn.height < y < top_left_y:
                if idx == 0:
                    print("Нажата кнопка 0")
                    self.current_scene_id = 0
                elif idx == 1:
                    print("Нажата кнопка 1")
                    self.current_scene_id = 1
                elif idx == 2:
                    print("Нажата кнопка 2")
                    self.current_scene_id = 0
                elif idx == 3:
                    print("Нажата кнопка 3")
                    self.current_scene_id = 1



def main():
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
