import arcade
import random
from engine.settings import GAME_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT, DESCRIPTION_WIDTH
from engine.settings import START_SCENE_ID, START_STATE
from engine.settings import FONT_PATH
from classes.scene import Scene
from classes.action import Action
from classes.stat import Stat
from classes.flag import Flag
from classes.inventory import Inventory, Item
from classes.consumables import ConsumablesList, ConsumableType, Consumable
from classes.menu import SidebarMenu
from engine.utils import read_content, is_cursor_on_object

# Game States
STATE_START = 0
STATE_MAIN = 1
STATE_INVENTORY = 2
STATE_CONSUMABLES = 3


def filter_actions_by_scene_id(actions_list, scene_id):
    filtered_actions = [action for action in actions_list if action.parent_scene == scene_id]
    return filtered_actions

def get_by_id(entities_list, entity_id):
    return next((entity for entity in entities_list if entity.id == entity_id), None)


def get_consumable_by_id(consumables_list, consumable_id):
    for t in consumables_list.consumable_types:
        for c in t.consumables:
            if c.id == consumable_id:
                return c
    return None


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)

        self.game_state = None
        self.scenes = None
        self.actions = None
        self.stats = None
        self.flags = None
        self.inventory = None
        self.consumables_list = None
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
        raw_scenes = read_content("content/scenes.yaml")
        scenes = []
        for a in raw_scenes["scenes"]:
            scenes.append(Scene(a["id"], a["description"]))

        # get actions
        raw_actions = read_content("content/actions.yaml")
        actions = []
        for a in raw_actions["actions"]:
            if "effects" in a:
                effects = a["effects"]
            else:
                effects = []
            if "visibility_flag" in a:
                visibility_flag = a["visibility_flag"]
            else:
                visibility_flag = None
            actions.append(Action(a["id"], a["parent"], a["target"], a["text"], effects, visibility_flag))

        # get stats
        raw_stats = read_content("content/stats.yaml")
        stats = []
        for a in raw_stats["stats"]:
            stats.append(Stat(a["id"], a["text"], a["value"]))

        # get flags
        raw_flags = read_content("content/flags.yaml")
        flags = []
        for a in raw_flags["flags"]:
            flags.append(Flag(a["id"], a["value"]))

        # get items
        raw_items = read_content("content/items.yaml")
        items = []
        for a in raw_items["items"]:
            items.append(Item(a["id"], a["text"], a["description"]))

        # get consumables
        raw_consumables_list = read_content("content/consumables.yaml")
        consumables_list = []
        for t in raw_consumables_list["consumable_types"]:
            consumables = []
            this_type_consumables = t["consumables"]
            for c in this_type_consumables:
                # (consumable_id, consumable_type_id, text, description, max_value)
                consumables.append(Consumable(c["id"], c["type"], c["text"], c["description"], c["max_value"],
                                              c["effects"]))
            consumables_list.append(ConsumableType(t["id"], t["name"], consumables))

        # setup sidebar menu
        self.menu = SidebarMenu()
        self.menu.add_item("Инвентарь", STATE_INVENTORY)
        self.menu.add_item("Расходники", STATE_CONSUMABLES)

        # config game
        self.game_state = START_STATE
        self.scenes = scenes
        self.actions = actions
        self.stats = stats
        self.flags = flags
        self.items = items
        self.current_scene_id = START_SCENE_ID
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, self.current_scene_id)

        self.inventory = Inventory()
        self.consumables_list = ConsumablesList(consumables_list)

        # fill inventory
        # self.inventory.add_item_by_id(self.items, 0)
        # self.inventory.add_item_by_id(self.items, 1)

        # fill consumables
        # self.consumables_list.set_consumable_value(0, 2)
        self.consumables_list.set_consumable_value(1, 2)
        self.consumables_list.set_consumable_value(2, 2)

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
        elif self.game_state == STATE_CONSUMABLES:
            self.draw_hero_portrait()
            self.draw_hero_stats()
            self.draw_sidebar_menu()
            self.draw_consumables()

    def draw_hero_portrait(self):
        self.hero_portrait.center_x = DESCRIPTION_WIDTH + 100
        self.hero_portrait.center_y = 500
        self.hero_portrait.draw()

    def draw_hero_stats(self):
        for index, stat in enumerate(self.stats):
            stat.draw(SCREEN_HEIGHT - 200 - 30 * index)

    def draw_scene_with_actions(self):
        current_scene = get_by_id(self.scenes, self.current_scene_id)
        self.current_scene_actions = filter_actions_by_scene_id(self.actions, current_scene.id)
        current_scene.draw()
        scene_desc_height = current_scene.height

        displayed_actions = []
        for action in self.current_scene_actions:
            # check visibility flag
            action_visibility = True
            if action.visibility_flag:
                flag = get_by_id(self.flags, action.visibility_flag["id"])
                if flag.value != action.visibility_flag["value"]:
                    action_visibility = False

            if action_visibility:
                displayed_actions.append(action)

        if scene_desc_height > 150:
            actions_top_y = SCREEN_HEIGHT - scene_desc_height - 50
        else:
            actions_top_y = SCREEN_HEIGHT - 175

        actions_line_number = 1
        for action in displayed_actions:
            action.draw(actions_top_y - 25 * actions_line_number)
            actions_line_number += action.height / 25 + 1

    def draw_sidebar_menu(self):
        self.menu.draw()

    def draw_inventory(self):
        self.inventory.draw()

    def draw_consumables(self):
        self.consumables_list.draw()

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
        # consumables
        if self.game_state == STATE_CONSUMABLES:
            for consumable_type in self.consumables_list.consumable_types:
                consumable_type.use_consumable_button.check_hover(x, y)
                for consumable in consumable_type.consumables:
                    consumable.check_hover(x, y)
            self.consumables_list.back_button.check_hover(x, y)

    def on_mouse_press(self, x, y, action, modifiers):

        # actions
        if self.game_state == STATE_START or self.game_state == STATE_MAIN:
            for a in self.current_scene_actions:
                if is_cursor_on_object(a, x, y):
                    self.apply_effects(a.effects)
                    self.apply_after_effects()
                    if not self.is_scene_changed:
                        self.current_scene_id = a.target_scene
                    self.is_scene_changed = False

        # menu buttons
        if self.game_state != STATE_START:
            for a in self.menu.buttons:
                if is_cursor_on_object(a, x, y):
                    self.game_state = a.target_game_state

        # inventory items
        if self.game_state == STATE_INVENTORY:
            for a in self.inventory.items:
                if is_cursor_on_object(a, x, y):
                    self.inventory.uncheck_all()
                    self.inventory.checked_item = a

            if self.inventory.back_button.check_press(x, y):
                self.inventory.back_button.is_pressed = False
                self.inventory.checked_item = None
                self.game_state = STATE_MAIN

            if self.inventory.checked_item and self.inventory.delete_item_button.check_press(x, y):
                self.inventory.delete_item_button.is_pressed = False
                self.inventory.remove_item(self.inventory.checked_item)
                self.inventory.checked_item = None

        # consumables
        if self.game_state == STATE_CONSUMABLES:
            for consumable_type in self.consumables_list.consumable_types:
                # if use button pressed
                if consumable_type.checked_item and consumable_type.use_consumable_button.check_press(x, y):
                    consumable_type.checked_item.use()
                    self.apply_effects(consumable_type.checked_item.effects)
                    if consumable_type.checked_item.value == 0:
                        self.consumables_list.uncheck_all()
                else:
                    for consumable in consumable_type.consumables:
                        if is_cursor_on_object(consumable, x, y):
                            self.consumables_list.uncheck_all()
                            consumable_type.checked_item = consumable

            if self.consumables_list.back_button.check_press(x, y):
                self.consumables_list.back_button.is_pressed = False
                self.consumables_list.checked_item = None
                self.game_state = STATE_MAIN

    def apply_after_effects(self):
        # here we insert any game logic that will execute after each player move

        # if spear is in inventory then we set flag 3 to 1
        if self.inventory.is_item_id_in_inventory(self.items, 0):
            changed_flag = get_by_id(self.flags, 3)
            changed_flag.set(1)

    def apply_effects(self, effects):
        if effects:
            for effect in effects:
                effect_type = effect["effect_type"]
                target = effect["target"] if "target" in effect else None
                value = effect["value"] if "value" in effect else None

                if effect_type == "CHANGE_STAT":
                    changed_stat = get_by_id(self.stats, target)
                    changed_stat.change(value)
                elif effect_type == "SET_FLAG":
                    changed_flag = get_by_id(self.flags, target)
                    changed_flag.set(value)
                elif effect_type == "ADD_ITEMS":
                    for item_id in effect["item_ids"]:
                        self.inventory.add_item_by_id(self.items, item_id)
                elif effect_type == "ADD_CONSUMABLE":
                    changed_consumable = get_consumable_by_id(self.consumables_list, target)
                    changed_consumable.change(value)
                elif effect_type == "CHANGE_GAME_STATE":
                    # print(f'gamestate changet to {target}')
                    self.game_state = target
                elif effect_type == "THROW_DICE":
                    dice_effects = effect["dice_effects"]
                    player_dice = random.randint(1, len(dice_effects))
                    for dice_effect in dice_effects:
                        if dice_effect["number"] == player_dice:
                            self.current_scene_id = dice_effect["target"]
                            self.is_scene_changed = True
                            break
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
