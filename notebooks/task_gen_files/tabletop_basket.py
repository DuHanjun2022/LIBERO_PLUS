from gen_utils import generate_task_bddl
from gen_utils import ObjectInitState, TaskInitState, DestInitState, BackgroundInitState, Distribution

from pprint import pprint
"""
This is the tabletop manipulation task putting objects into a basket:

LIVING_ROOM_SCENE2_put_both_the_cream_cheese_box_and_the_butter_in_the_basket
LIVING_ROOM_SCENE2_put_both_the_alphabet_soup_and_the_tomato_sauce_in_the_basket
LIVING_ROOM_SCENE1_put_both_the_alphabet_soup_and_the_cream_cheese_box_in_the_basket

We extend the difficulty by modifying the receptacle location, and enumerate any 2 objects as the target objects

"""

# we create combinations of all the dimensions of complexity
# instead maintain mapping between id and the task complexity


# create separate task suite for eval set?
task_name = "tabletop_basket"
train_backgrounds = ["living_room", "kitchen", "floor"]
eval_backgrounds = ["study"]

train_objs = ["alphabet_soup", "tomato_sauce", "milk", "cream_cheese"]
eval_objs = ["orange_juice", "butter", "ketchup"]

dest = "basket"


all_objs = train_objs + eval_objs

id_task_mapping = {}

train = False

if train:
    task_suite = "libero_10_random"
    objects = train_objs
    backgrounds = train_backgrounds
else:
    task_suite = "custom_eval_easy"
    objects = eval_objs
    backgrounds = train_backgrounds + eval_backgrounds

for background_idx, background in enumerate(backgrounds):
    for obj_1_idx in range(len(objects)):
        for obj_2_idx in range(len(objects)):
            if obj_1_idx <= obj_2_idx:
                continue
                

            task_id =  1_000 * (2 - int(train)) + background_idx * 100 + obj_1_idx * 10 + obj_2_idx
            # we create task id 1_000 is for train task suite, 2_000 for easy_eval, 3_000 for hard_eval
            # 100 for background, 10 for obj_1, 1 for obj_2 idx

            obj_1 = objects[obj_1_idx]
            obj_2 = objects[obj_2_idx]

            id_task_mapping[task_id] = f"{background}_{task_name}_{obj_1}_{obj_2}"

            objs = []
            for obj in all_objs:
                obj_dest = None
                if obj == obj_1 or obj == obj_2:
                    obj_dest = dest + "_1"

                objs.append(ObjectInitState(name=obj, dest=obj_dest))

            target_phrases = []

            for obj in [obj_1, obj_2]:
                phrase = f"put the {obj.replace('_', ' ')} in the {dest}"
                target_phrases.append(phrase)

            lang = ", ".join(target_phrases[:-1]) + " and " + target_phrases[-1]


            print(f"")
            task = TaskInitState(
                name=task_name,
                language_instruction=lang,
                task_suite=task_suite,
                goal_type="In",
                dests=[
                    DestInitState(name="basket") 
                ],
                objs=objs,
                background=BackgroundInitState(name=background),
                default_dist=Distribution([-0.025, 0.0], [0.175, 0.3])
            )
            
            
            generate_task_bddl(task, task_id)


pprint(f"\nTask ID mapping:\n{id_task_mapping}")

# ['/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/LIVING_ROOM_TABLETOP_BASKET_SCENE1010_put_the_alphabet_soup_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/LIVING_ROOM_TABLETOP_BASKET_SCENE1020_put_the_alphabet_soup_in_the_basket_and_put_the_milk_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/LIVING_ROOM_TABLETOP_BASKET_SCENE1021_put_the_milk_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/LIVING_ROOM_TABLETOP_BASKET_SCENE1030_put_the_alphabet_soup_in_the_basket_and_put_the_cream_cheese_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/LIVING_ROOM_TABLETOP_BASKET_SCENE1031_put_the_cream_cheese_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/LIVING_ROOM_TABLETOP_BASKET_SCENE1032_put_the_cream_cheese_in_the_basket_and_put_the_milk_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/KITCHEN_TABLETOP_BASKET_SCENE1110_put_the_alphabet_soup_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/KITCHEN_TABLETOP_BASKET_SCENE1120_put_the_alphabet_soup_in_the_basket_and_put_the_milk_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/KITCHEN_TABLETOP_BASKET_SCENE1121_put_the_milk_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/KITCHEN_TABLETOP_BASKET_SCENE1130_put_the_alphabet_soup_in_the_basket_and_put_the_cream_cheese_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/KITCHEN_TABLETOP_BASKET_SCENE1131_put_the_cream_cheese_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/KITCHEN_TABLETOP_BASKET_SCENE1132_put_the_cream_cheese_in_the_basket_and_put_the_milk_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/FLOOR_TABLETOP_BASKET_SCENE1210_put_the_alphabet_soup_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/FLOOR_TABLETOP_BASKET_SCENE1220_put_the_alphabet_soup_in_the_basket_and_put_the_milk_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/FLOOR_TABLETOP_BASKET_SCENE1221_put_the_milk_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/FLOOR_TABLETOP_BASKET_SCENE1230_put_the_alphabet_soup_in_the_basket_and_put_the_cream_cheese_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/FLOOR_TABLETOP_BASKET_SCENE1231_put_the_cream_cheese_in_the_basket_and_put_the_tomato_sauce_in_the_basket.bddl',
#  '/home/leisongao/LIBERO/libero/libero/bddl_files/libero_10_random/FLOOR_TABLETOP_BASKET_SCENE1232_put_the_cream_cheese_in_the_basket_and_put_the_milk_in_the_basket.bddl']
# Encountered some failures:  []
# ('\n'
#  'Task ID mapping:\n'
#  "{1010: 'living_room_tabletop_basket_tomato_sauce_alphabet_soup', 1020: "
#  "'living_room_tabletop_basket_milk_alphabet_soup', 1021: "
#  "'living_room_tabletop_basket_milk_tomato_sauce', 1030: "
#  "'living_room_tabletop_basket_cream_cheese_alphabet_soup', 1031: "
#  "'living_room_tabletop_basket_cream_cheese_tomato_sauce', 1032: "
#  "'living_room_tabletop_basket_cream_cheese_milk', 1110: "
#  "'kitchen_tabletop_basket_tomato_sauce_alphabet_soup', 1120: "
#  "'kitchen_tabletop_basket_milk_alphabet_soup', 1121: "
#  "'kitchen_tabletop_basket_milk_tomato_sauce', 1130: "
#  "'kitchen_tabletop_basket_cream_cheese_alphabet_soup', 1131: "
#  "'kitchen_tabletop_basket_cream_cheese_tomato_sauce', 1132: "
#  "'kitchen_tabletop_basket_cream_cheese_milk', 1210: "
#  "'floor_tabletop_basket_tomato_sauce_alphabet_soup', 1220: "
#  "'floor_tabletop_basket_milk_alphabet_soup', 1221: "
#  "'floor_tabletop_basket_milk_tomato_sauce', 1230: "
#  "'floor_tabletop_basket_cream_cheese_alphabet_soup', 1231: "
#  "'floor_tabletop_basket_cream_cheese_tomato_sauce',

# ('\n'
#  'Task ID mapping:\n'
#  "{2010: 'living_room_tabletop_basket_butter_orange_juice', 2020: "
#  "'living_room_tabletop_basket_ketchup_orange_juice', 2021: "
#  "'living_room_tabletop_basket_ketchup_butter', 2110: "
#  "'kitchen_tabletop_basket_butter_orange_juice', 2120: "
#  "'kitchen_tabletop_basket_ketchup_orange_juice', 2121: "
#  "'kitchen_tabletop_basket_ketchup_butter', 2210: "
#  "'floor_tabletop_basket_butter_orange_juice', 2220: "
#  "'floor_tabletop_basket_ketchup_orange_juice', 2221: "
#  "'floor_tabletop_basket_ketchup_butter', 2310: "
#  "'study_tabletop_basket_butter_orange_juice', 2320: "
#  "'study_tabletop_basket_ketchup_orange_juice', 2321: "
#  "'study_tabletop_basket_ketchup_butter'}")