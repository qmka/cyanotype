import arcade
from engine.settings import SCREEN_WIDTH, SCREEN_HEIGHT, DESCRIPTION_WIDTH, DESCRIPTION_HEIGHT
from engine.settings import CHARACTER_WIDTH, CHARACTER_HEIGHT, BACKGROUND_COLOR, TEXT_COLOR
from engine.settings import START_SCENE_ID
from classes.scene import Scene
from classes.action import Action
from classes.stat import Stat
from engine.utils import json_to_dict

# Game States
STATE_START = 0
STATE_MAIN = 1
STATE_INVENTORY = 2


def filter_actions_by_scene_id(actions_list, scene_id):
    filtered_actions = [action for action in actions_list if action.parent_scene == scene_id]
    return filtered_actions


def get_stat_by_id(stats_list, stat_id):
    filtered_stats = [stat for stat in stats_list if stat.id == stat_id]
    return filtered_stats[0]


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Choose Your Adventure")

        arcade.load_font("fonts/FiraCode-SemiBold.ttf")

        hero_portrait_image_path = "media/images/hero.png"
        self.hero_portrait = arcade.Sprite(hero_portrait_image_path)

        # Определение начальных характеристик персонажа
        self.character_name = "Hero"
        self.health = 100
        self.strength = 10
        self.defense = 5

        # get scenes
        raw_scenes = json_to_dict("content/scenes.json")
        scenes = []
        for a in raw_scenes["scenes"]:
            scenes.append(Scene(a["id"], a["description"]))

        # get actions
        raw_actions = json_to_dict("content/actions.json")
        actions = []
        for a in raw_actions["actions"]:
            if "effects" in a:
                effects = a["effects"]
            else:
                effects = []
            actions.append(Action(a["id"], a["parent"], a["target"], a["text"], effects))

        # get stats
        raw_stats = json_to_dict("content/stats.json")
        stats = []
        for a in raw_stats["stats"]:
            stats.append(Stat(a["id"], a["text"], a["value"]))

        # config game
        self.game_state = STATE_MAIN
        self.scenes = scenes
        self.actions = actions
        self.stats = stats
        self.current_scene_id = START_SCENE_ID
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, self.current_scene_id)

    def on_draw(self):
        arcade.start_render()
        if self.game_state == STATE_MAIN:
            self.draw_hero_portrait()
            self.draw_hero_stats()
            self.draw_scene_with_actions()
        elif self.game_state == STATE_START:
            self.draw_hero_portrait()

    def draw_hero_portrait(self):
        self.hero_portrait.center_x = DESCRIPTION_WIDTH + 100
        self.hero_portrait.center_y = 500
        self.hero_portrait.draw()

    def draw_hero_stats(self):
        for index, stat in enumerate(self.stats):
            stat.draw(SCREEN_HEIGHT - 200 - 30 * index)

    def draw_scene_with_actions(self):
        current_scene = self.scenes[self.current_scene_id]
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, current_scene.id)
        current_scene.draw()
        scene_desc_height = current_scene.height
        for index, action in enumerate(self.current_scene_actions):
            action.draw(SCREEN_HEIGHT - scene_desc_height - 150 - 40 * index)

    def on_mouse_motion(self, x, y, dx, dy):
        for action in self.actions:
            action.check_hover(x, y)

    def on_mouse_press(self, x, y, action, modifiers):
        for ac in self.current_scene_actions:
            top_left_x = ac.x
            top_left_y = ac.y + ac.height / 2 - 10
            if top_left_x < x < top_left_x + ac.width + 10 and top_left_y - ac.height < y < top_left_y:
                print(f"Выбран action id {ac.id}")
                self.apply_action_effects(ac.effects)
                self.current_scene_id = ac.target_scene

    def apply_action_effects(self, effects):
        if effects:
            for effect in effects:
                effect_type = effect["effect_type"]
                target = effect["target"]
                value = effect["value"]
                if effect_type == "CHANGE_STAT":
                    # Достаём стат с нужным id
                    changed_stat = get_stat_by_id(self.stats, target)
                    changed_stat.change(value)


def main():
    window = GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
