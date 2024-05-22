import arcade
import random
from engine.settings import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, DESCRIPTION_WIDTH
from engine.settings import START_SCENE_ID
from engine.settings import FONT_PATH
from classes.scene import Scene
from classes.action import Action
from classes.stat import Stat
from classes.inventory import Inventory, Item
from classes.menu import SidebarMenu
from engine.utils import json_to_dict, is_cursor_on_object

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


def get_scene_by_id(scenes_list, scene_id):
    filtered_scenes = [scene for scene in scenes_list if scene.id == scene_id]
    return filtered_scenes[0]


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)

        self.game_state = None
        self.scenes = None
        self.actions = None
        self.stats = None
        self.inventory = None
        self.items = None
        self.current_scene_id = None
        self.current_scene_actions = None
        self.is_scene_changed = False
        self.hero_portrait = None
        self.menu = None

    def setup(self):

        # upload font
        arcade.load_font(FONT_PATH)

        # upload graphics
        hero_portrait_image_path = "media/images/hero.png"
        self.hero_portrait = arcade.Sprite(hero_portrait_image_path)

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

        # get items
        raw_items = json_to_dict("content/items.json")
        items = []
        for a in raw_items["items"]:
            items.append(Item(a["id"], a["text"], a["description"]))

        # setup sidebar menu
        self.menu = SidebarMenu()
        self.menu.add_item("Инвентарь", STATE_INVENTORY)

        # config game
        self.game_state = STATE_START
        self.scenes = scenes
        self.actions = actions
        self.stats = stats
        self.items = items
        self.current_scene_id = START_SCENE_ID
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, self.current_scene_id)

        # fill inventory
        self.inventory = Inventory()
        self.inventory.add_item_by_id(self.items, 0)
        self.inventory.add_item_by_id(self.items, 1)

    def on_draw(self):
        arcade.start_render()
        if self.game_state == STATE_MAIN:
            self.draw_hero_portrait()
            self.draw_hero_stats()
            self.draw_sidebar_menu()
            self.draw_scene_with_actions()
        elif self.game_state == STATE_START:
            self.draw_scene_with_actions()
        elif self.game_state == STATE_INVENTORY:
            self.draw_hero_portrait()
            self.draw_hero_stats()
            self.draw_sidebar_menu()
            self.draw_inventory()

    def draw_hero_portrait(self):
        self.hero_portrait.center_x = DESCRIPTION_WIDTH + 100
        self.hero_portrait.center_y = 500
        self.hero_portrait.draw()

    def draw_hero_stats(self):
        for index, stat in enumerate(self.stats):
            stat.draw(SCREEN_HEIGHT - 200 - 30 * index)

    def draw_scene_with_actions(self):
        current_scene = get_scene_by_id(self.scenes, self.current_scene_id)
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, current_scene.id)
        current_scene.draw()
        scene_desc_height = current_scene.height
        for index, action in enumerate(self.current_scene_actions):
            action.draw(SCREEN_HEIGHT - scene_desc_height - 150 - 40 * index)

    def draw_sidebar_menu(self):
        self.menu.draw()

    def draw_inventory(self):
        self.inventory.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # actions
        if self.game_state == STATE_START or self.game_state == STATE_MAIN:
            for action in self.actions:
                action.check_hover(x, y)
        # menu buttons
        if self.game_state != STATE_START:
            for button in self.menu.buttons:
                button.check_hover(x, y)
        # inventory items
        if self.game_state == STATE_INVENTORY:
            for item in self.inventory.items:
                item.check_hover(x, y)
            self.inventory.back_button.check_hover(x, y)
            self.inventory.delete_item_button.check_hover(x, y)

    def on_mouse_press(self, x, y, action, modifiers):

        # actions
        if self.game_state == STATE_START or self.game_state == STATE_MAIN:
            for a in self.current_scene_actions:
                if is_cursor_on_object(a, x, y):
                    print(f"Выбран action id {a.id}")
                    self.apply_action_effects(a.effects)
                    if not self.is_scene_changed:
                        self.current_scene_id = a.target_scene
                        self.is_scene_changed = False

        # menu buttons
        if self.game_state != STATE_START:
            for a in self.menu.buttons:
                if is_cursor_on_object(a, x, y):
                    print(f"Выбран menu item {a.text}")
                    self.game_state = a.target_game_state

        # inventory items
        if self.game_state == STATE_INVENTORY:
            for a in self.inventory.items:
                if is_cursor_on_object(a, x, y):
                    self.inventory.clean_colors()
                    self.inventory.checked_item = a

            if self.inventory.back_button.check_press(x, y):
                self.inventory.back_button.is_pressed = False
                self.inventory.checked_item = None
                self.game_state = STATE_MAIN

            if self.inventory.checked_item and self.inventory.delete_item_button.check_press(x, y):
                self.inventory.delete_item_button.is_pressed = False
                self.inventory.remove_item(self.inventory.checked_item)
                self.inventory.checked_item = None

    def apply_action_effects(self, effects):
        if effects:
            for effect in effects:
                effect_type = effect["effect_type"]
                target = effect["target"] if "target" in effect else None
                value = effect["value"] if "value" in effect else None

                if effect_type == "CHANGE_STAT":
                    changed_stat = get_stat_by_id(self.stats, target)
                    changed_stat.change(value)
                elif effect_type == "CHANGE_GAME_STATE":
                    print(f'gamestate changet to {target}')
                    self.game_state = target
                elif effect_type == "CHECK_LUCK":   # экшен с изменением сцены должен быть один в списке экшенов,
                    # а в этом списке - в конце (для перестраховки - пока не понимаю, будет ли это работать корректно)
                    luck_check = random.choice([True, False])
                    self.current_scene_id = effect["good_target"] if luck_check else effect["bad_target"]
                    self.is_scene_changed = True


def main():
    game = GameWindow()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
